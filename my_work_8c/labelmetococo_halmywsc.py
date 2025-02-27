# -*- coding:utf-8 -*-
# !/usr/bin/env python

import argparse, math
import json, os, shutil
import matplotlib.pyplot as plt
import skimage.io as io
import cv2, time
# from labelme import utils
import numpy as np
import glob, math
import PIL
import traceback
import xml.etree.ElementTree as ET


def xmlclass():
    print('正在解析 annotation files')
    # print(0)
    rootdir = "/home/ai1/IMG_DATA/HALM/HALM_5BB/v5.13/"
    imgdir = os.path.join(rootdir, "JPEGImages")

    inputimgdir = "/home/ai1/IMG_DATA/HALM/HALM_5BB/v5.13/Annotations/"
    classdic = {}
    annots = [os.path.join(inputimgdir, s) for s in os.listdir(inputimgdir)]  # 训练样本的xml路径
    idx = 0
    # print(1)
    for annot in annots:
        # try:

        """依次解析XML文件"""
        idx += 1
        print("idx", idx)
        filename1 = annot.split('/')[-1]
        filepath = os.path.join(inputimgdir, annot)
        # print()
        aa, bb = os.path.splitext(filename1)
        print(annot)
        print("a", a)

        # str_xml = open(annot, 'r').read()

        # 将字符串解析成xml特殊对象，root代指xml文件的根节点
        # element = ET.XML(str_xml)
        et = ET.parse(annot)
        a, b = os.path.splitext(filename1)
        # imagedir = 'F:/image/0311/v3.12/ds/JPEGImages/'
        annotpath = os.path.join(imgdir, aa + '.png')
        print("annotpath", annotpath)
        # et =ET.fromstring(open(annot).read())
        element = et.getroot()
        # print("1111111111111111")
        # try:
        element_objs = element.findall('object')
        # print("element_objs", element_objs)
        # except Exception as e:
        # print("b奥错",e)

        for element_obj in element_objs:
            class_name = element_obj.find('name').text
            print("class_name", class_name)
            if class_name not in classdic:
                classdic[class_name] = 1
            else:
                classdic[class_name] += 1
            outputdir = os.path.join(rootdir, "5bbclass" + "/" + class_name)
            if not os.path.exists(outputdir):
                os.makedirs(outputdir)
            outputpth = os.path.join(outputdir, aa + ".xml")
            outputimgpath = os.path.join(outputdir, aa + ".png")
            if not os.path.exists(outputpth):
                shutil.copyfile(annot, outputpth)
            if not os.path.exists(outputimgpath):
                shutil.copyfile(annotpath, outputimgpath)
            print("imgname:", aa)
        # except Exception as e:
        #     print("e", e)
    print("classdic", classdic)


def classtojson(annotationsdir):
    jsonfiledir = os.path.join(annotationsdir, "instances_train2017.json")
    # classinforfiledir = os.path.join(annotationsdir, "classinfortj.json")
    classdicts = {}
    print('写入文件')
    with open(jsonfiledir, 'r') as f:
        data = json.load(f)
        categories = data["categories"]
        for classdict in categories:
            id = classdict["id"]
            name = classdict["name"]
            classdicts[id] = name
        print(classdicts)
        datat = {}
    classlist = []
    datat["classorder"] = classlist
    classlist.append(classdicts)
    # if os.path.exists(classinforfiledir):
    #     with open(classinforfiledir, 'r') as ft:
    #         with open(classinforfiledir, 'w') as f:
    #             json.dump(datat, f, indent=2, ensure_ascii=False)
    #
    # else:
    #     with open(classinforfiledir, 'w') as f:
    #         json.dump(datat, f, indent=2, ensure_ascii=False)
    return classlist


def tiaoxuanimg(input_img, input_json, picdir, oldjsondir, x1, bias):
    rz = " 挑选图片开始——————————————————————————————" + "\n\n"
    rz = rz + "input_img: " + input_img + "\n"
    rz = rz + "input_json: " + input_json + "\n"
    rz = rz + "x1: " + str(x1) + "\n"
    rz = rz + "bias: " + str(bias) + "\n"
    logdir = annotationsdir + '/' + txtname + '.txt'
    txt = open(logdir, 'a+')
    txt.write(rz)
    txt.close()

    inputlist = os.listdir(input_json)
    leninput = len(inputlist) // 2
    a, b = os.path.splitext(inputlist[0])
    classname = a[:-6]
    print("classname", classname)
    # classname = a.split("_")[0]

    cnt = 0
    for i in range(0, 1890000):
        if i % x1 == bias:
            a = classname + "_" + str(i).zfill(5)
            if os.path.exists(os.path.join(input_json, a + '.json')):

                # cnt += 1
                if os.path.exists(os.path.join(input_img, a + '.jpg')):
                    rz = "被挑选出图片名: " + a + "\n"
                    print("a,a", a)
                    inputimg = os.path.join(input_img, a + '.jpg')
                    inputjson = os.path.join(input_json, a + '.json')
                    outputimg = os.path.join(picdir, a + '.jpg')
                    outputjson = os.path.join(oldjsondir, a + '.json')
                    shutil.copyfile(inputimg, outputimg)
                    shutil.copyfile(inputjson, outputjson)
                    cnt = cnt + 1
                    logdir = annotationsdir + '/' + txtname + '.txt'
                    txt = open(logdir, 'a+')
                    txt.write(rz)
                    txt.close()

    rz = "被挑选图片数：" + str(cnt) + "\n"
    txt = open(logdir, 'a+')
    txt.write(rz)
    txt.close()
    print("input_img: ", input_img)
    print("input_json: ", input_json)
    print("cnt: ", cnt)

    # imglist = []
    # for file in inputlist:
    #     aa,bb = os.path.splitext(file)
    #     if bb == ".jpg":
    #         print("aa",aa)
    #         imglist.append(file)
    # for i in range(leninput):
    #     a,b = os.path.splitext(imglist[1])
    #     classname,num = a.split("_")[0]
    #
    #     if i % x1 == 0:
    #         #print("i",x1,i)
    #         a = classname + "_" + str(i).zfill(5)
    #         print("a",a)


def splitclass(json_path, rootdir):
    # json_path = "/home/ai1/IMG_DATA/HALM/HALM_5BB/v5.13/Annotations/"
    classdic = {}
    for file in os.listdir(json_path):
        filepath = os.path.join(json_path, file)
        aa, bb = os.path.splitext(file)
        # print(filepath)
        # rootdir = "/home/ai1/IMG_DATA/HALM/HALM_5BB/v5.13/"
        # output = "F:\GP\image\coco_back0529\\xdsjson"
        inputimg = rootdir + "/train"
        inputimgpath = os.path.join(inputimg, aa + ".png")

        # print()

        with open(filepath, 'r') as f:
            # with open(filepath, 'r', encoding='utf-8') as f:
            # encoding='GB2312'

            data = json.load(f)
            # data = data1
            # print(data)
            # print(type(data))
            imgdata = data["shapes"]
            # data["imagePath"] = a + '.png'
            # print("1111111111111111111111111111111111")
            # print(imgdata)
            hbcount = 0
            if imgdata:  # 如果shapes内有元素
                for label in imgdata:

                    class_name = label["label"]
                    print("class_name", class_name)
                    if class_name not in classdic:
                        classdic[class_name] = 1
                    else:
                        classdic[class_name] += 1

                    output = rootdir + "/class/" + class_name
                    if not os.path.exists(output):
                        os.makedirs(output)
                    outputpth = os.path.join(output, file)
                    outputimgpath = os.path.join(output, aa + ".png")
                    shutil.copyfile(filepath, outputpth)
                    shutil.copyfile(inputimgpath, outputimgpath)
                    print("imgname:", aa)
    print("classdic:", classdic)


