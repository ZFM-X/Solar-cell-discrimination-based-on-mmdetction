import os
import datetime
import json
import time

import yaml
import flask

import requests

from aio_email import send_email

app = flask.Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

pipeline_state = {
    'ZH1620A': {'current_state': 'offline', 'reload_thr': 3},
    # '01B': {'current_state': 'offline', 'reload_thr': 3},
    
    '01A': {'current_state': 'offline', 'reload_thr': 3},
    '01B': {'current_state': 'offline', 'reload_thr': 3},

    '4F_02A_test': {'current_state': 'offline', 'reload_thr': 3},
    'ZH_1620A_test': {'current_state': 'offline', 'reload_thr': 3},
    
    '02A': {'current_state': 'offline', 'reload_thr': 3},
    '02B': {'current_state': 'offline', 'reload_thr': 3},

    '03A': {'current_state': 'offline', 'reload_thr': 3},
    '03B': {'current_state': 'offline', 'reload_thr': 3},

    '04A': {'current_state': 'offline', 'reload_thr': 3},
    '04B': {'current_state': 'offline', 'reload_thr': 3},

    '05A': {'current_state': 'offline', 'reload_thr': 3},
    '05B': {'current_state': 'offline', 'reload_thr': 3},

    '06A': {'current_state': 'offline', 'reload_thr': 3},
    '06B': {'current_state': 'offline', 'reload_thr': 3},

    '07A': {'current_state': 'offline', 'reload_thr': 3},
    '07B': {'current_state': 'offline', 'reload_thr': 3},

    '08A': {'current_state': 'offline', 'reload_thr': 3},
    '08B': {'current_state': 'offline', 'reload_thr': 3},
    
    '09A': {'current_state': 'offline', 'reload_thr': 3},
    '09B': {'current_state': 'offline', 'reload_thr': 3},

    '10A': {'current_state': 'offline', 'reload_thr': 3},
    '10B': {'current_state': 'offline', 'reload_thr': 3},

    '11A': {'current_state': 'offline', 'reload_thr': 3},
    '11B': {'current_state': 'offline', 'reload_thr': 3},

    # '12A': {'current_state': 'offline', 'reload_thr': 3},
    # '12B': {'current_state': 'offline', 'reload_thr': 3},

    '13A': {'current_state': 'offline', 'reload_thr': 3},
    '13B': {'current_state': 'offline', 'reload_thr': 3},

    '14A': {'current_state': 'offline', 'reload_thr': 3},
    '14B': {'current_state': 'offline', 'reload_thr': 3},
    '15A': {'current_state': 'offline', 'reload_thr': 3},

    '15B': {'current_state': 'offline', 'reload_thr': 3},
    '16A': {'current_state': 'offline', 'reload_thr': 3},
    '16B': {'current_state': 'offline', 'reload_thr': 3},

    '17A': {'current_state': 'offline', 'reload_thr': 3},
    '17B': {'current_state': 'offline', 'reload_thr': 3},

    '18A': {'current_state': 'offline', 'reload_thr': 3},
    '18B': {'current_state': 'offline', 'reload_thr': 3},

    '19A': {'current_state': 'offline', 'reload_thr': 3},
    '19B': {'current_state': 'offline', 'reload_thr': 3},

    '20A': {'current_state': 'offline', 'reload_thr': 3},
    '20B': {'current_state': 'offline', 'reload_thr': 3},
    
    '21A': {'current_state': 'offline', 'reload_thr': 3},
    '21B': {'current_state': 'offline', 'reload_thr': 3},
}

empty_state = False
collect_state = False  # 经历一个完整收集周期
email_send_done = True
aio_config = yaml.load(open('C:\\workspace\\el_infer_online\\aio_config.yaml', 'r', encoding='utf-8').read(), yaml.FullLoader)['pipeline']


@app.route("/alive", methods=["POST"])
def predict():

    global pipeline_state
    global collect_state
    global empty_state
    global email_send_done

    data = {"success": False}

    if int(time.time() // 10) % 2 == 0:  # 10秒根据状态做动作，并清空状态
        from deploy_assistant import da_client # 为了确保用上最新代码，每次重新导入

        offlines = [k for k in pipeline_state if pipeline_state[k]['current_state'] == 'offline']
        if (empty_state==False) and (collect_state==True):
            for pipeline_name in offlines:
                if pipeline_state[pipeline_name].get('continuous_timeout_times', None) is None:
                    pipeline_state[pipeline_name]['continuous_timeout_times'] = 0
                pipeline_state[pipeline_name]['continuous_timeout_times'] += 1
                # 连续3个周期未收到心跳，重启程序
                if (pipeline_state[pipeline_name]['continuous_timeout_times'] >= 30) and (pipeline_state[pipeline_name]['current_state'] != 'restart'):
                    pipeline_state[pipeline_name]['current_state'] = 'restart'
                    print(pipeline_name + ' timeout 3 times, prepare to restart it ...')
                    try:
                        da_client.pull_and_restart(ip=aio_config[pipeline_name]['ip_infer_machine'], pipeline_name=pipeline_name, only_when_exist_win=True)
                    except requests.exceptions.ConnectionError:
                        print(f'{pipeline_name} pull_and_restart 请求失败')
                    pipeline_state[pipeline_name]['continuous_timeout_times'] = 0
                    # pipeline_state[pipeline_name]['current_state'] = 'online'

            email_content = str(datetime.datetime.now()) + ' - offline: ' + ', '.join(offlines)
            if (len(offlines) > 0):
                print(email_content)
                if (int(time.time()//60) % 60 == 0) and (email_send_done==False):
                    email_send_done = True
                    # send_email(title='ai2 warning', content=email_content)
                else:
                    email_send_done = False
            else:
                print('\r'+email_content, end='')
        
        empty_state = True
        collect_state = False

        for pipeline_name in pipeline_state:
            # if pipeline_state[pipeline_name]['current_state'] == 'online':
            pipeline_state[pipeline_name]['current_state'] = 'offline'
        
        data['success'] = True
        return flask.jsonify(data)
    else:  # 10秒收集状态
        collect_state = True
        empty_state = False

        if flask.request.method == 'POST':
            if flask.request.content_type.startswith('application/json'):
                pipeline_name = flask.request.json.get('pipeline_name')
                if pipeline_name in pipeline_state: # 仅监视pipeline_state中列出的线别
                    pipeline_state[pipeline_name]['current_state'] = 'online'
                    pipeline_state[pipeline_name]['continuous_timeout_times'] = 0
                data['success'] = True

    return flask.jsonify(data)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
