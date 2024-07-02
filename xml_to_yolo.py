import argparse
import os
import xml.etree.ElementTree as et

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


def xml_to_yolo(xml_path, txt_path):
    """
    voc格式转yolo格式
    :param xml_path: 输入的xml文件夹的路径
    :param txt_path: 输出的txt文件夹的路径
    :return:
    """

    # 遍历xml文件所有的类别名称
    classes = []
    for i in os.listdir(xml_path):
        xml_file = open(os.path.join(xml_path, i), encoding="utf8")
        tree = et.parse(xml_file)
        tree_root = tree.getroot()
        for obj in tree_root.iter("object"):
            cls = obj.find("name").text
            if cls not in classes:
                classes.append(cls)

    # 生成xml文件
    for i in tqdm(os.listdir(xml_path)):
        label_name = os.path.splitext(i)[0]
        out_txt_file_path = os.path.join(txt_path, label_name + ".txt")
        out_txt_file = open(out_txt_file_path, "w")
        # 解析xml文件
        xml_file = open(os.path.join(xml_path, i), encoding="utf8")
        tree = et.parse(xml_file)
        tree_root = tree.getroot()
        size = tree_root.find("size")
        w = int(size.find("width").text)
        h = int(size.find("height").text)
        for obj in tree_root.iter("object"):
            cls = obj.find("name").text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xml_box = obj.find("bndbox")
            b = (
                float(xml_box.find("xmin").text),
                float(xml_box.find("xmax").text),
                float(xml_box.find("ymin").text),
                float(xml_box.find("ymax").text),
            )
            bb = convert((w, h), b)
            out_txt_file.write(
                str(cls_id) + " " + " ".join([str(a) for a in bb]) + "\n"
            )
        out_txt_file.close()
        xml_file.close()

    # 生成classes.txt文件
    classes_txt_path = os.path.join(txt_path, "classes.txt")
    f = open(classes_txt_path, "w", encoding="utf8")
    for i in classes:
        f.write(i + "\n")
    f.close()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_path', type=str, default='',
                        help="输入的xml文件夹路径")
    parser.add_argument('--txt_path', type=str, default='',
                        help="输出的txt文件夹路径")
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    xml_to_yolo(**vars(opt))