def dellabel(json_path):
    for file in os.listdir(json_path):
        filepath = os.path.join(json_path, file)
        aa, bb = os.path.splitext(file)
        # print(filepath)
        rootdir = "F:\\GP\\image\\gp_back\\"
        # output = "F:\GP\image\coco_back0529\\xdsjson"
        inputimg = root + "train"
        inputimgpath = os.path.join(inputimg, aa + ".png")
        outputimgpath = os.path.join(output, aa + ".png")
        # print()

        outputpth = os.path.join(output, file)
        with open(filepath, 'r') as f:
            # with codecs.open(filepath, 'r', 'utf-8') as f:
            # encoding='GB2312'

            data = json.load(f)
            # data = data1
            # print(data)
            # print(type(data))
            imgdata = data["shapes"]
            # data["imagePath"] = a + '.png'
            # print("1111111111111111111111111111111111")
            # print(imgdata)
            hbcount = 0
            if imgdata:  # 如果shapes内有元素
                for label in imgdata:

                    class_name = label["label"]
                    print("class_name, class_name", class_name)
                    if class_name == "XDS":
                        hbcount += 1
            if hbcount == 0:
                print("shanchu")
            else:
                shutil.copyfile(filepath, outputpth)
                shutil.copyfile(inputimgpath, outputimgpath)


def show_old(annotationsdir, json_path):
    # path是你存放json的路径 手动创建
    rz = "统计故障数量开始：" + "\n\n\n"
    rz = rz + "annotationsdir:" + annotationsdir + "\n"
    rz = rz + "json_path:" + json_path + "\n"
    print(rz)

    txt = open(logdir, 'a+')
    txt.write(rz)
    txt.close()
    cnt = 0

    # json_file = os.listdir(json_path)

    classes_count = {}  # 标签种类和数量
    new_classes_count = {}  # 清洗后标签种类和数量
    last_classes_count = {}  # 标签种类和数量
    floog = 0
    ttmp = 0

    # os.system("python C:\\Users\\bigbox\\Anaconda3\\envs\\labelme\\Scripts\\labelme_json_to_dataset.exe %s" %(path))
    if floog == 0:
        # for root, dirs, json_file in os.walk(json_path):
        print("json_path", json_path)
        json_file = os.listdir(json_path)
        # print("json_file", json_file)
        for file in json_file:
            # print(file)
            a, b = os.path.splitext(file)
            # print(a)

            if b == ".json":

                filepath = os.path.join(json_path, file)
                print("filepath;", cnt, filepath)
                rz = "图片名" + filepath + "\n"
                txt = open(logdir, 'a+')
                txt.write(rz)
                txt.close()

                labelNUM = 0
                labelcount = {}
                after = []
                ordershape = {}
                shapelist = []
                arealist = []
                try:
                    with open(filepath, 'r', encoding='UTF-8') as f:
                        # with codecs.open(filepath, 'r', 'utf-8') as f:
                        # encoding='GB2312'

                        data = json.load(f)
                        # data = data1
                        # print(data)
                        # print(type(data))
                        imgdata = data["shapes"]
                        # data["imagePath"] = a + '.png'
                        # print(imgdata)
                        if imgdata:  # 如果shapes内有元素
                            cnt += 1
                            for label in imgdata:
                                class_name = label["label"]
                                # if class_name == "不明确故障":
                                #     aaa = filepath
                                # print("class_name", class_name)
                                if class_name not in classes_count:
                                    """统计每种类型出现次数"""
                                    classes_count[class_name] = 1
                                else:
                                    classes_count[class_name] += 1
                except:
                    # ttmp += 1
                    pass
                    try:
                        with open(filepath, 'r', encoding='GB2312') as f:
                            # with codecs.open(filepath, 'r', 'utf-8') as f:
                            # encoding='GB2312'

                            data = json.load(f)
                            # data = data1
                            # print(data)
                            # print(type(data))
                            imgdata = data["shapes"]
                            # data["imagePath"] = a + '.png'
                            # print(imgdata)
                            if imgdata:  # 如果shapes内有元素
                                cnt += 1
                                for label in imgdata:
                                    class_name = label["label"]
                                    # if class_name == "不明确故障":
                                    #     aaa = filepath
                                    # print("class_name", class_name)
                                    if class_name not in classes_count:
                                        """统计每种类型出现次数"""
                                        classes_count[class_name] = 1
                                    else:
                                        classes_count[class_name] += 1
                    except:
                        # ttmp += 1
                        pass
                        try:
                            with open(filepath, 'r', encoding='GBK') as f:
                                # with codecs.open(filepath, 'r', 'utf-8') as f:
                                # encoding='GB2312'

                                data = json.load(f)
                                # data = data1
                                # print(data)
                                # print(type(data))
                                imgdata = data["shapes"]
                                # data["imagePath"] = a + '.png'
                                # print(imgdata)
                                if imgdata:  # 如果shapes内有元素
                                    cnt += 1
                                    for label in imgdata:
                                        class_name = label["label"]
                                        # if class_name == "不明确故障":
                                        #     aaa = filepath
                                        # print("class_name", class_name)
                                        if class_name not in classes_count:
                                            """统计每种类型出现次数"""
                                            classes_count[class_name] = 1
                                        else:
                                            classes_count[class_name] += 1
                        except:
                            ttmp += 1
                            pass

    print(classes_count)
    print(ttmp)
    dist11 = {}
    list11 = []
    # timea = str(time.time())
    dist11["classcount"] = list11
    list11.append(classes_count)
    rz = "classes_count" + str(classes_count) + "\n"
    txt = open(logdir, 'a+', encoding='UTF-8')
    txt.write(rz)
    txt.close()
    # # data = json.dumps(classes_count,indent=4, ensure_ascii=False)
    # print("dist11",dist11)
    # print(aaa)
    with open(os.path.join(annotationsdir, "classinfor.json"), "w", encoding='UTF-8') as f:
        json.dump(dist11, f, indent=2, ensure_ascii=False)
        # f.write(data)
    # print(last_classes_count)
    # print(classes_count)


