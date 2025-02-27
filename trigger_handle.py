import re
import os
import time
import shutil
import datetime
import json
import logging

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver as Observer
import torch
import numpy as np
import cv2
from mmcv.ops.nms import nms, batched_nms
from mmdet.core.post_processing.bbox_nms import multiclass_nms
from mmdet.apis import inference_detector
from mmdet.apis import init_detector
# from mmdeploy.utils import Backend, get_backend, get_input_shape, load_config
# from mmdeploy.codebase import BaseTask

# from prepare_task_processor import get_task_processor
# from prepare_model import get_model
from post_process import convert_rcnn_result_to_el_rule_condition
# from utils_coco import get_category_names
from rule_engine import RuleEngine
# from vai_web import VaiWeb
from utils import get_latest_month, is_later_month

class PNGEventHandler(FileSystemEventHandler):

    # def __init__(self, model_cfg, checkpoint, rule_engine_config):
    def __init__(self, config, model, ruleEngine, work_dir):

        self.count_create = 0
        # self.ts = time.time()

        # self.model_cfg = model_cfg
        # self.checkpoint = checkpoint

        self.logger = logging.getLogger('report')

        self.config = config

        self.model = model
        self.category_names = self.model.CLASSES
        self.ruleEngine = ruleEngine
        self.work_dir = work_dir

        # self.model_cfg = model_cfg
        # self.checkpoint = checkpoint
        # self.model = init_detector(self.model_cfg, self.checkpoint, device='cuda:0')
        # self.category_names = self.model.CLASSES
        # self.ruleEngine = RuleEngine(config=rule_engine_config)

    def on_created(self, event):
        super().on_created(event)

        if not event.is_directory:
            if (src_path := event.src_path).endswith('.png'):
                if os.path.exists(src_path):
                    ts = time.time()
                    print(src_path)
                    if self.config['folder_name'] in src_path:

                        try:

                            img_fullname = src_path
                            # print(src_path)

                            image_grayscale = cv2.imread(
                                img_fullname, flags=cv2.IMREAD_GRAYSCALE)
                            image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
                            
                            image_bgr = cv2.imread(img_fullname)
                            image_bgr = cv2.resize(image_bgr, (1024, 1024))
                            result = inference_detector(
                                    self.model, image_bgr)
                            defects_info, defects_info_overview = convert_rcnn_result_to_el_rule_condition(
                                result=result, 
                                category_names=self.category_names, 
                                image=image_grayscale,
                                config=self.ruleEngine.config
                            )

                            rule_engine_result = self.ruleEngine.defect_handle(defects=defects_info)
                            rule_engine_result_category = [defects_info[di]['category'] for di in rule_engine_result[1]]
                            
                            print("Final level:", rule_engine_result[0])
                            print("Worst level defect: ", rule_engine_result_category)
                            print("Level per defect: ", [(defects_info[i]['category'], self.ruleEngine.config['defect_level_good_to_bad'][rule_engine_result[2][i]]) 
                                for i in range(len(rule_engine_result[2]))], )

                            image_name_info = img_fullname.split('_')

                            mes_ai_result = None
                            if rule_engine_result[0] == "UD":
                                mes_ai_result = 2
                            elif rule_engine_result[0] == "NG":
                                mes_ai_result = 1
                            elif rule_engine_result[0] == "OK":
                                mes_ai_result = 0

                            mes_url = self.config['mes_url']  # 'http://172.16.97.154:1230/api/label/halmbin/ai_push'
                            mes_header = {'content-type': 'application/json'}
                            mes_data = {
                                'event': 'halmbin_ai_push',
                                'event_time': str(datetime.datetime.now()),
                                'data': {
                                    'eqp_id': self.config['mes_eqp_id'],
                                    'wafer_id': image_name_info[-3],
                                    'ai_result': mes_ai_result,
                                    'halm_bin': image_name_info[-2]  # .split('.')[0]
                                },
                                'metadata': {
                                    'msg_seq_ns': None, 
                                    'msg_seq': None
                                }
                            }
                            mes_data = json.dumps(mes_data)
                            print(mes_url, mes_data)
                            
                            response = requests.post(mes_url, mes_data, headers=mes_header)
                            print(response.text)

                            self.count_create += 1
                            print('FPS: ', round(1 / (time.time() - ts), 2))
                            print('Count: ', self.count_create)

                            dst_dir = os.path.join(self.work_dir, *img_fullname.split('/')[-3:-1], rule_engine_result[0])
                            if not os.path.exists(dst_dir):
                                os.makedirs(dst_dir)
                            shutil.copyfile(img_fullname, os.path.join(dst_dir, img_fullname.split('/')[-1]))

                            self.logger.info(mes_data)
                        except Exception as e:
                            self.logger.info(e)
                else:
                    print('不存在', src_path)


