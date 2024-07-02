import argparse
import os
import shutil


def find_different(input_path, compare_path, move_path):
    """
    比较两个文件夹不同的文件
    :param input_path: 输入的文件夹路径
    :param compare_path: 要比较的文件夹路径
    :param move_path: 要移动到的文件夹路径
    :return:
    """
    # 要比较的文件夹里的文件名前缀
    compare_folder_name = [
        os.path.splitext(x)[0] for x in os.listdir(compare_path)
    ]
    different_folder = []
    # 循环遍历输入的文件，找到文件名不在要比较文件夹里的文件
    for i in os.listdir(input_path):
        if os.path.splitext(i)[0] not in compare_folder_name:
            different_folder.append(i)
    for i in different_folder:
        old_file_path = os.path.join(input_path, i)
        new_file_path = os.path.join(move_path, i)
        shutil.move(old_file_path, new_file_path)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='',
                        help="输入的文件夹路径")
    parser.add_argument('--compare_path', type=str, default='',
                        help="要比较的文件夹路径")
    parser.add_argument('--move_path', type=str, default='',
                        help="要将不同的文件移动到的文件夹的路径")
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    find_different(**vars(opt))