def show(annotationsdir, json_path, classlist):
    # path是你存放json的路径 手动创建
    rz = "统计故障数量开始：" + "\n\n\n"
    rz = rz + "annotationsdir:" + annotationsdir + "\n"
    rz = rz + "json_path:" + json_path + "\n"
    print(rz)

    txt = open(logdir, 'a+')
    txt.write(rz)
    txt.close()
    cnt = 0

    # json_file = os.listdir(json_path)

    classes_count = {}  # 标签种类和数量
    new_classes_count = {}  # 清洗后标签种类和数量
    last_classes_count = {}  # 标签种类和数量
    floog = 0

    # os.system("python C:\\Users\\bigbox\\Anaconda3\\envs\\labelme\\Scripts\\labelme_json_to_dataset.exe %s" %(path))
    if floog == 0:
        # for root, dirs, json_file in os.walk(json_path):
        print("json_path", json_path)
        json_file = os.listdir(json_path)
        # print("json_file", json_file)
        for file in json_file:
            # print(file)
            a, b = os.path.splitext(file)
            # print(a)

            if b == ".json":

                filepath = os.path.join(json_path, file)
                # print("filepath;", cnt, filepath)
                rz = "图片名" + filepath + "\n"
                txt = open(logdir, 'a+')
                txt.write(rz)
                txt.close()

                labelNUM = 0
                labelcount = {}
                after = []
                ordershape = {}
                shapelist = []
                arealist = []
                with open(filepath, 'r') as f:
                    # with codecs.open(filepath, 'r', 'utf-8') as f:
                    # encoding='GB2312'
                    try:
                        data = json.load(f)
                        # data = data1
                        # print(data)
                        # print(type(data))
                        imgdata = data["shapes"]
                        # data["imagePath"] = a + '.png'
                        # print(imgdata)
                        if imgdata:  # 如果shapes内有元素
                            cnt += 1
                            for label in imgdata:
                                class_name = label["label"]
                                # print("class_name", class_name)
                                if class_name not in classes_count:
                                    """统计每种类型出现次数"""
                                    classes_count[class_name] = 1
                                else:
                                    classes_count[class_name] += 1
                    except:
                        pass

    print(classes_count)
    dist11 = {}
    list11 = []
    # timea = str(time.time())
    dist11["classcount"] = list11
    dist11['classorder'] = classlist
    list11.append(classes_count)
    rz = "classes_count" + str(classes_count) + "\n"
    txt = open(logdir, 'a+')
    txt.write(rz)
    txt.close()
    # # data = json.dumps(classes_count,indent=4, ensure_ascii=False)
    # print("dist11",dist11)
    with open(os.path.join(annotationsdir, "classinfor.json"), "w") as f:
        json.dump(dist11, f, indent=2, ensure_ascii=False)
        # f.write(data)
    # print(last_classes_count)
    # print(classes_count)


def splitjson_img(file_dir, ROOT_DIR):
    # 将file_dir文件夹内所有文件按png和json格式的不同分别放到ROOT_DIR的pic文件夹和oldjson文件夹
    json_path = ROOT_DIR + '/' + 'oldjson/'
    pic_path = ROOT_DIR + '/' + 'pic/'
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)

    img = []
    json = []
    # for root, dirs, files in os.walk(file_dir):
    while True:
        for file in os.listdir(file_dir):  # files:
            root = file_dir
            print("file;", file)
            a, b = os.path.splitext(file)
            if b == '.png':  # os.path.splitext(file)[1] == '.jpg' or
                oldimgpath = os.path.join(root, file)

                pic_imgpath = os.path.join(pic_path, file)
                shutil.move(oldimgpath, pic_imgpath)
            if b == '.jpg':
                oldimgpath = os.path.join(root, file)
                pic_imgpath = os.path.join(pic_path, a + ".jpg")
                shutil.move(oldimgpath, pic_imgpath)
            elif b == '.json':
                oldjisonpath = os.path.join(root, file)
                jsonpath = os.path.join(json_path, file)
                shutil.move(oldjisonpath, jsonpath)


def label_clean(labellist, label, labelcount, last_classes_count):
    # labellist为故障可能的名字
    # labelNUM为一张图片中某故障的排序
    # 为json文件中的字典
    # last_classes_count为故障字典
    # print("label,", label["label"])

    for i in range(len(labellist)):
        new_class_name = labellist[0]
        if label["label"] == labellist[i]:
            # label["label"] = new_class_name + str(labelNUM)
            # labelNUM += 1

            if new_class_name not in labelcount:
                # 统计每种类型出现次数
                labelcount[new_class_name] = 1
            else:
                labelcount[new_class_name] += 1
            label["label"] = new_class_name
            print("label ", label["label"], labelcount[new_class_name])

            if new_class_name not in last_classes_count:
                # 统计每种类型出现次数
                last_classes_count[new_class_name] = 1
            else:
                last_classes_count[new_class_name] += 1
    # return last_classes_count


def compute_polygon_area(points):
    point_num = len(points)
    if (point_num < 3): return 0.0
    s = points[0][1] * (points[point_num - 1][0] - points[1][0])
    # for i in range(point_num): # (int i = 1 i < point_num ++i):
    for i in range(1, point_num):  # 有小伙伴发现一个bug，这里做了修改，但是没有测试，需要使用的亲请测试下，以免结果不正确。
        s += points[i][1] * (points[i - 1][0] - points[(i + 1) % point_num][0])
    return abs(s / 2.0)


