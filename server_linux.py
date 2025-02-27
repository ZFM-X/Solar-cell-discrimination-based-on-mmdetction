from copy import deepcopy
import os
import datetime
import json
import shutil

import requests
import yaml
import cv2
import flask
from mmdet.apis import init_detector
from mmdet.apis import inference_detector

from post_process import convert_rcnn_result_to_el_rule_condition
from rule_engine import RuleEngine


app = flask.Flask(__name__)
model_cuda_0 = None
model_cuda_1 = None
ruleEngine_ori = None
config = yaml.load(open('/home/aiuser/workspace/mmlab/el_infer_online/config_online.yaml', 'r').read(), yaml.FullLoader)['pipeline']


def load_model(model_cfg, checkpoint, rule_engine_config, device):
    """Load the pre-trained model, you can use your model just as easily.

    """
    global model_cuda_0
    global model_cuda_1
    global ruleEngine_ori

    model_cuda_0 = init_detector(model_cfg, checkpoint, device='cuda:0')
    model_cuda_1 = init_detector(model_cfg, checkpoint, device='cuda:1')
    ruleEngine_ori = RuleEngine(config=rule_engine_config)

    # model = resnet50(pretrained=True)
    # model.eval()
    # if use_gpu:
    #     model.cuda()


@app.route("/predict", methods=["POST"])
def predict():

    global model_cuda_0
    global model_cuda_1
    global ruleEngine_ori

    # Initialize the data dictionary that will be returned from the view.
    data = {"success": False}

    # Ensure an image was properly uploaded to our endpoint.
    if flask.request.method == 'POST':
        if flask.request.content_type.startswith('application/json'):

            ruleEngine = deepcopy(ruleEngine_ori)
            # comment = request.get_json()["content"]
            image = flask.request.json.get('image')
            print(image, '========')

            path_ele = image.replace('\\', '/').replace('//', '/').split('/')
            path_ele.remove('')

            server_ip = path_ele[0]
            if server_ip == '172.20.149.173':
                current_pipline = '17A'
                model = model_cuda_0
            elif server_ip == '172.20.149.176':
                current_pipline = '17B'
                model = model_cuda_1
            else:
                print('error ip:', server_ip)
                return

            img_fullname = '/run/user/1000/gvfs/smb-share:server=' + server_ip + ',share=' + '/'.join(path_ele[1:])

            '/run/user/1000/gvfs/smb-share:server=172.20.149.173,share=halm/PVCTData/2022/2022-9/EL_NG/2022_09_21_15/EL_89.0_21.09.2022-15-16-27_1902122464_126_2.pn'

            '\\172.20.149.176\halm\PVCTData\2022'

            # print(src_path)

            # ================
            # Infer by Pytorch
            # ================

            image_grayscale = cv2.imread(img_fullname, flags=cv2.IMREAD_GRAYSCALE)
            image_grayscale = cv2.resize(image_grayscale, (1024, 1024))
            
            image_bgr = cv2.imread(img_fullname)
            image_bgr = cv2.resize(image_bgr, (1024, 1024))
            result = inference_detector(model, image_bgr)
            defects_info, defects_info_overview = convert_rcnn_result_to_el_rule_condition(
                result=result, 
                category_names=model.CLASSES, 
                image=image_grayscale,
                config=ruleEngine.config
            )

            rule_engine_result = ruleEngine.defect_handle(defects=defects_info)
            rule_engine_result_category = [defects_info[di]['category'] for di in rule_engine_result[1]]
            
            print("Final level:", rule_engine_result[0])
            print("Worst level defect: ", rule_engine_result_category)
            print("Level per defect: ", [(defects_info[i]['category'], ruleEngine.config['defect_level_good_to_bad'][rule_engine_result[2][i]]) 
                for i in range(len(rule_engine_result[2]))], )

            # ===============
            # Calling MES API
            # ===============

            image_name_info = img_fullname.split('_')

            mes_ai_result = None
            if rule_engine_result[0] == "UD":
                mes_ai_result = 2
            elif rule_engine_result[0] == "NG":
                mes_ai_result = 1
            elif rule_engine_result[0] == "OK":
                mes_ai_result = 0

            mes_url = config[current_pipline]['mes_url']  # 'http://172.16.97.154:1230/api/label/halmbin/ai_push'
            mes_header = {'content-type': 'application/json'}
            mes_data = {
                'event': 'halmbin_ai_push',
                'event_time': str(datetime.datetime.now()),
                'data': {
                    'eqp_id': config[current_pipline]['mes_eqp_id'],
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

            data = {'ai2': rule_engine_result[0]}

            try:
                dst_dir = os.path.join(config[current_pipline]['work_dir'], *img_fullname.split('/')[-3:-1], rule_engine_result[0])
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copyfile(img_fullname, os.path.join(dst_dir, img_fullname.split('/')[-1]))
            except Exception as e:
                print(e)

    # Return the data dictionary as a JSON response.
    return flask.jsonify(data)
