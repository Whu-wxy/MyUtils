import cv2
from os import path
import os


file_name1 = r'E:\video\20190624-154745.264'
file_name2 = r'E:\video\CCTV)20190623-163409.264'

def video2img(file_name, frame_number=60):
    name = path.basename(file_name).split('.')[0]
    save_path = path.dirname(file_name) + '\\' + name + '\\'
    if os.path.exists(save_path) == False:    #在视频同级目录下创建文件夹
        os.mkdir(save_path)

    vc = cv2.VideoCapture(file_name)  # 读入视频文件
    c = 1

    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False

    timeF = frame_number  # 视频帧计数间隔频率

    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        if (c % timeF == 0):  # 每隔timeF帧进行存储操作
            cv2.imwrite(save_path + str(c) + '.jpg', frame)  # 存储为图像
        c = c + 1
        cv2.waitKey(1)
    vc.release()

video2img(file_name1)
video2img(file_name2)

print('All Finished!')