def train_data(path, rootpath, labelalllist):
    rz = "清洗标签开始：" + "\n\n"
    # json_path = path + '/oldjson/'  # path是你存放json的路径 手动创建
    # #out_json_path = jsondir
    # imgdir = path + '/pic/'
    json_path = oldjsondir  # path是你存放json的路径 手动创建
    imgdir = picdir
    txtpath = path + 'dataclass.txt'
    out_json_path = os.path.join(rootpath, "json")
    out_img_path = os.path.join(rootpath, "train")
    # if not os.path.exists(out_json_path):
    # os.makedirs(out_json_path)
    json_file = os.listdir(json_path)
    rz = rz + "json_path：" + json_path + "\n"
    rz = rz + "txtpath：" + txtpath + "\n"
    rz = rz + "out_json_path：" + out_json_path + "\n"
    rz = rz + "out_img_path：" + out_img_path + "\n"
    txt = open(logdir, 'a+')
    txt.write(rz)
    txt.close()

    # labelme_json文件夹创建

    # if not os.path.exists(labelme_json_dst):
    # os.makedirs(labelme_json_dst)
    # cv2_mask文件夹创建
    # if not os.path.exists(path + 'cv2_mask'):
    # os.makedirs(path + 'cv2_mask')
    # print(json_file)
    classes_count = {}  # 标签种类和数量
    new_classes_count = {}
    last_classes_count = {}  # 标签种类和数量
    last_classeslist_count = {}  # 清洗后标签种类和数量
    cnnt = 0

    # labelalllist = [['偏移', '偏移1', '印刷偏移'],  # 1
    #                 ['其他划伤', '其它划伤', '未知划伤', '其它划伤、'],  # 2
    #                 ['卡点烧伤', '卡点过烧'],  # 3
    #                 ['手指印'],  # 4
    #                 ['叠插划伤'],  # 5
    #                 ['连续断栅', '密集断栅', '背场缺失'],  # 6
    #                 ['黑点'],  # 7
    #                 ['花篮印', '花篮'],  # 8
    #                 ['雾状发黑', '雾状', '小雾状', '大雾状'],  # 10
    #                 ['气流片'],  # 11
    #                 ['黑斑'],  # 12
    #                 ['过刻', '过客', '过客、', '四角发黑'],  # 13
    #                 ['黑边', '黑边1', '小黑边', '大黑边', '边缘少刻', '边缘过刻'],  # 14
    #                 ['堵片划伤', '堵片划伤1', '部分叠片划伤', '单片卡片划伤', '满面划伤', '堵片满面划伤', '掉堵片划伤', '卡堵片划伤', '赌片划伤', '掉片漏吸'],  # 15
    #                 ['直线划伤', '一字划伤', '丝网直线划伤', '丝网直线'],  # 16
    #                 ['花篮划伤'],  # 17
    #                 ['断栅'],  # 18
    #                 ['石墨舟划痕', '石墨舟划伤', '石墨舟', '石磨舟划伤'],  # 19
    #                 ['卡点印'],  # 20
    #                 ['舟框印'],  # 21
    #                 ['退火/扩散吸盘印', '扩散吸盘印', '退火吸盘印', '吸盘印'],  # 22
    #                 ['水印', 'ˮӡ'],  # 23
    #                 ['炉后划伤', '炉后无规则划伤', '炉后划伤、', '炉后无规则游戏划伤'],  # 24
    #                 ['麻点'],  # 25
    #                 ['顶针印'],  # 26
    #                 ['同心圆'],  # 27
    #                 ['星形隐裂', '星型隐裂'],  # 28
    #                 ['退火划伤', '退火满面划伤'],  # 29
    #                 ['线痕划伤'],  # 30
    #                 ['掉片曲线划伤', '掉线曲线划伤', '曲线掉线划伤', '掉片曲线', '掉线曲线', '堵片曲线划伤', '掉片划伤'],  # 31
    #                 ['边缘隐裂', '倒角隐裂', '隐裂', '碎片'],  # 32
    #                 ['滚轮印'],  # 33
    #                 ['暗片'],  # 34
    #                 ['吸笔印'],  # 35
    #                 ['伸缩舌头划伤', '舌头划伤', '伸缩舌头'],  # 36
    #                 ['工装黑印', '舟齿印', '底杆印', '带水烧伤', '舟齿', '夹持印'],  # 37
    #                 ['镀膜吸盘印', 'PE吸盘印'],  # 38
    #                 ['石墨舟两边', '石墨舟划伤两边'],  # 39
    #                 ['皮带印'],  # 40
    #                 ['顶齿划伤'],  # 41
    #                 ['刻蚀缓存划伤'],  # 42
    #                 ['花篮齿印'],  # 43
    #                 ]

    # labelalllist = [['PY', '偏移', '偏移1', '印刷偏移'],
    #                 ['SMZHS', 'SMZHH', '石墨舟划伤'],
    #                 ['LXDS', '连续断栅', '密集断栅', '背场缺失'],
    #                 ['HD', '黑点'],
    #                 ['BCGS', '背场过烧', '背极发黑', '背电极发黑', '过烧'],
    #                 ['WZFH', '雾状发黑', '雾状', '小雾状', '大雾状'],
    #                 ['QLP', '气流片'],
    #                 ['LX', '亮线'],
    #                 ['HBN', '黑斑'],
    #                 ['GK', '过刻', '过客', '过客、', '四角发黑'],
    #                 ['HB', '黑边', '黑边1', '小黑边', '大黑边', '边缘少刻', '边缘过刻'],
    #                 ['DS', '断栅'],
    #                 # ['LXDS', '连续断栅'],
    #                 ['LXHS', '连续划伤', 'SMZLB', 'DCHAHS'],
    #                 ['KDY', '卡点印'],
    #                 ['ZKY', '舟框印'],
    #                 ['SY', '水印', 'ˮӡ'],
    #                 ['MD', '麻点'],
    #                 ['TXY', '同心圆'],
    #                 ['GLY', '滚轮印'],
    #                 ['YL', 'XXYL', '星形隐裂', '星型隐裂', 'BYYL', '边缘隐裂', '倒角隐裂', '隐裂', '碎片'],
    #                 ['ZCY', '工装黑印', '底杆印', '舟齿印', '舟齿', '带水烧伤', '夹持印', 'GZHY', 'GZHY1', 'HLCY', '花篮齿印', '顶针印'],  # 42
    #                 ['PDY', '皮带印'],
    #                 ['YK', '印宽'],
    #                 ['ZSDS', '主栅断栅'],
    #                 ["HS", '划痕', 'HH', '划伤', 'LHHS', 'QTHS', 'ZXHS'],
    #                 ["XPY", "吸盘印"],
    #                 ["BDJFH", '背电极发黑'],
    #                 ["BJFH", '边角发黑'],
    #                 ["DJPY", "搭接偏移"],
    #                 ["PDY1", '皮带印1'],
    #                 ["HJ", '黑角'],
    #                 ["QHB", '浅黑边'],
    #                 ["WR", '污染'],
    #                 ["HX", '黑线'],
    #                 ["CXYC", '成像异常'],
    #                 ["ZSYH", '主栅印厚'],
    #                 ["BJPY", '边角偏移']
    #                 # ['YCKDS', '鱼叉口断栅']
    #                 ]

    # labelalllist = [['PY','印刷偏移'],  # 1
    #                 ['DS','LXDS','搭接不良','过主栅断栅','断栅','连续断栅'],  # 2
    #                 ['GK','过刻'],  # 3
    #                 ['HH','QTHS','SMZHH','DPQXHS', 'LHHS','ZXHS','HLHS','DCHIHS','XHHS','划痕','划伤'],  # 4
    #                 ['LXHH','SMZLB','DPHS','THHS', 'DCHAHS','SSSTHS','连续划痕'],  # 5
    #                 ['HB','四角发黑','浅黑边','黑边'],  # 6
    #                 ['TXY'],  # 7
    #                 ['SY','水印手指印'],  # 8
    #                 ['AP'],  # 9
    #                 ['BCGS','烧结异常'],  # 10
    #                 ['DZY','顶针印'],  # 11
    #                 ['HBN','BGZHB','HBN','黑斑'],  # 12
    #                 ['HD','黑斑黑点'],
    #                 ['HLCY','花篮齿印'], # 13
    #                 ['KDSS'],  # 14
    #                 ['KDY','卡点印'],  # 15
    #                 ['PDYGLY','PDY','GLY','皮带印滚轮印','滚轮印'],  # 16
    #                 ['QLP'],  # 18
    #                 ['SZY','手指印'],  # 19
    #                 ['WZFH','雾状发黑'],  # 20
    #                 ['XPY','THXPY','DMXPY'],  # 21
    #                 ['YL','XXYL','BYYL','隐裂'],  # 22
    #                 ['ZKY','舟框印'],  # 23
    #                 ['GZHY','半圆黑边','舟齿印'],  # 24
    #                 ]
    # labelalllist = [
    #                 ['HD', '黑点'],  # 7
    #                 ['QLP', '气流片'],  # 13
    #                 ['HBN', '黑斑'],  # 15
    #                 ['GK', '过刻', '过客', '过客、', '四角发黑'],  # 16
    #                 ['HB', '黑边', '黑边1', '小黑边', '大黑边', '边缘少刻', '边缘过刻'],  # 17
    #                 ['DS', '断栅','LXDS', '连续断栅', '密集断栅', '背场缺失'],  # 21
    #                 ['SY', '水印', 'ˮӡ'],  # 26
    #                 ['MD', '麻点'],  # 28
    #                 ['GZHY', '工装黑印', '底杆印', '舟齿印', '舟齿', '带水烧伤', '夹持印', 'ZCY','KDSS', '卡点烧伤', '卡点过烧'],  # 42
    #                 ["HS", '划痕', '连续划痕', 'HH', '划伤','QTHS', '其他划伤', '其它划伤', '未知划伤', '其它划伤、','DCHIHS', '顶齿划伤'],
    #                 ]
    for file in json_file:
        # print(file)
        a, b = os.path.splitext(file)
        # print("文件名", a)
        imgpath = os.path.join(imgdir, a + '.png')
        oldimgpath = os.path.join(imgdir, a + '.jpg')
        outfilepath = os.path.join(out_json_path, file)
        outimgfilepath = os.path.join(out_img_path, a + '.png')
        flagg = 0
        # # if os.path.exists(outfilepath) and os.path.exists(outimgfilepath):
        #     flagg = 1

        # json文件有相应的图片
        if (os.path.exists(imgpath) or os.path.exists(oldimgpath)) and flagg == 0:
            if not os.path.exists(imgpath):
                os.rename(oldimgpath, imgpath)
            rz = "清洗的图片名：" + a + "\n"
            txt = open(logdir, 'a+')
            txt.write(rz)
            txt.close()
            filepath = os.path.join(json_path, file)
            # print("filepath;", filepath)
            outfilepath = os.path.join(out_json_path, a + '.json')
            outimgfilepath = os.path.join(out_img_path, a + '.png')

            labelcount = {}
            ordershape = {}
            shapelist = []
            arealist = []
            try:
                with open(filepath, 'r') as f:
                    # with codecs.open(filepath, 'r', 'utf-8') as f:
                    # encoding='GB2312'
                    data = json.load(f)
                    # data = data1
                    # print(data)
                    # print(type(data))
                    imgdata = data["shapes"]
                    imgdata11 = list(imgdata)
                    data["imagePath"] = a + '.png'
                    # print(imgdata)
                    flag11 = 0
                    if imgdata:  # 如果shapes内有元素
                        for label in imgdata11:
                            flag11 += 1
                            # print("flag11,abel",flag11, label)
                            class_name = label["label"]
                            class_name00 = label["label"]

                            # print("class_name", class_name00)

                            # print("class_name", class_name)
                            if class_name not in classes_count:
                                """统计每种类型出现次数"""
                                classes_count[class_name] = 1
                            else:
                                classes_count[class_name] += 1
                            # label = imgdata[i]
                            # 清洗标签

                            # print("labelalllist;", labelalllist, len(labelalllist))
                            daclasslist = []

                            for i in range(len(labelalllist)):
                                daclasslist.append(labelalllist[i][0])

                                # print("labelalllist[i];", labelalllist[i])
                                label_clean(labelalllist[i], label, labelcount, last_classes_count)

                            new_class_name = label["label"]
                            # print("new_class_name", new_class_name)
                            # print("new_class_name,daclasslist", new_class_name,daclasslist)

                            # print("class_name00: %s _new_class_name: %s ", % (class_name00,new_class_name))

                            if new_class_name not in daclasslist:
                                # print("删除outfilepath", filepath)
                                # print("删除前imgdata", imgdata)
                                print("删除前label", label)

                                imgdata.remove(label)
                                print("删除的label", new_class_name)

                            else:
                                # print("label1111111111111",label)
                                if new_class_name not in new_classes_count:
                                    # 统计每种类型出现次数
                                    new_classes_count[new_class_name] = 1
                                else:
                                    new_classes_count[new_class_name] += 1

                                if 'shape_type' not in label:
                                    label['shape_type'] = "polygon"

                                if label['shape_type'] == "polygon":
                                    # print("label;" ,label)

                                    pt = label['points']
                                    # print("pt", len(pt))
                                    if len(pt) <= 2:
                                        imgdata.remove(label)
                                        new_classes_count[new_class_name] -= 1
                                        # del label
                                    else:
                                        shapelist.append(label)
                                        # print("dayuliangdian")
                                        area = compute_polygon_area(pt) + (0.001 * flag11)
                                        # print(area)

                                        arealist.append(area)
                                        imgdata.remove(label)
                                        # print("arealist333",arealist)
                                        # del label
                                elif label['shape_type'] == "rectangle":

                                    pt = label['points']
                                    # print("pt", pt)
                                    if len(pt) != 2:
                                        imgdata.remove(label)
                                        new_classes_count[new_class_name] -= 1
                                        # del label
                                    else:
                                        # print("label222222222222", label)
                                        shapelist.append(label)
                                        area = abs((pt[1][0] - pt[0][0]) * (pt[1][1] - pt[0][1])) + (
                                                0.001 * flag11)  # compute_polygon_area(pt)
                                        # print(area)

                                        arealist.append(area)
                                        imgdata.remove(label)
                                        # del label
                                elif label['shape_type'] == "circle":

                                    pt = label['points']
                                    if len(pt) != 2:
                                        imgdata.remove(label)
                                        new_classes_count[new_class_name] -= 1
                                        # del label
                                    else:
                                        shapelist.append(label)
                                        # 计算半径
                                        p1 = np.array(pt[0])
                                        p2 = np.array(pt[1])
                                        p3 = p2 - p1
                                        p4 = math.hypot(p3[0], p3[1])
                                        # print(p4)
                                        r = math.ceil(p4)  # 向上取整r
                                        # c = np.array(pt, dtype = np.int32)
                                        # cv2.circle(im, (pt[0][0], pt[0][1]), r, 255, -1)

                                        area = 3.14 * r * r + (0.001 * flag11)
                                        arealist.append(area)
                                        # ordershape[area]
                                        imgdata.remove(label)

                        for yy in range(0, len(arealist)):
                            ordershape[arealist[yy]] = yy
                            # print("arealist,ordershape", arealist, ordershape)
                        arealist.sort()  # 排序

                        for area11 in arealist:
                            # print("area11", area11)
                            listi = ordershape[area11]

                            # print("shapelist[listi]", shapelist[listi])
                            imgdata.insert(0, shapelist[listi])
                            # print("imgdata", imgdata)

                            # imgdata.append(shapelist[listi])
                        # """
                        # print("imgdata2222222222222222222222", imgdata)

                        print(new_classes_count)
                        # print(last_classes_count)
                        print(classes_count)

                        # print(imgdata)
                        after = data
                        imgdatabb = after["shapes"]
                        labelmedict = {}
                        if imgdatabb:

                            for label22 in imgdatabb:

                                classlisttt = label22["label"]
                                print("class_name00: {0} _new_class_name: {1} ".format(class_name00, classlisttt))
                                # classlisttt = shapelist[listi]["label"]  # last_classeslist_count
                                if classlisttt not in last_classeslist_count:
                                    # 统计每种类型出现次数
                                    last_classeslist_count[classlisttt] = 1
                                else:
                                    last_classeslist_count[classlisttt] += 1

                                if classlisttt not in labelmedict:
                                    # 统计每种类型出现次数
                                    labelmedict[classlisttt] = 1
                                else:
                                    labelmedict[classlisttt] += 1
                            for key in labelmedict.keys():
                                print("各个故障数量", key, labelmedict[key], labelcount[key])
                                if labelmedict[key] > labelcount[key]:
                                    print("此图片有问题")

                            # 打开文件并覆盖写入修改后内容
                            # print("outfilepath", outfilepath)
                            # print("outimgfilepath", outimgfilepath)
                            with open(outfilepath, 'w') as f:
                                data = json.dump(after, f, indent=2, ensure_ascii=False)  # , ensure_ascii=False
                                print("清洗标签写入成功")
                            shutil.move(imgpath, outimgfilepath)
                            cnnt = cnnt + 1


                        else:
                            print("空11json")
                            # f.close()
                            # os.remove(filepath)
                        print(last_classeslist_count)
                    else:

                        print("空22json")
                        # f.close()
                        # os.remove(filepath)

            except:
                txt = open(logdir, 'a+')
                error = '\n\n\n' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + '\n' + str(traceback.format_exc())
                txt.write(error)
                txt.close()
                pass

    print("清洗标签数;", cnnt)
    rz = "labelalllist:  " + str(labelalllist) + "\n"
    rz = rz + "last_classeslist_count:  " + str(last_classeslist_count) + "\n"
    txt = open(logdir, 'a+')
    txt.write(rz)
    txt.close()


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


