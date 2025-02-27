import os
import time
import numpy as np
import datetime
import shutil
import re
import argparse
import torch


def parse_opt():
    # parse = argparse.ArgumentParser()
    # # 样本存放路径
    # parse.add_argument('--traindatapath', type=str, help='', default='/home/Data/JW_Yue/mmdetection/data/data20240907')
    # # parse.add_argument('--rootpath', type=str, help='', default='/home/Data/JW_Yue/mmdetection/data/data20240907')
    # parse.add_argument('--modelpath', type=str, help='', default='/home/Data/JW_Yue/mmdetection/work_dir_5c')
    # # 模型配置文件存放路径
    # parse.add_argument('--check_out', type=str, help='', default='/home/ai_data/JW_Yue/mmdetection/configs/htc_/htc_5c')
    # parse.add_argument('--ann_file', type=str, help='', default='')
    # parse.add_argument('--pngFolder', type=str, help='', default='')
    # parse.add_argument('--segm_dir', type=str, help='', default='66')
    # parse.add_argument('--annotations_dir', type=str, help='', default='')
    # args = parse.parse_args()
    args = argparse.Namespace()
    # 样本存放路径
    args.traindatapath = '/home/Data/JW_Yue/mmdetection/data_8c/data20241021'
    # 模型存放路径
    args.modelpath = '/home/Data/JW_Yue/mmdetection/work_dir_8c'
    # 配置文件存放路径
    args.check_out = '/home/ai_data/JW_Yue/mmdetection_8c/configs/htc_/htc_8c'
    return args


def split_png_json():
    opts = parse_opt()
    traindatapath = opts.traindatapath
    return traindatapath


# def labelmetococo_values():
#     opts = parse_opt()
#     traindatapath = opts.traindatapath
#     rootpath = opts.rootpath
#     modelpath = opts.modelpath
#     return traindatapath, rootpath, modelpath

def labelmetococo_values():
    opts = parse_opt()
    traindatapath = opts.traindatapath
    # rootpath = opts.rootpath
    # modelpath = opts.modelpath
    return traindatapath


def coco_values():
    opts = parse_opt()
    traindatapath = opts.traindatapath
    ann_file = os.path.join(traindatapath, 'annotations/instances_train2017.json')
    pngFolder = os.path.join(traindatapath, 'export_png')
    return ann_file, pngFolder


def rgb_gray():
    opts = parse_opt()
    traindatapath = opts.traindatapath
    pngFolder = os.path.join(traindatapath, 'export_png')
    segm_dir = os.path.join(traindatapath, 'stuffthingmaps/')
    return pngFolder, segm_dir


def train_values():
    opts = parse_opt()
    traindatapath = opts.traindatapath
    check_out = opts.check_out
    # traindatapath = '/home/Data/JW_Yue/mmdetection/data/data20240907'
    # check_out = '/home/ai_data/JW_Yue/mmdetection/configs/htc_/htc_5c'
    annotations_dir = os.path.join(traindatapath, 'annotations')

    return traindatapath, check_out, annotations_dir


def main():
    torch.autograd.set_detect_anomaly(True)
    # opts = parse_opt()
    # traindatapath = opts.traindatapath
    # rootpath = opts.rootpath
    # modelpath = opts.modelpath
    # check_out = opts.check_out
    # ann_file = os.path.join(traindatapath, 'annotations/instances_train2017.json')
    # pngFolder = traindatapath = opts.traindatapath
    # segm_dir = os.path.join(traindatapath, 'stuffthingmaps/')
    # print('--------执行首步 区分图片和json-------')
    # os.system('{} {}'.format('python', '/home/ai_data/KWZhang_workingspace/open_solov2_new/my_work/sftp_database.py'))

    print('--------执行第一步 转格式--------')
    # os.system('{} {}'.format('python', '/home/ai_data/JW_Yue/my_work_8c/labelmetococo_halmywsc.py'))  # 直接调用  转格式labelme_coco 其中不包含训练集和验证集

    print('--------执行第二步 获取掩码-------')
    # os.system('{} {}'.format('python', '/home/ai_data/JW_Yue/my_work_8c/my_pycoco.py'))  # 直接调用 掩码图的获取（三通道）

    print('--------执行第三步 转灰度图像--------')
    # os.system('{} {}'.format('python', '/home/ai_data/JW_Yue/my_work_8c/rgb2gray.py'))  # 直接调用  掩码图的转化（三通道） 转换为 单通道

    print('--------执行第四步 创建并修改配置文件并开始训练--------')
    #os.remove('/home/ai_data/JW_Yue/my_work_5c/nohup.out')
    os.system('{} {}'.format('python', '/home/ai_data/JW_Yue/my_work_8c/my_train.py'))  # 直接调用 训练所需要文件的创建 修改内容(包括数据集的路径,coco.py和classnames.py的内容，num_classes,以及模型的保存路径)

    print('---------执行第五步 监控训练日志---------------------')
    os.system('{}'.format('tail -f /home/ai_data/JW_Yue/my_work_8c/nohup.out'))
    # 暂时和第四部写到一起 之后在考虑分开


if __name__ == '__main__':
    main()
