# coding:utf-8

import os
import json

import torch
from torchvision import transforms
from model import resnet34
from PIL import Image
# import matplotlib.pyplot as plt


def main(path):
    data_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # load image
    img_root = os.path.join(os.getcwd(), "..")
    img_path = os.path.join(img_root, "data_set", "flower_data", path)
    assert os.path.exists(img_path), "file: '{}' does not exist.".format(img_path)
    img = Image.open(img_path)
    # plt.imshow(img)
    img = data_transform(img)
    img = torch.unsqueeze(img, dim=0)

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' does not exist.".format(json_path)

    json_file = open(json_path, "r")
    class_indict = json.load(json_file)

    # create model
    model = resnet34(num_classes=5)

    # load model weights
    weights_path = "resNet34_flower.pth"
    assert os.path.exists(weights_path), "file:'{}' does not exist.".format(weights_path)
    model.load_state_dict(torch.load(weights_path))

    # prediction
    model.eval()
    with torch.no_grad():
        output = torch.squeeze(model(img))
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()

    print_res = "class: {}  prob: {:.3}".format(class_indict[str(predict_cla)], predict[predict_cla].numpy())
    # plt.title(print_res)

    for i in range(len(predict)):
        print("class: {:10}  prob: {:.3f}".format(class_indict[str(i)], predict[i].numpy()))
    # plt.show()


if __name__ == '__main__':
    main("44.png")