class labelme2coco(object):
    def __init__(self, labelme_json=[], save_json_path='./tran.json'):
        '''
        :param labelme_json: 所有labelme的json文件路径组成的列表
        :param save_json_path: json保存位置
        '''
        self.labelme_json = labelme_json
        self.save_json_path = save_json_path
        self.images = []
        self.categories = []
        self.annotations = []
        # self.data_coco = {}
        self.label = []
        self.annID = 1
        self.fileID = 1
        self.height = 0
        self.width = 0
        rz = "转换格式开始：" + "\n\n\n"
        txt = open(logdir, 'a+')
        txt.write(rz)
        txt.close()

        self.save_json()

    def data_transfer(self):
        sum = len(self.labelme_json)
        HIDE_CURSOR = "\033[?25l"
        SHOW_CURSOR = "\033[?25h"
        print(HIDE_CURSOR, end="", flush=True)  # 隐藏光标
        for num, json_file in enumerate(self.labelme_json):
            # print("111222222222222222222222222222222222222222222222")
            print(str(self.fileID) + ' / ' + str(sum), end="\r", flush=True)
            with open(json_file, 'r') as fp:
                strF = fp.read()
                if len(strF) > 0:
                    data = json.loads(strF)
                    # data = json.load(fp)  # 加载json文件

                    self.images.append(self.image(data, num))

                    for shapes in data['shapes']:

                        label = shapes['label']
                        if label not in self.label:
                            self.categories.append(self.categorie(label))
                            self.label.append(label)
                        points = shapes['points']  # 这里的point是用rectangle标注得到的，只有两个点，需要转成四个点 ，点不行
                        pointstmp = []
                        try:
                            if shapes['shape_type'] == "rectangle":
                                yp1 = points[0][1]
                                xp1 = points[0][0]
                                yp2 = points[1][1]
                                xp2 = points[1][0]
                                pointstmp.append(np.array([xp1, yp1]).tolist())
                                pointstmp.append(np.array([xp1, yp2]).tolist())
                                pointstmp.append(np.array([xp2, yp2]).tolist())
                                pointstmp.append(np.array([xp2, yp1]).tolist())
                                points = pointstmp
                            elif shapes['shape_type'] == "circle":
                                p1 = np.array(points[0])
                                p2 = np.array(points[1])
                                p3 = p2 - p1
                                p4 = math.hypot(p3[0], p3[1])
                                # print(p4)
                                r = math.ceil(p4)  # 向上取整r
                                # c = np.array(pt, dtype = np.int32)
                                '''
                                xp1 = points[0][0] - r
                                yp1 = points[0][1] - r
                                xp2 = points[0][0] + r
                                yp2 = points[0][1] + r
                                '''
                                xp = points[0][0] - r
                                yp = points[0][1] - r
                                xpp = points[0][0] + r
                                ypp = points[0][1] + r
                                xp1 = round(xp + (2 - math.sqrt(2)) * r)
                                yp1 = yp
                                xp2 = round(xp + math.sqrt(2) * r)
                                yp2 = yp
                                xp3 = xpp
                                yp3 = round(yp + (2 - math.sqrt(2)) * r)
                                xp4 = xpp
                                yp4 = round(yp + math.sqrt(2) * r)
                                xp5 = round(xp + math.sqrt(2) * r)
                                yp5 = ypp
                                xp6 = round(xp + (2 - math.sqrt(2)) * r)
                                yp6 = ypp
                                xp7 = xp
                                yp7 = round(yp + math.sqrt(2) * r)
                                xp8 = xp
                                yp8 = round(yp + (2 - math.sqrt(2)) * r)

                                pointstmp.append(np.array([xp1, yp1]).tolist())
                                pointstmp.append(np.array([xp2, yp2]).tolist())
                                pointstmp.append(np.array([xp3, yp3]).tolist())
                                pointstmp.append(np.array([xp4, yp4]).tolist())
                                pointstmp.append(np.array([xp5, yp5]).tolist())
                                pointstmp.append(np.array([xp6, yp6]).tolist())
                                pointstmp.append(np.array([xp7, yp7]).tolist())
                                pointstmp.append(np.array([xp8, yp8]).tolist())

                                points = pointstmp
                            elif shapes['shape_type'] == "line":
                                pointstmp.append((np.array(points[0]) + np.array([0, -1])).tolist())
                                pointstmp.append((np.array(points[1]) + np.array([0, -1])).tolist())
                                pointstmp.append((np.array(points[1]) + np.array([0, 1])).tolist())
                                pointstmp.append((np.array(points[0]) + np.array([0, 1])).tolist())
                                points = pointstmp
                            elif shapes['shape_type'] == "point":
                                pointstmp.append((np.array(points[0]) + np.array([-1, -1])).tolist())
                                pointstmp.append((np.array(points[0]) + np.array([-1, 1])).tolist())
                                pointstmp.append((np.array(points[0]) + np.array([1, 1])).tolist())
                                pointstmp.append((np.array(points[0]) + np.array([1, -1])).tolist())
                                points = pointstmp
                            elif shapes['shape_type'] == "linestrip":
                                for i in range(len(points)):
                                    pointstmp.append((np.array(points[i]) + np.array([0, -1])).tolist())
                                for i in range(len(points) - 1, -1, -1):
                                    pointstmp.append((np.array(points[i]) + np.array([0, 1])).tolist())
                                points = pointstmp
                        except:
                            error = '\n\n\n' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + '\n' + str(
                                traceback.format_exc())
                            txt = open(logdir, 'a+')
                            txt.write(error)
                            txt.close()
                            pass
                        self.annotations.append(self.annotation(points, label, num))
                        self.annID += 1
            self.fileID += 1
        print(SHOW_CURSOR, end="", flush=True)  # 程序结束时显示光标

    def image(self, data, num):
        image = {}
        # img = utils.img_b64_to_arr(data['imageData'])  # 解析原图片数据
        # img=io.imread(data['imagePath']) # 通过图片路径打开图片
        # img = cv2.imread(data['imagePath'], 0)
        imgname = data['imagePath'].split('/')[-1]
        # print("imgname;", imgname)
        rz = "图片名; " + imgname + "\n"
        txt = open(logdir, 'a+')
        txt.write(rz)
        txt.close()
        aa, bb = os.path.splitext(imgname)
        height = data["imageHeight"]
        width = data["imageWidth"]
        # height, width = img.shape[:2]
        # img = None
        image['height'] = height
        image['width'] = width
        image['id'] = num + 1
        image['file_name'] = aa + ".png"

        self.height = height
        self.width = width

        return image

    def categorie(self, label):
        categorie = {}
        categorie['supercategory'] = 'Cancer'
        categorie['id'] = len(self.label) + 1  # 0 默认为背景
        categorie['name'] = label
        return categorie

    def annotation(self, points, label, num):
        annotation = {}
        annotation['segmentation'] = [list(np.asarray(points).flatten())]
        annotation['iscrowd'] = 0
        annotation['image_id'] = num + 1
        # annotation['bbox'] = str(self.getbbox(points)) # 使用list保存json文件时报错（不知道为什么）
        # list(map(int,a[1:-1].split(','))) a=annotation['bbox'] 使用该方式转成list
        annotation['bbox'] = list(map(float, self.getbbox(points)))
        annotation['area'] = annotation['bbox'][2] * annotation['bbox'][3]
        # annotation['category_id'] = self.getcatid(label)
        annotation['category_id'] = self.getcatid(label)  # 注意，源代码默认为1
        annotation['id'] = self.annID
        return annotation

    def getcatid(self, label):
        for categorie in self.categories:
            if label == categorie['name']:
                return categorie['id']
        return 1

    def getbbox(self, points):
        # img = np.zeros([self.height,self.width],np.uint8)
        # cv2.polylines(img, [np.asarray(points)], True, 1, lineType=cv2.LINE_AA)  # 画边界线
        # cv2.fillPoly(img, [np.asarray(points)], 1)  # 画多边形 内部像素值为1
        polygons = points

        mask = self.polygons_to_mask([self.height, self.width], polygons)
        # print(mask)
        return self.mask2box(mask)

    def mask2box(self, mask):
        '''从mask反算出其边框
        mask：[h,w]  0、1组成的图片
        1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        '''
        # np.where(mask==1)

        index = np.argwhere(mask == 1)
        # print(index)
        rows = index[:, 0]
        clos = index[:, 1]

        # 解析左上角行列号
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        # 解析右下角行列号
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        # return [(left_top_r,left_top_c),(right_bottom_r,right_bottom_c)]
        # return [(left_top_c, left_top_r), (right_bottom_c, right_bottom_r)]
        # return [left_top_c, left_top_r, right_bottom_c, right_bottom_r]  # [x1,y1,x2,y2]
        return [left_top_c, left_top_r, right_bottom_c - left_top_c,
                right_bottom_r - left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

    def polygons_to_mask(self, img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        import PIL.ImageDraw as ImageDraw
        ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco = {}
        data_coco['images'] = self.images
        data_coco['categories'] = self.categories
        data_coco['annotations'] = self.annotations
        return data_coco

    def save_json(self):

        self.data_transfer()

        self.data_coco = self.data2coco()
        # print("111111111111111111111111111111111111111111111111111111111")
        # 保存json文件
        json.dump(self.data_coco, open(self.save_json_path, 'w'), indent=4, cls=MyEncoder)  # indent=4 更加美观显示


'''

读取中文路径图片

'''


def cv_imread(file_path=""):
    img_mat = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), 1)
    return img_mat


