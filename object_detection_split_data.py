import argparse
import os
import random
import shutil

from tqdm import tqdm


def split_data(train_rate, val_rate, test_rate, image_path, label_path, out_path):
    """
    划分训练集、验证集、测试集
    :param train_rate: 训练集的比例
    :param val_rate: 验证集的比例
    :param test_rate: 测试集的比例
    :param image_path: 输入的图片文件夹路径
    :param label_path: 输入的标签文件夹路径
    :param out_path: 输出的文件夹路径
    :return:
    """
    # 随机数种子，确保能复现
    random.seed(15)

    # 生成文件夹
    def generate_folder(flag, name, rate):
        folder_path = os.path.join(out_path, flag, name)
        if not os.path.exists(folder_path) and rate != 0.0:
            os.makedirs(folder_path)
        return folder_path

    # 打乱数据
    data = list(zip(os.listdir(image_path), os.listdir(label_path)))
    total = len(os.listdir(image_path))
    random.shuffle(data)
    each_class_image, each_class_label = zip(*data)

    # 生成对应的图片文件夹
    new_image_train_path = generate_folder("images", "train", train_rate)
    new_image_val_path = generate_folder("images", "val", val_rate)
    new_image_test_path = generate_folder("images", "test", test_rate)

    # 生成对应的标签文件夹
    new_label_train_path = generate_folder("labels", "train", train_rate)
    new_label_val_path = generate_folder("labels", "val", val_rate)
    new_label_test_path = generate_folder("labels", "test", test_rate)

    # 划分数据集
    for i in tqdm(range(len(each_class_image))):
        image = each_class_image[i]
        label = each_class_label[i]
        old_image_path = os.path.join(image_path, image)
        old_label_path = os.path.join(label_path, label)
        # 训练集
        if i < int(train_rate * total):
            shutil.copy(old_image_path, os.path.join(new_image_train_path, image))
            shutil.copy(old_label_path, os.path.join(new_label_train_path, label))
        # 验证集
        if int(train_rate * total) <= i < int((train_rate + val_rate) * total):
            shutil.copy(old_image_path, os.path.join(new_image_val_path, image))
            shutil.copy(old_label_path, os.path.join(new_label_val_path, label))
        # 测试集
        if i >= int((train_rate + val_rate) * total):
            shutil.copy(old_image_path, os.path.join(new_image_test_path, image))
            shutil.copy(old_label_path, os.path.join(new_label_test_path, label))


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_rate', type=str, default='',
                        help="训练集的比例")
    parser.add_argument('--val_rate', type=str, default='',
                        help="验证集的比例")
    parser.add_argument('--test_rate', type=str, default='',
                        help="测试集的比例")
    parser.add_argument('--image_path', type=str, default='',
                        help="输入的图片文件夹路径")
    parser.add_argument('--label_path', type=str, default='',
                        help="输入的标签文件夹路径")
    parser.add_argument('--out_path', type=str, default='',
                        help="输出的文件夹路径")
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    split_data(**vars(opt))
