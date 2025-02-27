"""

Convert result of AI model to rule condition.

"""
from copy import deepcopy
import math
import numpy as np
import cv2
from PIL import Image


def convert_rcnn_result_to_el_rule_condition(result: list, category_names: list, image: np.array, config):
    """
    Convert result of rcnn series, which contains bbox and masks to rule condition.

    Args:
        result: list, which has two elements. Element 0 contains bbox and confidence; element 1 contains masks. Both
            of them were sorted by category index.
        category_names: list, category names in coco json file.
        image: np.array, original image.
        config: dict, config for rule engine

    Returns:
        defects: list, list of defect.
            defect: dict, rule condition for rule engine.
                category: str, category name, e.g. DS.
                area: float, area of defect, which unit is pixel^2.
                length: float, length of defect, which unit is pixel.
                grayscale: float, which range is [0, 100], and 0 is white while 100 is black.
                image_shape: tuple, height and width of image, e.g. (520, 520).
                same_defect_number: int, the number of same defect

    """

    except_box = config['except_box']
    region_box = config['region_box']
    region_index_box = config['region_index_box']
    main_grid_line_x = config['main_grid_line_x']
    bell_location_y = config['bell_location_y']

    defects = []
    bboxs = result[0]
    masks = result[1]
    mask_background = np.ones((image.shape[0], image.shape[1]))

    for box in except_box:
        mask_background[box[1]:box[3], box[0]:box[2]] = 0

    grayscale_255_0_average_background = np.sum(mask_background * image) / np.sum(mask_background)
    grayscale_0_100_average_background = (1 - (grayscale_255_0_average_background / 255)) * 100

    img_mask = mask_background * image
    c1 = img_mask[45:979, 107:250]  # 左颜色
    d1 = img_mask[45:979, 774:917]  # 右颜色
    mask_c1 = mask_background[45:979, 107:250]
    mask_d1 = mask_background[45:979, 774:917]
    grayscale_255_0_average_background2 = np.sum(c1) / np.sum(mask_c1)
    grayscale_255_0_average_background3 = np.sum(d1) / np.sum(mask_d1)
    gray_left = (1 - (grayscale_255_0_average_background2 / 255)) * 100
    gray_right = (1 - (grayscale_255_0_average_background3 / 255)) * 100

    number_ds = 0
    number_ds2 = 0
    number2 = 0
    number_DJPY = 0
    category_number = {}
    for ci, c in enumerate(bboxs):  # 检测到所有的缺陷
        for di, d in enumerate(c):  # 左上角点  右下角点 置信度
            category = category_names[ci]
            center_x = (d[0] + d[2]) / 2
            center_y = (d[1] + d[3]) / 2
            center_x = int(center_x)
            center_y = int(center_y)
            mask = masks[ci][di]

            mask1 = deepcopy(mask)
            image_zeros = np.zeros(shape=(int(math.sqrt(np.size(mask1)))), dtype=int)
            b5 = mask1 + [image_zeros]
            dd = b5 < 0.5

            score = bboxs[ci][di][4]

            defect_center = ((bboxs[ci][di][2] + bboxs[ci][di][0]) / 2, (bboxs[ci][di][3] + bboxs[ci][di][1]) / 2)

            region_index = None  # 缺陷中心所在区域索引
            for region_index_ in range(len(region_index_box)):
                region_index_box_ = region_index_box[region_index_]
                if (region_index_box_[0] < defect_center[0] < region_index_box_[2]) and (
                        region_index_box_[1] < defect_center[1] < region_index_box_[3]):
                    region_index = region_index_
                    break
            assert region_index is not None, '未找到缺陷中心所在区域'

            number_cross_category = len(bboxs[ci])  # 图中该种缺陷的数目

            category_numberr = len(bboxs[ci])
            category_number[category] = category_numberr
            # print('category_number:',category_number)
            ds = 'DS'
            ds2 = 'DS2'
            djpy = 'DJPY'
            if ds in category_number.keys():
                number_ds = category_number[ds]

            if ds2 in category_number.keys():
                number_ds2 = category_number[ds2] * 2
            if djpy in category_number.keys():
                number_DJPY = category_number[djpy]
            number2 = number_ds + number_ds2

            image_shape = mask.shape
            area_pixel = np.sum(mask)
            area_ratio = area_pixel / ((image_shape[0]) * (image_shape[1]))

            length_pixel = math.sqrt((d[2] - d[0]) ** 2 + (d[3] - d[1]) ** 2)
            length_ratio = length_pixel / math.sqrt(image_shape[0] ** 2 + image_shape[1] ** 2)

            mask_except = deepcopy(mask)
            # if gray_tzp5 > 65:
            for box in except_box:
                mask_except[box[1]:box[3], box[0]:box[2]] = False
                dd[box[1]:box[3], box[0]:box[2]] = False

            area_pixel_for_grayscale = np.sum(mask_except)
            if area_pixel_for_grayscale == 0:
                area_pixel_for_grayscale = 1

            end_area_pixel_for_grayscale = np.sum(dd)
            if end_area_pixel_for_grayscale == 0:
                end_area_pixel_for_grayscale = 1

            grayscale_255_0 = np.sum(mask_except * image) / area_pixel_for_grayscale
            try:
                end_grayscale_255_0 = np.sum(dd * image) / end_area_pixel_for_grayscale
            except:
                end_grayscale_255_0 = np.sum(np.dot(dd, image)) / end_area_pixel_for_grayscale

            grayscale_255_0_var = np.std(mask_except * image)
            grayscale_0_100 = (1 - (grayscale_255_0 / 255)) * 100
            end_grayscale_0_100 = (1 - (end_grayscale_255_0 / 255)) * 100
            sub_gray = np.abs(grayscale_0_100 - end_grayscale_0_100)
            gray_left_1 = np.abs(gray_left - grayscale_0_100)
            gray_right_1 = np.abs(gray_right - grayscale_0_100)
            max_defect_pixel_number_in_region = 0
            defect_mask_in_region = None  # 一个缺陷可能跨区域，这是缺陷最大的区域
            region_background_mask_ = None  # 区域背景灰度
            # 选出缺陷最主要存在的区域
            for box in region_box:
                region_mask_ = np.zeros_like(mask)  # deepcopy(mask_except)  # np.zeros_like(mask)
                # mask_except[box[1]:box[3], box[0]:box[2]] = False
                region_mask_[box[1]:box[3], box[0]:box[2]] = 1

                defect_mask_in_region_ = region_mask_ & mask_except  # 该缺陷该区域掩码
                if (_defect_pixel_number_in_region := defect_mask_in_region_.sum()) > max_defect_pixel_number_in_region:
                    defect_mask_in_region = defect_mask_in_region_
                    max_defect_pixel_number_in_region = _defect_pixel_number_in_region

                    region_background_mask_ = region_mask_ & mask_background.astype('bool')

            if max_defect_pixel_number_in_region > 0:
                # 该缺陷该区域灰度
                region_defect_gray_0_100 = (1 - (
                            (np.sum(defect_mask_in_region * image) / (defect_mask_in_region.sum() + 1)) / 255)) * 100
                # 区域中缺陷和背景的灰度差
                region_defect_bg_gray_diff_0_100 = np.abs(
                    (1 - ((np.sum(region_background_mask_ * image) / (
                                np.sum(region_background_mask_) + 1)) / 255)) * 100
                    - region_defect_gray_0_100
                )
            else:
                region_defect_bg_gray_diff_0_100 = 0

            is_cross_main_grid = 0
            is_bell_area = 0
            for _x in main_grid_line_x:
                if d[0] < _x < d[2]:
                    is_cross_main_grid = 1

                    # is locate bell
                    for _y in bell_location_y:
                        if d[1] < _y < d[3]:
                            is_bell_area = 1
                            break
            defect = {
                "category": category,
                "area_pixel": area_pixel,
                "area_ratio": area_ratio,
                "length_pixel": length_pixel,
                "length_ratio": length_ratio,
                "grayscale_255_0": grayscale_255_0,
                "image_shape": image_shape,
                "grayscale_0_100": grayscale_0_100,
                "is_cross_main_grid": is_cross_main_grid,
                "is_bell_area": is_bell_area,
                "number_ds": number_ds,
                "number_DJPY": number_DJPY,
                "score": score,
                "number2": number2,
                "sub_gray": sub_gray,
                "grayscale_255_0_var": grayscale_255_0_var,
                "gray100_bk": grayscale_0_100_average_background,
                'gray_left': gray_left,
                'gray_right': gray_right,
                'gray_left_1': gray_left_1,
                'gray_right_1': gray_right_1,
                'number_cross_category': number_cross_category,
                'region_defect_bg_gray_diff_0_100': region_defect_bg_gray_diff_0_100,
                'region_index': region_index
            }
            defects.append(defect)
    return defects, {"gray100_bk": grayscale_0_100_average_background,
                     }