'''

添加 无故障图片到train.json文件，用于过检图片当作背景进行训练
执行后手动将okimg中图片加入train文件夹中即可

'''


def addImgToJson(jsonpath, imgpath, traindir):
    with open(jsonpath, 'r') as f:
        print(jsonpath)
        data = json.load(f)

        images = data["images"]
        id = images[-1]["id"]
        print(images[-1])
    print(imgpath)
    for file in os.listdir(imgpath):
        imgdir = os.path.join(imgpath, file)
        if os.path.splitext(imgdir)[-1] in ['.png', '.bmp']:
            img = cv_imread(imgdir)
            imgdict = dict()
            print("imgdir", imgdir)
            imgdict["height"], imgdict["width"] = img.shape[:-1]
            id += 1
            imgdict["id"] = id
            imgdict["file_name"] = file
            images.append(imgdict)
            pic_imgpath = os.path.join(imgpath, file)
            train_imgpath = os.path.join(traindir, file)
            print('pic_imgpath', pic_imgpath)
            # shutil.copyfile(pic_imgpath, traindir)
            shutil.move(pic_imgpath, train_imgpath)  # 图片路径，存入路径

    json.dump(data, open(jsonpath, "w"), indent=2, ensure_ascii=False)


from my_work_test import labelmetococo_values

