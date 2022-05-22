import shutil

import cv2
import os
import time


class dup_picture:
    def __init__(self):
        self.orb = cv2.ORB_create()
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    def get_pic_desc(self, img1_path: str):
        img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)  # 读取灰度图片
        kp1, des1 = self.orb.detectAndCompute(img1, None)
        return des1

    def get_similary(self, des1, des2):
        # knn筛选结果
        matches = self.bf.knnMatch(des1, trainDescriptors=des2, k=2)
        # 查看最大匹配点数目
        good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]

        if len(matches) == 0:
            return 0
        similary = len(good) / len(matches)
        return similary


def quchong(file_path):
    t1 = time.time()
    duptool = dup_picture()
    # file_path = r"D:\害虫识别数据集\ceshi"
    file_list = os.listdir(file_path)
    file_list = list(filter(lambda x: x.endswith(".jpg"), file_list))  # must .jpg pic
    os.chdir(file_path)
    # 创建文件夹
    temp_file_path = file_path + './重复'
    os.makedirs(temp_file_path)

    unique_list = [duptool.get_pic_desc(file_list[0]), ]
    cnt = 0
    for k, file in enumerate(file_list[1:]):
        print(k)
        des = duptool.get_pic_desc(file)
        if des is None:
            shutil.copyfile(file_path + '\\' + file, temp_file_path + '\\' + file)
            os.remove(file)
            continue
        # 遍历unique_list来比较
        for des_i in unique_list:
            if duptool.get_similary(des, des_i) > 0.5:
                shutil.copyfile(file_path + '\\' + file, temp_file_path + '\\' + file)
                os.remove(file)
                print(file)
                break
            # 没有匹配的就加入
        # else:  # Smooth and uninterrupted execution completed
        if cnt <= 800:
            unique_list.append(des)
            cnt += 1
        # if k==1600 or k==3200 or k==4800:
        #     cnt=0
        #     unique_list = [duptool.get_pic_desc(file_list[0]), ]

    t2 = time.time()
    print(file_path, '已经完成')
    print("用时", t2 - t1)


if __name__ == "__main__":
    filepath = r'D:\害虫识别数据集\now_img\lou_gu_太多了跑不了'
    quchong(filepath)

# if __name__ == '__main__':
#     t1 = time.time()
#     duptool = dup_picture()
#     file_path = r"D:\害虫识别数据集\ceshi"
#     file_list = os.listdir(file_path)
#     file_list = list(filter(lambda x: x.endswith(".jpg"), file_list))  # must .jpg pic
#     os.chdir(file_path)
#     # 创建文件夹
#     temp_file_path = file_path + './重复'
#     os.makedirs(temp_file_path)
#
#     unique_list = [duptool.get_pic_desc(file_list[0]), ]
#     for k, file in enumerate(file_list[1:]):
#         print(k)
#         des = duptool.get_pic_desc(file)
#         if des is None:
#             shutil.copyfile(file_path + '\\' + file, temp_file_path + '\\' + file)
#             os.remove(file)
#             continue
#         # 遍历unique_list来比较
#         for des_i in unique_list:
#             if duptool.get_similary(des, des_i) > 0.5:
#                 shutil.copyfile(file_path + '\\' + file, temp_file_path + '\\' + file)
#                 os.remove(file)
#                 print(file)
#                 break
#         # 没有匹配的就加入
#         else:  # Smooth and uninterrupted execution completed
#             unique_list.append(des)
#
#     t2 = time.time()
#     print("用时", t2 - t1)
