import subprocess
import os
import shutil
import cv2
import re
import chardet
import json

from my_work_test import train_values, coco_values, rgb_gray, parse_opt

import ast
import astor  # 用于将 AST 转回源代码

# count = 0

classname_list = []
filename = '/home/ai_data/JW_Yue/mmdetection_8c/configs/htc_/htc_8c/htc_r50_newdata_8c_original.py'


def classnames(annotations_dir):
    classnames_dir = os.path.join(annotations_dir, 'classinfor.json')
    with open(classnames_dir, 'rb') as ff:
        detect = chardet.detect(ff.read())
        thisencoding = detect['encoding']
        # print(thisencoding)
    if thisencoding == 'utf-8':
        with open(classnames_dir, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # print(data)
    else:
        with open(classnames_dir, 'r', encoding='gbk') as f:
            data = json.load(f)
    classname_dict = data["classorder"][0]
    classname_list = list(classname_dict.values())

    return classname_list


# 修改配置中的指定内容
# def modify_config(config, ann_file, traindatapath, segm_dir, work_dir, num_classes):
#     # 修改指定内容
#     img_prefix = os.path.join(traindatapath, "train")
#     # print(ann_file)
#     # print(img_prefix)
#     # print(segm_dir)
#     # print(work_dir)
#     config['data']['train']['ann_file'] = ann_file
#     config['data']['train']['img_prefix'] = img_prefix
#     config['data']['train']['seg_prefix'] = segm_dir
#     config['data']['val']['ann_file'] = ann_file
#     config['data']['val']['img_prefix'] = img_prefix
#     config['data']['test']['ann_file'] = ann_file
#     config['data']['test']['img_prefix'] = img_prefix
#     config['work_dir'] = work_dir
#     config['model']['roi_head']['bbox_head'][0]['num_classes'] = num_classes
#     config['model']['roi_head']['bbox_head'][1]['num_classes'] = num_classes
#     config['model']['roi_head']['bbox_head'][2]['num_classes'] = num_classes
#     config['model']['roi_head']['mask_head'][0]['num_classes'] = num_classes
#     config['model']['roi_head']['mask_head'][1]['num_classes'] = num_classes
#     config['model']['roi_head']['mask_head'][2]['num_classes'] = num_classes
#     # print(config['data']['train']['ann_file'])
#     # print(config['data']['train']['img_prefix'])
#     # print(config['data']['train']['seg_prefix'])
#     # print(config['data']['val']['ann_file'])
#     # print(config['data']['val']['img_prefix'])
#     # print(config['data']['test']['ann_file'])
#     # print(config['data']['test']['img_prefix'])
#     # print(config['work_dir'])
#     # print(config['model']['roi_head']['bbox_head'][0]['num_classes'])
#     # print(config['model']['roi_head']['bbox_head'][1]['num_classes'])
#     # print(config['model']['roi_head']['bbox_head'][2]['num_classes'])
#     # print(config['model']['roi_head']['mask_head'][0]['num_classes'])
#     # print(config['model']['roi_head']['mask_head'][1]['num_classes'])
#     # print(config['model']['roi_head']['mask_head'][2]['num_classes'])
#
#     # 修改其他指定内容
#     # config['data']['samples_per_gpu'] = 16  # 例如修改每个GPU的样本数量
#
#     return config

def replace_line_in_file(file_path, train_key, model_key, num_classes):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(file_path, "w", encoding="utf-8") as file:
        for line in lines:
            if 'num_classes=0' in line:
                line = line.replace('num_classes=0', num_classes)
            elif 'data_original' in line:
                line = line.replace('data_original', train_key)
            elif 'htc_r50_newdata_8c_original' in line:
                line = line.replace('htc_r50_newdata_8c_original', model_key)
            file.write(line)


def revise_train(traindatapath, check_out, annotations_dir, ann_file, segm_dir, work_dir):
    # 统计缺陷个数
    classname_list = classnames(annotations_dir=annotations_dir)
    # print('缺陷数目', classname_list)

    num_classes = 'num_classes=' + str(len(classname_list))
    print('分类数目：', num_classes)

    new_filename = check_out + '/htc_r50_newdata_8c_' + traindatapath.split('/')[-1].replace('data', '') + '.py'
    new_file = 'htc_r50_newdata_8c_' + traindatapath.split('/')[-1].replace('data', '') + '.py'
    # work_dir = work_dir + '/htc_r50_newdata_5c_' + traindatapath.split('/')[-1].replace('data', '')
    model_key = 'htc_r50_newdata_8c_' + traindatapath.split('/')[-1].replace('data', '')
    shutil.copyfile(filename, new_filename)

    print('复制初始文件：{} 为一个新文件：{}'.format(filename.split('/')[-1], new_filename.split('/')[-1]))
    replace_line_in_file(new_filename, traindatapath.split('/')[-1], model_key, num_classes)

    print('当前训练所需的py文件已经修改完成,\n文件是路径是 {} \n文件是        {}'.format(new_filename, new_file))
    #
    # cc = "source /home/KW_Zhang/anaconda3/etc/profile.d/conda.sh && conda info --envs && " \
    #     #      "conda activate open_solov2_new && CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 " \
    #     #      "echo nohup bash /home/ai_data/KWZhang_workingspace/open_solov2_new/mmdetection/tools/dist_train.sh " \
    #     #      + new_filename + " 8 &"
    #     #
    #     # print('cc', cc)
    #     # fname, fename = os.path.splitext(new_file)
    #     # #
    #     # new_txt = "/home/ai_data/JW_Yue/my_work" + fname + '.txt'
    #     # with open(new_txt, 'w') as f:
    #     #     f.write(cc)
    #     # train_name = fname + '.sh'
    #     # new_sh = "/home/ai_data/JW_Yue/my_work" + train_name
    #     # os.rename(new_txt, new_sh)
    #     # chmod_sh = "chmod +x /home/ai_data/JW_Yue/my_work" + train_name
    #     # call_sh = "/home/ai_data/JW_Yue/my_work" + train_name
    #     # subprocess.call(chmod_sh, shell=True)
    #     # subprocess.call(call_sh, shell=True)
    #
    # # my_system = "CUDA_VISIBLE_DEVICES=0,1,2,3,4,5 bash /home/ai_data/KWZhang_workingspace/open_solov2_new/mmdetection/tools/dist_train.sh /home/ai_data/KWZhang_workingspace/open_solov2_new/mmdetection/configs/ZHUHAI/" + new_filename[78:] +" 6 "
    # my_system = "bash /home/ai_data/KWZhang_workingspace/open_solov2_new/mmdetection/tools/dist_train.sh /home/ai_data/KWZhang_workingspace/open_solov2_new/mmdetection/configs/ZHUHAI/" + new_filename[78:] + " 8 "
    # print('my_system:', my_system)
    # os.system(my_system)
    my_system = "nohup bash /home/ai_data/JW_Yue/mmdetection_8c/tools/dist_train.sh " + new_filename + " 8 &"
    print('my_system:', my_system)
    os.system(my_system)


if __name__ == '__main__':
    traindatapath, check_out, annotations_dir = train_values()
    ann_file, pngFolder = coco_values()
    pngFolder, segm_dir = rgb_gray()
    opts = parse_opt()
    work_dir = opts.modelpath
    revise_train(traindatapath=traindatapath, check_out=check_out, annotations_dir=annotations_dir, ann_file=ann_file, segm_dir=segm_dir, work_dir=work_dir)
