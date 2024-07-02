import argparse
import json
import os

import cv2
import numpy as np
from tqdm import tqdm


def yolo_to_coco(image_path, txt_path, classes_path, json_path):
    """
    yolo格式转json格式
    :param image_path: 图片文件夹路径
    :param txt_path: 标签文件夹路径
    :param classes_path: classes.txt文件的路径
    :param json_path: 输出json文件夹的路径
    :return:
    """
    with open(classes_path) as f:
        classes = list(map(lambda x: x.strip(), f.readlines()))

    dataset = {'categories': [], 'annotations': [], 'images': []}
    for i, cls in enumerate(classes, 0):
        dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})

    ann_id_cnt = 0
    for k, index in enumerate(tqdm(os.listdir(image_path))):
        # 支持 png jpg 格式的图片。
        txt_file = index.replace('images', 'txt').replace('.jpg', '.txt').replace('.png', '.txt')
        # 读取图像的宽和高
        im = cv2.imdecode(np.fromfile(os.path.join(image_path, index), dtype=np.uint8), -1)

        # im = cv2.imread(os.path.join(input_image_path, index))
        height, width, _ = im.shape
        # 添加图像的信息
        if not os.path.exists(os.path.join(txt_path, txt_file)):
            # 如没标签，跳过，只保留图片信息。
            continue
        dataset['images'].append({'file_name': index,
                                  'id': int(index[:-4]) if index[:-4].isnumeric() else index[:-4],
                                  'width': width,
                                  'height': height})
        with open(os.path.join(txt_path, txt_file), 'r') as fr:
            label_list = fr.readlines()
            for label in label_list:
                label = label.strip().split()
                x = float(label[1])
                y = float(label[2])
                w = float(label[3])
                h = float(label[4])

                # convert x,y,w,h to x1,y1,x2,y2
                H, W, _ = im.shape
                x1 = round((x - w / 2) * W)
                y1 = round((y - h / 2) * H)
                x2 = round((x + w / 2) * W)
                y2 = round((y + h / 2) * H)
                # 标签序号从0开始计算, coco2017数据集标号混乱，不管它了。
                cls_id = int(label[0])
                width = max(0, x2 - x1)
                height = max(0, y2 - y1)
                dataset['annotations'].append({
                    'area': width * height,
                    'bbox': [x1, y1, width, height],
                    'category_id': cls_id,
                    'id': ann_id_cnt,
                    'image_id': int(index[:-4]) if index[:-4].isnumeric() else index[:-4],
                    'iscrowd': 0,
                    # mask, 矩形是从左上角点按顺时针的四个顶点
                    'segmentation': [[x1, y1, x2, y1, x2, y2, x1, y2]]
                })
                ann_id_cnt += 1
    json_name = "result.json"
    # 保存结果
    with open(os.path.join(json_path, json_name), 'w') as f:
        json.dump(dataset, f)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default='',
                        help="输入的图片文件夹路径")
    parser.add_argument('--txt_path', type=str, default='',
                        help="输入的标签文件夹路径")
    parser.add_argument('--classes_path', type=str, default='',
                        help="classes.txt文件的路径")
    parser.add_argument('--json_path', type=str, default='',
                        help="输出json文件夹的路径")
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    yolo_to_coco(**vars(opt))
