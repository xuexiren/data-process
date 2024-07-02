import argparse
import os


def generate_negative_txt(input_path, output_path):
    """
    生成负样本txt文件
    :param input_path: 输入的负样本图片的文件夹路径
    :param output_path: 输出的标签文件夹的路径
    :return:
    """
    for filename in os.listdir(input_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg")):
            # 构建生成txt文件的路径
            txt_path = os.path.join(
                output_path, os.path.splitext(filename)[0] + ".txt"
            )
            # 生成txt文件
            f = open(txt_path, "w")
            f.close()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='',
                        help="输入的负样本图片的文件夹路径")
    parser.add_argument('--out_path', type=str, default='',
                        help="输出的标签文件夹的路径")
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    generate_negative_txt(**vars(opt))
