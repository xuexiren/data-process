import argparse
import json
import os

from tqdm import tqdm


def convert(size, box):
    """
    坐标归一化
    :param size: 图片的宽高
    :param box: 坐标
    :return:
    """
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def coco_to_yolo(json_path, out_path):
    """
    coco转yolo格式
    :param json_path: json文件路径
    :param out_path: 输出txt文件夹路径
    :return:
    """

    # 读取json文件
    data = json.load(open(json_path, "r"))
    # 重新映射id
    id_map = {}
    with open(os.path.join(out_path, 'classes.txt'), 'w', encoding="utf-8") as f:
        # 写入classes.txt
        for i, category in enumerate(data['categories']):
            f.write(f"{category['name']}\n")
            id_map[category['id']] = i
    # 生成txt文件
    for img in tqdm(data["images"]):
        img_name = img["file_name"]
        img_width = img["width"]
        img_height = img["height"]
        img_id = img["id"]
        head = os.path.splitext(img_name)[0]
        txt_name = head + ".txt"
        f_txt = open(os.path.join(out_path, txt_name), 'w', encoding="utf8")
        for ann in data['annotations']:
            if ann['image_id'] == img_id:
                box = convert((img_width, img_height), ann["bbox"])
                f_txt.write("%s %s %s %s %s\n" % (id_map[ann["category_id"]], box[0], box[1], box[2], box[3]))
        f_txt.close()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', type=str, default='',
                        help="json文件路径")
    parser.add_argument('--out_path', type=str, default='',
                        help="输出txt文件夹路径")
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    coco_to_yolo(**vars(opt))
