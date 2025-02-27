import os
import re
import sys
import time
import logging
from argparse import ArgumentParser

import yaml
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import LoggingEventHandler

from trigger_handle import PNGEventHandler, MonthCreateEventHandler
from utils import get_latest_month

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--config_file', help='.yaml file', default='./config_online.yaml')
    parser.add_argument('--pipline_name', help='key(name) of pipline')

    args = parser.parse_args()

    return args

if __name__ == "__main__":

    args = parse_args()

    pipeline_name = args.pipline_name

    config = yaml.load(open(args.config_file, 'r').read(), yaml.FullLoader)['pipeline'][pipeline_name]

    path_year = config['path_year']
    print('固定监测目录：', path_year)

    path_month = os.path.join(path_year, get_latest_month(monthes=os.listdir(path_year)))

    folder_name = config['folder_name']

    # max_month = 0
    # for folder in os.listdir(path_year):
    #     if re.match(r'^20\d{2}-\d{1,2}$', folder):
    #         if (curr_month:=int(folder.split('-')[-1])) > max_month:
    #             max_month = curr_month
    #             path_month = os.path.join(path_year, folder)
    # assert max_month != 0, f'该{path_year}年份目录下未检测到任何月份目录'

    assert os.path.exists(os.path.join(path_month, folder_name)), f'该{path_month}月份目录下未检测到EL_NG目录'
    init_observe_path = os.path.join(path_month, folder_name)

    print('初始监测目录：', init_observe_path)

    # observer.schedule(event_handler, os.path.join(path_month, 'EL_NG'), recursive=True)
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    logger = logging.getLogger('report')
    logger.setLevel(logging.INFO)

    # create file handler
    # logger_file_path = os.path.join(report_folder_root, )
    if not os.path.exists('log'):
        os.mkdir('log')

    fh = logging.FileHandler('log/'+pipeline_name+'_logger.txt')
    fh.setLevel(logging.INFO)

    logger.addHandler(fh)

    observe_job = [{
        "folder_name": folder_name,
        "observe_full_path": init_observe_path,
        "work_dir": config['work_dir']
    }]

    event_handler_month_create = MonthCreateEventHandler(
        config=config,
        observe_job=observe_job, 
        model_cfg=config['model_cfg'],
        checkpoint=config['checkpoint'],
        rule_engine_config=config['rule_engine_config']
    )

    observer_month = Observer()
    observer_month.schedule(event_handler_month_create, path_year, recursive=False)


    observer_month.start()
    # observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        # observer.stop()
        # observer.join()
        observer_month.stop()
        observer_month.join()
