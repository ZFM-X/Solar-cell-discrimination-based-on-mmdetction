import os
import time
import yaml
import threading
from argparse import ArgumentParser

from watchdog.observers import Observer
from mmdet.apis import init_detector
import requests

from rule_engine import RuleEngine
from aio_logger import get_logger
from aio_handler import PNGEventHandler


def i_am_alive(pipeline_name: str):
    while True:
        try:
            url = 'http://172.16.97.177:5000/alive'

            headers = {
                'Accept': "application/json, text/plain, */*",
                "content_type": 'application/json',
            }

            form_data = {
                "pipeline_name": pipeline_name,
            }

            response = requests.post(url=url, json=form_data, headers=headers)

            # print('sended: ', response.content)
        except Exception as e:
            # print(e)
            pass

        time.sleep(5)  # 每5秒发送一次心跳


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--config_file', help='.yaml file', default=r'E:\Aikosolar\02_AI_rejudication\03_AI2\A级\el_infer_online\el_infer_online\aio_config.yaml')
    parser.add_argument('--pipline_name', help='key(name) of pipline', default='01A')

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_args()

    # beating_ts = time.time()  # call interface's timestamp

    pipeline_name = args.pipline_name

    config = yaml.load(open(args.config_file, 'r', encoding='utf-8').read(), yaml.FullLoader)['pipeline'][pipeline_name]

    logger_image_name = pipeline_name+'_image'
    logger_software_name = pipeline_name+'_software'

    logger_image = get_logger(name=logger_image_name, filename=os.path.join(config['work_dir'], 'log', logger_image_name+'.txt'))
    logger_software = get_logger(name=logger_software_name, filename=os.path.join(config['work_dir'], 'log', logger_software_name+'.txt'))

    model = init_detector(config['model_cfg'], config['checkpoint'], device=config['ai_device'])
    ruleEngine = RuleEngine(config=config['rule_engine_config'])

    logger_software.info(f"Using model: {config['model_cfg']}")
    logger_software.info(f"Using checkpoint: {config['checkpoint']}")
    logger_software.info(f"Using rule_engine_config: {config['rule_engine_config']}")

    # 启动一个专用线程来发送心跳
    thread_beating = threading.Thread(target=i_am_alive, args=(pipeline_name,))
    thread_beating.start()

    while True:

        # print('尝试重新监控', time.time())
        logger_software.info('尝试重新监控 Try to observe...')

        observer = Observer()
        event_handler = PNGEventHandler(
            config=config, 
            model=model,
            ruleEngine=ruleEngine,
            logger=logger_image,
        )
        observer.schedule(event_handler, config['observer_path'], recursive=True)

        try:
            observer.start()
            # print('监控成功开启', time.time())
            logger_software.info(f"监控成功开启 Successfully start observing: {config['observer_path']}")
            try:
                while True:
                    time.sleep(0.01)
                    # print(threading.active_count(), time.time())
                    if (th_count:=threading.active_count()) < 4:
                        # print('监控线程数异常 abnormal observation: ', th_count, time.time())
                        logger_software.error(f'监控线程数异常 Abnormal observation: {th_count}')
                        break
                    # if (time.time()-beating_ts) > 5:
                    #     i_am_alive(pipeline_name=pipeline_name)
                    #     # beating_ts = time.time()
            finally:
                observer.stop()
                # observer.join()
        except:
            # print('重新监控尝试失败', threading.active_count(), time.time())
            logger_software.error(f'重新监控尝试失败，线程数 failed to observe, threads count: {threading.active_count()}')
        
        time.sleep(0.01)

