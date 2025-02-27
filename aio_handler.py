import os
import shutil
import datetime
import json
import time
from datetime import datetime, date, timedelta
import cv2
import numpy as np
import requests
from watchdog.events import FileSystemEventHandler
from mmdet.apis import inference_detector

from post_process import convert_rcnn_result_to_el_rule_condition
from aio_db import *
from aio_db_result import writehalm_ak_secaidata,writehalm_ak_secokaidata
from aio_upload_img import upload_img
from aio_defect_name import names as defect_name_map
from aio_kafka import result_to_kafka


class PNGEventHandler(FileSystemEventHandler):

    def __init__(self, config: dict, model, ruleEngine, logger):

        self.count_create = 0
        self.previous_png = ''

        self.config = config
        self.model = model
        self.ruleEngine = ruleEngine
        self.logger = logger

        self.max_read_times = 10
    
    def extract_info_var_name(self, filename_parser: str, filename: str):
        if filename_parser == "halm":
            image_name_info = filename.split('_')
            wafer_id, wafer_bin = image_name_info[-3], image_name_info[-2]
            return {'wafer_id': wafer_id, 'wafer_bin': wafer_bin}
        if filename_parser == "lxt":
            image_name_info = filename.split('\\')[-1].split('_')
            wafer_id, wafer_bin = image_name_info[1], image_name_info[0][len('BIN'):]
            return {'wafer_id': wafer_id, 'wafer_bin': wafer_bin}
    
    def generate_dst_dir(self, filename_parser: str, filename: str, work_dir: str, rule_engine_result_0: str):
        if filename_parser == "halm":
            if self.config.get('write_image_with_half_hour',True):
                now_hour = datetime.now().strftime("%M")
                hlocal = datetime.now().strftime("%Y_%m_%d_%H")
                hnext = (datetime.now() + timedelta(hours=1)).strftime("%Y_%m_%d_%H")
                mintmp = int(now_hour) / 30
                if mintmp < 1:
                    hdir = hlocal[11:13] + "：00" + "-" + hlocal[11:13] + "：30"
                else:
                    hdir = hlocal[11:13] + "：30" + "-" + hnext[11:13] + "：00"
                if filename.split('\\')[-3]=="EL_OK_22.6":
                    dst_dir = os.path.join(work_dir,str(time.strftime('%Y_%m')),str(time.strftime('%Y_%m_%d')),hdir, "EL_OK_DX")
                elif filename.split('\\')[-3]=="EL_OK":
                    dst_dir = os.path.join(work_dir,str(time.strftime('%Y_%m')),str(time.strftime('%Y_%m_%d')),hdir, rule_engine_result_0)
                else:
                    dst_dir = os.path.join(work_dir, *filename.split('\\')[-4:-2],str(time.strftime('%Y_%m_%d')),hdir, rule_engine_result_0)
            else:
                if filename.split('\\')[-3]=="EL_OK_22.6":
                    dst_dir = os.path.join(work_dir,str(time.strftime('%Y_%m')),str(time.strftime('%Y_%m_%d')),str(time.strftime('%m_%d_%H')), "EL_OK_DX")
                elif filename.split('\\')[-3]=="EL_OK":
                    dst_dir = os.path.join(work_dir,str(time.strftime('%Y_%m')),str(time.strftime('%Y_%m_%d')),str(time.strftime('%m_%d_%H')), rule_engine_result_0)
                else:
                    dst_dir = os.path.join(work_dir, *filename.split('\\')[-4:-2],str(time.strftime('%Y_%m_%d')),str(time.strftime('%m_%d_%H')), rule_engine_result_0)
            return dst_dir
        if filename_parser == "lxt":
            dst_dir = os.path.join(work_dir, filename.split('\\')[-4][:6], *filename.split('\\')[-4:-2],str(time.strftime('%Y_%m_%d')),str(time.strftime('%m_%d_%H')),rule_engine_result_0)
            return dst_dir

    def on_created(self, event):
        super().on_created(event)

        if not event.is_directory:
            # if os.path.splitext((src_path := event.src_path))[-1] in ['.png', '.jpg', '.bmp']:
            if os.path.splitext((src_path := event.src_path))[-1] in ['.png', '.bmp']:
                if os.path.exists(src_path):
                    if (len([folder_name for folder_name in self.config['folder_name'] if folder_name in src_path])) and (src_path != self.previous_png):
                        self.previous_png = src_path
                        
                        # bin为102，108，>=120
                        image_name_info1 = self.extract_info_var_name(filename_parser=self.config['filename_parser'], filename=src_path)
                        bin_=int(image_name_info1['wafer_bin'])
                        print("bin",bin_) # int
                        print("EL_?",src_path.split('\\')[-3])
 
                        if bin_ >=120 or bin_ == 102 or bin_ ==108: # B级复判
                            try:
                                img_fullname = src_path
                                self.logger.info(f'observed created image: {img_fullname}')

                                for read_time in range(1, self.max_read_times):
                                    try:
                                        time.sleep(0.05)
                                        image_grayscale = cv2.imdecode(np.fromfile(img_fullname, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                                        if image_grayscale is None:
                                            continue
                                        # image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
                                        break
                                    except:
                                        self.logger.warn(f'reading failed {read_time} times: {img_fullname}')
                                        
                                image_bgr = cv2.imdecode(np.fromfile(img_fullname, dtype=np.uint8), cv2.IMREAD_COLOR)
                                if image_grayscale.shape[0] != 800:  #halm  1200
                                    image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
                                    image_bgr = cv2.resize(image_bgr, (1024, 1024))
                                if image_grayscale.shape[0] == 800:   #力禧特
                                    image_grayscale = cv2.transpose(image_grayscale)
                                    image_grayscale = cv2.flip(image_grayscale, 1)
                                    image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
                                    image_bgr = cv2.resize(image_bgr, (1024, 1024))
                                    image_bgr = cv2.transpose(image_bgr)
                                    image_bgr = cv2.flip(image_bgr, 1)
                                    # cv2.imshow('img', image_bgr)
                                    # cv2.waitKey(0)
                                # image_bgr = cv2.imdecode(np.fromfile(img_fullname, dtype=np.uint8), cv2.IMREAD_COLOR)
                                # image_bgr = cv2.resize(image_bgr, (1024, 1024))
                                result = inference_detector(
                                        self.model, image_bgr)
                                defects_info, defects_info_overview = convert_rcnn_result_to_el_rule_condition(
                                    result=result, 
                                    category_names=self.model.CLASSES, 
                                    image=image_grayscale,
                                    config=self.ruleEngine.config
                                )

                                rule_engine_result = self.ruleEngine.defect_handle(defects=defects_info)
                                rule_engine_result_category = [defects_info[di]['category'] for di in rule_engine_result[1]]
                                
                                self.logger.info(f"Final level: {rule_engine_result[0]}")
                                self.logger.info(f"Worst level defect: {rule_engine_result_category}")
                                self.logger.info(f"Level per defect: {[(defects_info[i]['category'], self.ruleEngine.config['defect_level_good_to_bad'][rule_engine_result[2][i]]) for i in range(len(rule_engine_result[2]))]}")

                                # image_name_info = img_fullname.split('_')
                                image_name_info = self.extract_info_var_name(filename_parser=self.config['filename_parser'], filename=img_fullname)
                                
                                if ((defect_name_map_key:=self.config.get('upload_ng_img', False)) != False) and (rule_engine_result[0] == 'NG'):  # 如果拦截时有图片为NG，则上传图片
                                    upload_img_response = upload_img(
                                        img_filename=img_fullname,
                                        pipeline_name=self.config['mes_eqp_id'],
                                        wafer_id=image_name_info['wafer_id'],
                                        wafer_bin=image_name_info['wafer_bin'],
                                        defect_name_cn=defect_name_map[defect_name_map_key][rule_engine_result_category[0]]['name_cn'],
                                        defect_name_en=defect_name_map[defect_name_map_key][rule_engine_result_category[0]]['name_en'],
                                        logger=self.logger,
                                    )
                                    self.logger.info(f"Upload img response: {upload_img_response}")

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
                                        'wafer_id': image_name_info['wafer_id'],
                                        'ai_result': mes_ai_result,
                                        'halm_bin': image_name_info['wafer_bin']
                                    },
                                    'metadata': {
                                        'msg_seq_ns': None, 
                                        'msg_seq': None
                                    }
                                }
                                mes_data = json.dumps(mes_data)
                                # print(mes_url, mes_data)

                                if (image_name_info['wafer_bin'] != '102') and (image_name_info['wafer_bin'] != '108') and (len(mes_url)>0):
                                    if self.config.get('is_write_halm_db', False):
                                        writehalm(m=img_fullname.split('\\')[-1], ai_result=mes_ai_result, docktablesname='aidata_a' if self.config['mes_eqp_id'].endswith('A') else 'aidata_b')
                                        
                                    self.logger.info(f'sended to MES: {mes_data}')
                                
                                    response = requests.post(mes_url, mes_data, headers=mes_header)
                                    # print(response.text)
                                    self.logger.info(f'response from MES: {response.text}')

                                if self.config.get('is_write_halm_ak_secaidata',True):
                                    writehalm_ak_secaidata(m=img_fullname.split('\\')[-1], ai_result=mes_ai_result, docktablesname='halm_a' if self.config['mes_eqp_id'].endswith('A') else 'halm_b')

                                # if self.config.get('is_write_ok_to_kafka',True): 
                                #     result_to_kafka(c=img_fullname.split('\\')[-3],m=img_fullname.split('\\')[-1], wafer_id=image_name_info['wafer_id'], ai_result=mes_ai_result, result_name=defect_name_map['4c'][rule_engine_result_category[0]]['name_cn'] if mes_ai_result==1 else 'OK', eqp_blk=self.config['eqp_blk'], topic='halm-ai-a')
                                
                                # 添加线别头
                                if self.config['filename_parser'] == 'lxt':
                                    modified_last_name = self.config['mes_eqp_id'][3:]+(img_fullname.split('\\')[-1])
                                elif self.config['filename_parser'] == 'halm':
                                    modified_last_name = self.config['mes_eqp_id'][3:]+(img_fullname.split('\\')[-1])
                                else:
                                    raise Exception

                                # AI2自己的work_dir
                                dst_dir = self.generate_dst_dir(
                                    filename_parser=self.config['filename_parser'],  #  filename_parser: 'lxt',
                                    filename=img_fullname, 
                                    work_dir=self.config['work_dir'],  # work_dir: 'F:\F1601BELv3.1\processed_el',  # 保存图片的目录
                                    rule_engine_result_0=rule_engine_result[0] # NG or OK
                                )
                                
                                if not os.path.exists(dst_dir):
                                    os.makedirs(dst_dir)
                                dst_file_fullname = os.path.join(dst_dir, modified_last_name)
                                shutil.copyfile(img_fullname, dst_file_fullname)
                                self.logger.info(f'saved image: {dst_file_fullname}')

                                # ok片放A级片NG目录中
                                if (rule_engine_result[0] == "OK") and (self.config['put_ai2_ok_to_eqp_okng'] == True):
                                    if (image_name_info['wafer_bin'] != '102') and (image_name_info['wafer_bin'] != '108'):
                                        dst_dir_ok_ng = os.path.join(
                                            self.config['work_dir_ok'], 
                                            str(time.strftime('%Y_%m')), 
                                            str(time.strftime('%Y_%m_%d')),
                                            str(time.strftime('%m_%d_%H')),
                                            'NG')
                                        if not os.path.exists(dst_dir_ok_ng):
                                            os.makedirs(dst_dir_ok_ng)
                                        dst_file_ok_ng_fullname = os.path.join(dst_dir_ok_ng, modified_last_name)
                                        shutil.copyfile(dst_file_fullname, dst_file_ok_ng_fullname)
                                        self.logger.info(f'saved ok image: {dst_file_ok_ng_fullname}')

                                self.count_create += 1
                                
                                self.logger.info(f'Count: {self.count_create}')

                            except Exception as e:
                                self.logger.error(f'Exception: {e}')
                        
                        elif src_path.split('\\')[-3]=="EL_OK_22.6" or src_path.split('\\')[-3]=="EL_OK": # A级拦截
                            try:
                                img_fullname = src_path
                                self.logger.info(f'observed created image: {img_fullname}')

                                for read_time in range(1, self.max_read_times):
                                    try:
                                        time.sleep(0.05)
                                        image_grayscale = cv2.imdecode(np.fromfile(img_fullname, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                                        if image_grayscale is None:
                                            continue
                                        # image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
                                        break
                                    except:
                                        self.logger.warn(f'reading failed {read_time} times: {img_fullname}')
                                        
                                image_bgr = cv2.imdecode(np.fromfile(img_fullname, dtype=np.uint8), cv2.IMREAD_COLOR)
                                if image_grayscale.shape[0] != 800:  #halm  1200
                                    image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
                                    image_bgr = cv2.resize(image_bgr, (1024, 1024))
                                if image_grayscale.shape[0] == 800:   #力禧特
                                    image_grayscale = cv2.transpose(image_grayscale)
                                    image_grayscale = cv2.flip(image_grayscale, 1)
                                    image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
                                    image_bgr = cv2.resize(image_bgr, (1024, 1024))
                                    image_bgr = cv2.transpose(image_bgr)
                                    image_bgr = cv2.flip(image_bgr, 1)

                                result = inference_detector(
                                        self.model, image_bgr)
                                defects_info, defects_info_overview = convert_rcnn_result_to_el_rule_condition(
                                    result=result, 
                                    category_names=self.model.CLASSES, 
                                    image=image_grayscale,
                                    config=self.ruleEngine.config
                                )

                                rule_engine_result = self.ruleEngine.defect_handle(defects=defects_info)
                                rule_engine_result_category = [defects_info[di]['category'] for di in rule_engine_result[1]]
                                
                                self.logger.info(f"Final level: {rule_engine_result[0]}")
                                self.logger.info(f"Worst level defect: {rule_engine_result_category}")
                                self.logger.info(f"Level per defect: {[(defects_info[i]['category'], self.ruleEngine.config['defect_level_good_to_bad'][rule_engine_result[2][i]]) for i in range(len(rule_engine_result[2]))]}")
                                rule_engine_result_category_ng_t = [defects_info[i]['category'] for i in range(len(rule_engine_result[2])) if self.ruleEngine.config['defect_level_good_to_bad'][rule_engine_result[2][i]] == 'NG']
                                rule_engine_result_category_ng = sorted(set(rule_engine_result_category_ng_t),key=rule_engine_result_category_ng_t.index)
                                # image_name_info = img_fullname.split('_')
                                image_name_info = self.extract_info_var_name(filename_parser=self.config['filename_parser'], filename=img_fullname)
                                

                                # AI2自己的work_dir
                                dst_dir = self.generate_dst_dir(
                                    filename_parser=self.config['filename_parser'],  #  filename_parser: 'lxt',
                                    filename=img_fullname, 
                                    work_dir=self.config['work_dir'],  # work_dir: 'F:\F1601BELv3.1\processed_el',  # 保存图片的目录
                                    rule_engine_result_0=rule_engine_result[0] # NG or OK
                                )
                                
                                if not os.path.exists(dst_dir):
                                    os.makedirs(dst_dir)
                                
                                mes_ai_result = None
                                if rule_engine_result[0] == "UD":
                                    mes_ai_result = 2
                                elif rule_engine_result[0] == "NG":
                                    mes_ai_result = 1
                                elif rule_engine_result[0] == "OK":
                                    mes_ai_result = 0
                                
                                if self.config.get('is_write_halm_ak_secokaidata',True):
                                    writehalm_ak_secokaidata(c=img_fullname.split('\\')[-3],m=img_fullname.split('\\')[-1], ai_result=mes_ai_result, docktablesname='halm_a' if self.config['mes_eqp_id'].endswith('A') else 'halm_b')
                                
                                if self.config.get('is_write_ok_to_kafka',True): 
                                    result_to_kafka(c=img_fullname.split('\\')[-3],m=img_fullname.split('\\')[-1], wafer_id=image_name_info['wafer_id'], ai_result=mes_ai_result, result_name=defect_name_map['4c'][rule_engine_result_category[0]]['name_cn'] if mes_ai_result==1 else 'OK', eqp_blk=self.config['mes_eqp_id'], topic='halm-ai-a')
                                
                                # img_name, img_type = os.path.splitext(img_fullname.split('\\')[-1])
                                parts = img_fullname.split('\\')[-1].split('_')
                                # 添加线别头
                                if self.config['filename_parser'] == 'lxt':
                                    modified_last_name = self.config['mes_eqp_id'][3:]+(img_fullname.split('\\')[-1])
                                elif self.config['filename_parser'] == 'halm':
                                    if img_fullname.split('\\')[-3]=="EL_OK_22.6": # 低效片
                                        modified_last_name = self.config['mes_eqp_id'][3:] + "_" + "_".join(parts[:2]) + "_" + "OKDX" + "_" + "_".join(parts[2:])
                                    else:
                                        # modified_last_name = self.config['mes_eqp_id'][3:]+"_"+ rule_engine_result[0] +"_"+(img_fullname.split('\\')[-1])
                                        # modified_last_name = self.config['mes_eqp_id'][3:]+"_"+ rule_engine_result[0] + "_" + "-".join(rule_engine_result_category_ng) + "_"+ (img_fullname.split('\\')[-1])
                                        if rule_engine_result[0] == 'OK':
                                            modified_last_name = self.config['mes_eqp_id'][3:] + "_" + "_".join(parts[:2]) + "_" + rule_engine_result[0] + "_" + "_".join(parts[2:])
                                        else: 
                                            modified_last_name = self.config['mes_eqp_id'][3:] + "_" + "_".join(parts[:2]) + "_" + rule_engine_result[0] + "_" + "-".join(rule_engine_result_category_ng) + "_" + "_".join(parts[2:])
                                else:
                                    raise Exception
                                print("modified",modified_last_name)
                                
                                dst_file_fullname = os.path.join(dst_dir, modified_last_name)
                                shutil.copyfile(img_fullname, dst_file_fullname)
                                self.logger.info(f'saved image: {dst_file_fullname}')
                                self.count_create += 1
                                
                                self.logger.info(f'Count: {self.count_create}')

                            except Exception as e:
                                self.logger.error(f'Exception: {e}')
                else:
                    # print(f'not exists: {src_path}')
                    self.logger.warn(f'not exists: {src_path}')