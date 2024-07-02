import argparse
import os
import random
import shutil


def split_data(root_dir, train_rate, val_rate, test_rate, dataset_path):
    """
    图片分类，划分训练集、验证集、测试集
    :param root_dir: 原始图片的文件夹
    :param train_rate: 训练集的比例
    :param val_rate: 验证集的比例
    :param test_rate: 测试集的比例
    :param dataset_path: 划分好的数据集的根路径
    :return:
    """

    def generate_folder(name, rate):
        folder_path = os.path.join(dataset_path, name)
        if not os.path.exists(folder_path) and rate != 0.0:
            os.makedirs(folder_path)
        return folder_path

    # 训练集的路径
    train_path = generate_folder("train", train_rate)
    # 验证集的路径
    val_path = generate_folder("val", val_rate)
    # 测试集的路径
    test_path = generate_folder("test", test_rate)

    # 设置随机数种子
    random.seed(42)
    # 分类名称列表
    classes_list = os.listdir(root_dir)
    # 获取每个类别的图片
    for i in classes_list:
        # 每个类别的图片路径
        image_list = os.listdir(os.path.join(root_dir, i))
        # 随机打乱
        random.shuffle(image_list)
        # 训练集
        train_list = image_list[:int(train_rate * len(image_list))]
        # 验证集
        valid_list = image_list[int(train_rate * len(image_list)): int((train_rate + val_rate) * len(image_list))]
        # 测试集
        test_list = image_list[int((train_rate + val_rate) * len(image_list)):]

        if not os.path.exists(os.path.join(train_path, i)):
            os.makedirs(os.path.join(train_path, i))

        if not os.path.exists(os.path.join(val_path, i)):
            os.makedirs(os.path.join(val_path, i))

        if not os.path.exists(os.path.join(test_path, i)):
            os.makedirs(os.path.join(test_path, i))

        # 复制训练集的图片
        for j in train_list:
            shutil.copy(os.path.join(root_dir, i, j), os.path.join(train_path, i, j))
        # 复制验证集的图片
        for j in valid_list:
            shutil.copy(os.path.join(root_dir, i, j), os.path.join(val_path, i, j))
        # 复制测试集的图片
        for j in test_list:
            shutil.copy(os.path.join(root_dir, i, j), os.path.join(test_path, i, j))


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, default='',
                        help="原始图片文件夹路径")
    parser.add_argument('--train_rate', type=float, default=0.7,
                        help="训练集比例")
    parser.add_argument('--val_rate', type=float, default=0.2,
                        help="验证集比例")
    parser.add_argument('--test_rate', type=float, default=0.1,
                        help="测试集比例")
    parser.add_argument('--dataset_path', type=str, default="",
                        help="划分好的数据集的根路径")
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    split_data(**vars(opt))
