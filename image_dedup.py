import argparse
import os
import shutil

from imagededup.methods import CNN


def image_dedup(input_path, move_path, threshold):
    """
    图片去重
    :param input_path: 输入的文件夹路径
    :param move_path: 移动的文件夹路径
    :param threshold: 比较的阈值
    :return:
    """
    # 设置编码器
    my_encoder = CNN()
    duplicates = my_encoder.find_duplicates_to_remove(image_dir=input_path,
                                                      min_similarity_threshold=threshold)
    for i in duplicates:
        shutil.move(os.path.join(input_path, i), os.path.join(move_path, i))


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='',
                        help="输入的文件夹路径")
    parser.add_argument('--move_path', type=str, default='',
                        help="移动的文件夹路径")
    parser.add_argument('--threshold', type=float, default=0.9,
                        help="比较的阈值")
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    image_dedup(**vars(opt))
