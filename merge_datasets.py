import argparse
import os
import shutil

from tqdm import tqdm


def merge_datasets(input_path, out_path):
    """
    合并数据集，将选择多个文件夹中的图片和标注文件复制到一个文件夹中
    :param input_path: 输入的文件夹路径
    :param out_path: 输出的文件夹路径
    :return:
    """

    out_image_path = os.path.join(out_path, "images")
    out_label_path = os.path.join(out_path, "labels")
    if (
            not os.path.exists(out_image_path)
            or not os.path.exists(out_label_path)
    ):
        os.makedirs(out_image_path)
        os.makedirs(out_label_path)

    image_path_list = []
    label_path_list = []
    image_name_list = []
    label_name_list = []
    for path, dir_lst, file_lst in os.walk(input_path):
        for file_name in file_lst:
            if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg")):
                image_path_list.append(os.path.join(path, file_name))
                image_name_list.append(file_name)
            if file_name.lower().endswith((".txt", ".json", ".xml")):
                label_path_list.append(os.path.join(path, file_name))
                label_name_list.append(file_name)

    # 复制图片文件
    for i in tqdm(range(len(image_path_list))):
        new_image_path = os.path.join(out_image_path, image_name_list[i])
        shutil.copy(image_path_list[i], new_image_path)

    # 复制标签文件
    for i in tqdm(range(len(label_name_list))):
        new_label_path = os.path.join(out_label_path, label_name_list[i])
        shutil.copy(label_path_list[i], new_label_path)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='',
                        help="输入的文件夹路径")
    parser.add_argument('--out_path', type=str, default='',
                        help="输出的文件夹路径")
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    merge_datasets(**vars(opt))
