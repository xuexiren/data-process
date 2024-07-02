import os

import cv2
from tqdm import tqdm
import argparse


def extract_images(fps, input_path, out_path):
    """
    视频抽帧
    :param fps: 抽帧的间隔
    :param input_path: 输入的视频文件夹路径
    :param out_path: 输出的文件夹路径
    :return:
    """
    video_path_list = []
    for file in os.listdir(input_path):
        if file.lower().endswith((".mp4", ".avi", ".flv", ".m4v", ".webm")):
            video_path_list.append(file)
    # 视频抽帧
    for video_path in tqdm(video_path_list):
        # 视频名字
        video_name = os.path.splitext(video_path)[0]
        # 新建文件夹
        output_path = os.path.join(out_path, video_name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # 打开视频
        cap = cv2.VideoCapture(os.path.join(input_path, video_path))
        # 设置帧间隔
        frame_interval = int(fps)
        # 逐帧提取并保存
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if count % frame_interval == 0:
                    image_name = os.path.join(output_path, f"{video_name}_{count}.jpg")
                    cv2.imencode(".jpg", frame)[1].tofile(image_name)
                count += 1
            else:
                break
        cap.release()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', default=25, type=int,
                        help="抽帧的间隔")
    parser.add_argument('--input_path', type=str, default='',
                        help="输入的视频文件夹路径")
    parser.add_argument('--out_path', type=str, default='',
                        help="输出的图片文件夹路径")
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    extract_images(**vars(opt))