class MonthCreateEventHandler(FileSystemEventHandler):

    def __init__(self, config, observe_job, model_cfg, checkpoint, rule_engine_config):

        self.config=config
        self.model_cfg = model_cfg
        self.checkpoint = checkpoint
        self.model = init_detector(self.model_cfg, self.checkpoint, device=self.config['ai_device'])
        self.ruleEngine = RuleEngine(config=rule_engine_config)

        self.observe_job = observe_job


        for i in self.observe_job:
            self.create_observe(job_info=i)

    def create_observe(self, job_info):
        self.observer = Observer()
        self.event_handler = PNGEventHandler(
            config=self.config, 
            model=self.model, 
            ruleEngine=self.ruleEngine,
            work_dir=job_info['work_dir']
        )
        self.observer.schedule(self.event_handler, job_info['observe_full_path'], recursive=True)
        self.observer.start()

        # try:
        #     while True:
        #         time.sleep(1)
        # finally:
        #     # observer.stop()
        #     # observer.join()
        #     self.observer.stop()
        #     self.observer.join()

        #     self.create_observe(job_info)

    def on_created(self, event):
        super().on_created(event)
        # print('created: ', event.src_path)
        if event.is_directory:
            # print('dir: ', event.src_path)
            if src_path := event.src_path:  # 匹配文件夹名字是否为“年份-月份”格式
                print('detected month create event: ', src_path)
                # ob_folder = 'EL_NG'

                for job_info in self.observe_job:

                    if os.path.exists(src_path):

                        latest_month = get_latest_month(os.listdir(os.path.join(src_path, os.pardir)))
                        if latest_month == src_path.split('/')[-1]:  # 判断是否是最晚的月份目录

                            # try:
                            detect_folder_count = 0
                            while (True):
                                if job_info['folder_name'] is None:

                                    print('detected: ', src_path)

                                    job_info['observe_full_path'] = os.path.join(src_path)  # 不修改检测到的目录

                                    self.observer.stop()
                                    self.observer.join()

                                    self.create_observe(job_info=job_info)
                                    
                                    print('切换observer: ', src_path)
                                    break

                                elif (folder_name:=job_info['folder_name']) in os.listdir(src_path):

                                    # get_latest_month(monthes=os.listdir(path_year))
                                    # latest_month = get_latest_month(os.listdir(os.path.join(src_path, os.pardir)))
                                    # if latest_month == src_path.split('/')[-1]:  # 判断是否是最晚的月份目录
                                        
                                    print('detected: ', folder_name)

                                    job_info['observe_full_path'] = os.path.join(src_path, folder_name)

                                    self.observer.stop()
                                    self.observer.join()

                                    self.create_observe(job_info=job_info)

                                    print('切换observer: ', job_info['observe_full_path'])
                                    break
                                detect_folder_count += 1
                                time.sleep(1)
                                if detect_folder_count > 3600*6:  # 如果6小时未检测到EL_NG目录，则break
                                    break
                            # except Exception as e:
                            #     logging.getLogger('report').error(e)      
                    else:
                        print('不存在', src_path)