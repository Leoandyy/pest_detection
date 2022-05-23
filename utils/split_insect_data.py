# coding:utf-8

import os
from shutil import copy, rmtree
import random

def mk_file(file_path : str):
    if os.path.exists(file_path):
        #如果文件夹存在，则重新创建文件夹
        rmtree(file_path)
    os.makedirs(file_path)

def main():
    random.seed(0)
    valid_split_rate = 0.2
    test_split_rate = 0.1
    
    cwd = os.getcwd()
    data_root = os.path.join(cwd, "ip102_v1.1")
    origin_insect_path = os.path.join(data_root, "now_img")
    assert os.path.exists(origin_insect_path), "path '{}' does not exist.".format(origin_insect_path)

    insect_class = [cla for cla in os.listdir(origin_insect_path)
                    if os.path.isdir(os.path.join(origin_insect_path, cla))]
    
    train_root = os.path.join(data_root, "train")
    mk_file(train_root)
    for cla in insect_class:
        mk_file(os.path.join(train_root, cla))
    
    val_root = os.path.join(data_root, "validation")
    mk_file(val_root)
    for cla in insect_class:
        mk_file(os.path.join(val_root, cla))
        
    test_root = os.path.join(data_root, "test")
    mk_file(test_root)
    for cla in insect_class:
        mk_file(os.path.join(test_root, cla))

    for cla in insect_class:
        cla_path = os.path.join(origin_insect_path, cla)
        images = os.listdir(cla_path)
        num = len(images)

        eval_index = random.sample(images, k=int(num*valid_split_rate))
        for index, image in enumerate(images):
            if image in eval_index:
                image_path = os.path.join(cla_path, image)
                new_path = os.path.join(val_root, cla)
                copy(image_path, new_path)
                images.remove(image)
        num = len(images)
        test_index = random.sample(images, k=int(num*test_split_rate))
        for index, image in enumerate(images):
            if image in test_index:
                image_path = os.path.join(cla_path, image)
                new_path = os.path.join(test_root, cla)
                copy(image_path, new_path)
            else:
                image_path = os.path.join(cla_path, image)
                new_path = os.path.join(train_root, cla)
                copy(image_path, new_path)
            print("\r[{}] processing [{}/{}]".format(cla, index+1, num))
        print()
    print("processing done!")

if __name__ == '__main__':
    main()