# def main(traindatapath, rootpath):
#     return traindatapath, rootpath


traindatapath = labelmetococo_values()
# traindatapath, rootpath, modelpath = main(traindatapath=traindatapath, rootpath=rootpath, modelpath=modelpath)
print(traindatapath)
rootpath = traindatapath
# file_dir = "\\\\172.16.11.198\\4BGPv1.1\\mask标签汇总\\正面\\" #最原始图片
# file_dir = "F:\\GP\\image\\背面\\"
# file_dir = "/home/ai_data/SY_Song/mask/maskrcnn-benchmark/datasets/halm_eldata/el_halm_xi211025/train"
rz = '\n\n\n开始时间;' + str(time.strftime('%Y-%m-%d %H:%M:%S')) + '\n'
# traindatapath = "/home/Data/JW_Yue/mmdetection/data/data20240907"
# rootpath = "/home/Data/JW_Yue/mmdetection/data/data20240907"  # coco_back0529"
# modelpath = "/home/ai_data/JW_Yue/mmdetection/output_model/halm_data/data20240907/model/"
rz = rz + "traindatapath: " + traindatapath + "\n"
rz = rz + "rootpath: " + rootpath + "\n"
# file_dir = "/home/ai1/IMG_DATA/GP/GP_FRONT/12BB标签（人打）/张利强/my_gp1a正/"
# traindatapath = "E:\\pycharm_detetion\\GP\Mask_RCNN-master\\maskdata\\GP_FRONT\\GP_FRONTALL0506\\imagedata\\" #y原图
# rootpath = "E:\\pycharm_detetion\\maskrcnn-benchmark\\datasets\\coco0528"
jsondir = os.path.join(rootpath, "json")  # "E:\\pycharm_detetion\\maskrcnn-benchmark\\datasets\\coco\\json"
oldjsondir = os.path.join(rootpath, "oldjson")
picdir = os.path.join(rootpath, "pic")
inputpath = os.path.join(rootpath,
                         "json/*.json")  # "E:\\pycharm_detetion\\maskrcnn-benchmark\\datasets\\coco\\json\\*.json"
