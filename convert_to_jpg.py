import argparse
import os

from PIL import Image
from tqdm import tqdm


def convert_to_jpg(input_path, output_path):
    """
    图片转jpg格式
    :param input_path: 输入的文件夹路径
    :param output_path: 输出的文件夹路径
    :return:
    """
    for filename in tqdm(os.listdir(input_path)):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg")):
            # 构建输入和输出文件的完整路径
            input_image_path = os.path.join(input_path, filename)
            output_image_path = os.path.join(
                output_path, os.path.splitext(filename)[0] + ".jpg"
            )
            image = Image.open(input_image_path)
            rgb_im = image.convert("RGB")
            rgb_im.save(output_image_path)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='',
                        help="输入的图片文件夹路径")
    parser.add_argument('--out_path', type=str, default='',
                        help="输出的图片文件夹路径")
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    convert_to_jpg(**vars(opt))
