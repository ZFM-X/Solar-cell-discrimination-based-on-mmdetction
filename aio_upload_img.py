import datetime
import requests


def upload_img(img_filename: str, pipeline_name: str, wafer_id: str, wafer_bin: str, defect_name_cn: str, defect_name_en: str, logger: None):
    """上传图片

    Args:
        img_filename (str): 图片完整路径
        pipeline_name (str): 线别名称
        wafer_id (str): wafer id
        wafer_bin (str): wafer bin
        defect_name_cn (str): 缺陷中文名称
        defect_name_en (str): 缺陷英文名称
    """

    data = {
        "sourceTime": str(datetime.datetime.now()).split('.')[0], 
        "prodlinesName": pipeline_name, # 线别名
        "imageID": wafer_id, # wafer id
        "imageBIN": str(int(wafer_bin)), # bin
        "flawName": defect_name_cn, # 缺陷中文名
        "imageName": img_filename.split('\\')[-1], # 图像名，带后缀
        "flawEngName": defect_name_en  # 缺陷英文名
    }
    
    imgdata = open(img_filename, 'rb')
    imgfile = [("image", imgdata)]

    if logger is not None:
        logger.info(f"Request img data: {data}")
    
    response = requests.post('http://10.24.6.9:18080/ai/aiMissedDetection/8/input ', data=data, files=imgfile)
    response.encoding = response.apparent_encoding
    retext = response.text
    return retext
    # print("response.text: ", retext)


# def py_to_flask(warninfordict, imgdata):
#     cols_name = ", ".join(warninfordict["flaw_name"])
#     cols_engname = ", ".join(warninfordict["flaw_engname"])
#     # sbase64_data = sbase64_data[1:]
#     # print("base64_data",base64_data)
#     # print("11111111111111")

#     task = {"sourceTime": warninfordict["time"], "prodlinesName": warninfordict["prodlines_name"],
#             "imageID": warninfordict["img_id"],
#             "imageBIN": warninfordict["img_bin"],
#             "flawName": cols_name,
#             "imageName": warninfordict["imgname"],
#             "flawEngName": cols_engname

#             }  # " md5": warninfordict["md5"],

#     imgfile = [("image", imgdata)]
#     # print("task",task)

#     a = web_requests()
#     retext = a.Interface(urlpath, task, imgfile)
#     # strtask = str(task,'utf8')
#     return retext


# def Interface(self, urlpath, task, imgdata):
#     print("task", task)

#     response = requests.request("POST", url=urlpath, data=task, files=imgdata)
#     response.encoding = response.apparent_encoding
#     retext = response.text
#     print("response.text: ", retext)

#     return retext
