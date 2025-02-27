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


class PNGEventHandler(FileSystemEventHandler):

    # def __init__(self, model_cfg, checkpoint, rule_engine_config):
    def __init__(self, config, logger):

        # logger = logging.getLogger(pipline_name)
        self.logger = logger

        self.count_create = 0
        # self.ts = time.time()

        # self.model_cfg = model_cfg
        # self.checkpoint = checkpoint

        # self.logger = logging.getLogger('report')

        self.config = config

        self.previous_png = ''

        # self.model = model
        # self.category_names = self.model.CLASSES
        # self.ruleEngine = ruleEngine
        # self.work_dir = work_dir

        # self.model_cfg = model_cfg
        # self.checkpoint = checkpoint
        # self.model = init_detector(self.model_cfg, self.checkpoint, device='cuda:0')
        # self.category_names = self.model.CLASSES
        # self.ruleEngine = RuleEngine(config=rule_engine_config)

    def on_created(self, event):
        super().on_created(event)

        if not event.is_directory:
            if (src_path := event.src_path).endswith('.png'):
                if src_path != self.previous_png:
                    if os.path.exists(src_path):
                        ts = time.time()
                        # print(src_path)
                        if self.config['folder_name'] in src_path:
                        # if True:

                            # try:

                            self.logger.info('created:'+src_path)

                            img_fullname = src_path
                            print("prepare sending: "+img_fullname)

                            url = 'http://172.20.149.177:5000/predict'

                            headers = {
                                'Accept': "application/json, text/plain, */*",
                                "content_type": 'application/json',
                            }

                            form_data = {
                                "image": src_path,
                            }

                            response = requests.post(url=url, json=form_data, headers=headers)

                            print('sended: ', response.content)
                            self.logger.info('sended:'+img_fullname)

                            # except Exception as e:
                            #     self.logger.info(e)
                            self.previous_png = img_fullname
                    else:
                        print('不存在', src_path)
                        self.logger.error('不存在:'+src_path)


# class MonthCreateEventHandler(FileSystemEventHandler):

#     def __init__(self, config, observe_job, model_cfg, checkpoint, rule_engine_config):

#         self.config=config
#         self.model_cfg = model_cfg
#         self.checkpoint = checkpoint
#         self.model = init_detector(self.model_cfg, self.checkpoint, device=self.config['ai_device'])
#         self.ruleEngine = RuleEngine(config=rule_engine_config)

#         self.observe_job = observe_job


#         for i in self.observe_job:
#             self.create_observe(job_info=i)

#     def create_observe(self, job_info):
#         self.observer = Observer()
#         self.event_handler = PNGEventHandler(
#             config=self.config, 
#             model=self.model, 
#             ruleEngine=self.ruleEngine,
#             work_dir=job_info['work_dir']
#         )
#         self.observer.schedule(self.event_handler, job_info['observe_full_path'], recursive=True)
#         self.observer.start()

#         # try:
#         #     while True:
#         #         time.sleep(1)
#         # finally:
#         #     # observer.stop()
#         #     # observer.join()
#         #     self.observer.stop()
#         #     self.observer.join()

#         #     self.create_observe(job_info)

#     def on_created(self, event):
#         super().on_created(event)
#         # print('created: ', event.src_path)
#         if event.is_directory:
#             # print('dir: ', event.src_path)
#             if src_path := event.src_path:  # 匹配文件夹名字是否为“年份-月份”格式
#                 print('detected month create event: ', src_path)
#                 # ob_folder = 'EL_NG'

#                 for job_info in self.observe_job:

#                     if os.path.exists(src_path):

#                         latest_month = get_latest_month(os.listdir(os.path.join(src_path, os.pardir)))
#                         if latest_month == src_path.split('/')[-1]:  # 判断是否是最晚的月份目录

#                             # try:
#                             detect_folder_count = 0
#                             while (True):
#                                 if job_info['folder_name'] is None:

#                                     print('detected: ', src_path)

#                                     job_info['observe_full_path'] = os.path.join(src_path)  # 不修改检测到的目录

#                                     self.observer.stop()
#                                     self.observer.join()

#                                     self.create_observe(job_info=job_info)
                                    
#                                     print('切换observer: ', src_path)
#                                     break

#                                 elif (folder_name:=job_info['folder_name']) in os.listdir(src_path):

#                                     # get_latest_month(monthes=os.listdir(path_year))
#                                     # latest_month = get_latest_month(os.listdir(os.path.join(src_path, os.pardir)))
#                                     # if latest_month == src_path.split('/')[-1]:  # 判断是否是最晚的月份目录
                                        
#                                     print('detected: ', folder_name)

#                                     job_info['observe_full_path'] = os.path.join(src_path, folder_name)

#                                     self.observer.stop()
#                                     self.observer.join()

#                                     self.create_observe(job_info=job_info)

#                                     print('切换observer: ', job_info['observe_full_path'])
#                                     break
#                                 detect_folder_count += 1
#                                 time.sleep(1)
#                                 if detect_folder_count > 3600*6:  # 如果6小时未检测到EL_NG目录，则break
#                                     break
#                             # except Exception as e:
#                             #     logging.getLogger('report').error(e)      
#                     else:
#                         print('不存在', src_path)