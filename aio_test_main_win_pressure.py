import os
import time
import yaml
import threading
from argparse import ArgumentParser

from watchdog.observers import Observer
from mmdet.apis import init_detector

from rule_engine import RuleEngine
from aio_logger import get_logger
from aio_handler import PNGEventHandler


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--config_file', help='.yaml file', default='./aio_test_config.yaml')
    parser.add_argument('--pipline_name', help='key(name) of pipline')

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_args()

    pipeline_name = args.pipline_name

    config = yaml.load(open(args.config_file, 'r', encoding='utf-8').read(), yaml.FullLoader)['pipeline'][pipeline_name]

    logger = get_logger(name=pipeline_name, filename=os.path.join(config['work_dir'], 'log', pipeline_name))

    model = init_detector(config['model_cfg'], config['checkpoint'], device=config['ai_device'])
    ruleEngine = RuleEngine(config=config['rule_engine_config'])

    while True:

        # print('尝试重新监控', time.time())
        logger.info('尝试重新监控 Try to observe...')

        observer = Observer()
        event_handler = PNGEventHandler(
            config=config, 
            model=model,
            ruleEngine=ruleEngine,
            logger=logger,
        )
        observer.schedule(event_handler, config['observer_path'], recursive=True)

        try:
            observer.start()
            # print('监控成功开启', time.time())
            logger.info(f"监控成功开启 Successfully start observing: {config['observer_path']}")
            try:
                while True:
                    time.sleep(0.01)
                    # print(threading.active_count(), time.time())
                    if (th_count:=threading.active_count()) < 3:
                        # print('监控线程数异常 abnormal observation: ', th_count, time.time())
                        logger.error(f'监控线程数异常 Abnormal observation: {th_count}')
                        break
            finally:
                observer.stop()
                observer.join()
        except:
            # print('重新监控尝试失败', threading.active_count(), time.time())
            logger.error(f'重新监控尝试失败，线程数 failed to observe, threads count: {threading.active_count()}')
        
        time.sleep(0.01)