okimgpath = os.path.join(rootpath, "okimg")

annotationsdir = os.path.join(rootpath, "annotations")
traindir = os.path.join(rootpath, "train")
valdir = os.path.join(rootpath, "val")
trainjsondir = os.path.join(annotationsdir, "instances_train2017.json")
valjsondir = os.path.join(annotationsdir, "val.json")
if not os.path.exists(jsondir):
    os.makedirs(jsondir)
if not os.path.exists(annotationsdir):
    os.makedirs(annotationsdir)
if not os.path.exists(traindir):
    os.makedirs(traindir)
if not os.path.exists(valdir):
    os.makedirs(valdir)
if not os.path.exists(oldjsondir):
    os.makedirs(oldjsondir)
if not os.path.exists(picdir):
    os.makedirs(picdir)
# if not os.path.exists(modelpath):
#     os.makedirs(modelpath)

txtname = str(time.strftime('%Y-%m-%d %H:%M:%S'))
logdir = annotationsdir + '/' + txtname + '.txt'
txt = open(logdir, 'a+')
txt.write(rz)
txt.close()

# ouputpath = "E:\\pycharm_detetion\\maskrcnn-benchmark\\datasets\\coco0506\\annotations\\train.json"
# splitjson_img(file_dir, traindatapath) ##将打标签后的图片分成json和pic
# inputpath = "F:\\image\\5bb\\jsontest\\*.json"
# trainjsondir  = "F:\\image\\5bb\\jsontest\\train.json"
# inputimg = "/home/ai3/贴图样本与标签/EL样本库/10BB210/20200331/舟框印/10BB210舟框印8（样本+标签）/"  # 混膜色图片
# inputjson = "/home/ai3/贴图样本与标签/EL样本库/10BB210/20200331/舟框印/10BB210舟框印8（样本+标签）/"  # 图片 + json
# print(inputjson)

# x1 = 4
# bias = 3
# tiaoxuanimg(inputimg,inputjson,picdir,oldjsondir,x1,bias)

# step1 以下四行图像清洗
# labelme_json=['./Annotations/*.json']
# print("清洗标签开始")
# train_data(traindatapath, rootpath)  # 清洗标签
# print("清洗标签完成")
# # #
# # # # #jsondir11 = "F:\\GP\\image\\coco_back0610\\oldjson"
# # #
# # # # # jsondir11 = "F:\\GP\\image\\gp_back\\json"
# # # # #dellabel(json_path = jsondir11)
# # # # step2 按缺陷名称切分样本保存
# # # splitclass(json_path=jsondir, rootdir=rootpath)
# # # # # xmlclass()
# # # #
# # # # step3 labelme格式转换成coco数据集
# print("转格式开始")
# labelme_json = glob.glob(inputpath)
# labelme2coco(labelme_json, trainjsondir)
# classlist = classtojson(annotationsdir)  # 将coco格式的json里的故障排序转换为dict然后写入json文件labelme_json = glob.glob(inputpath)
# # labelme2coco(labelme_json, trainjsondir)
# # classlist = classtojson(annotationsdir)  # 将coco格式的json里的故障排序转换为dict然后写入json文件
# # print("格式转换成功")
# show(annotationsdir, json_path=jsondir, classlist=classlist)
# show_old(annotationsdir, json_path=oldjsondir)
# step4 添加没有缺陷的样本，防止图像出现误判
# 以上三步先使用，最后一步注释掉，
# 清洗完，注释掉前3步，打开最后一步往coco.json文件添加无缺陷样本
# addImgToJson(trainjsondir, okimgpath, traindir)
labelalllist = [['PY', '偏移', '偏移1', '印刷偏移'],
                ['SMZHS', 'SMZHH', '石墨舟划伤'],
                ['LXDS', '连续断栅', '密集断栅', '背场缺失'],
                ['HD', '黑点'],
                ['BCGS', '背场过烧', '背极发黑', '背电极发黑', '过烧'],
                ['WZFH', '雾状发黑', '雾状', '小雾状', '大雾状'],
                ['QLP', '气流片'],
                ['LX', '亮线'],
                ['HBN', '黑斑'],
                ['GK', '过刻', '过客', '过客、', '四角发黑'],
                ['HB', '黑边', '黑边1', '小黑边', '大黑边', '边缘少刻', '边缘过刻'],
                ['DS', '断栅'],
                ['LXHS', '连续划伤', 'SMZLB', 'DCHAHS'],
                ['KDY', '卡点印'],
                ['ZKY', '舟框印'],
                ['SY', '水印', 'ˮӡ'],
                ['MD', '麻点'],
                ['TXY', '同心圆'],
                ['GLY', '滚轮印'],
                ['YL', 'XXYL', '星形隐裂', '星型隐裂', 'BYYL', '边缘隐裂', '倒角隐裂', '隐裂', '碎片'],
                ['ZCY', '工装黑印', '底杆印', '舟齿印', '舟齿', '带水烧伤', '夹持印', 'GZHY', 'GZHY1', 'HLCY', '花篮齿印', '顶针印'],  # 42
                ['PDY', '皮带印'],
                ['YK', '印宽'],
                ['ZSDS', '主栅断栅'],
                ["HS", '划痕', 'HH', '划伤', 'LHHS', 'QTHS', 'ZXHS'],
                ["XPY", "吸盘印"],
                ["BDJFH", '背电极发黑'],
                ["BJFH", '边角发黑'],
                ["DJPY", "搭接偏移"],
                ["PDY1", '皮带印1'],
                ["HJ", '黑角'],
                ["QHB", '浅黑边'],
                ["WR", '污染'],
                ["HX", '黑线'],
                ["CXYC", '成像异常'],
                ["ZSYH", '主栅印厚'],
                ["BJPY", '边角偏移']
                ]
''' step1 查看清洗前标注标签的命名 '''
show_old(annotationsdir, json_path=oldjsondir)

''' step2 修改上面labelalllist，为标签清洗做准备 '''

''' step3 清洗标签 '''
train_data(traindatapath, rootpath, labelalllist)

''' step4 labelme格式转换成coco数据集 '''
labelme_json = glob.glob(inputpath)
labelme2coco(labelme_json, trainjsondir)
classlist = classtojson(annotationsdir)
show(annotationsdir, json_path=jsondir, classlist=classlist)

''' step5 添加没有缺陷的样本，防止图像出现误判 '''
addImgToJson(trainjsondir, okimgpath, traindir)
