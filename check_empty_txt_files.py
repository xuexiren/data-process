import argparse
import os


def check_empty_txt_files(folder_path):
    """
    判断文件夹中的txt文件是否为空
    :param folder_path: txt文件夹的路径
    :return:
    """

    def is_txt_file_empty(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return not content.strip()

    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)

        if is_txt_file_empty(file_path):
            # 删除该文件
            os.remove(file_path)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path', type=str, default='',
                        help="输入的标签文件夹路径")
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    check_empty_txt_files(**vars(opt))
