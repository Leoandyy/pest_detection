# coding:utf-8

import os
import json
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
from matplotlib import pyplot as plt
from tqdm import tqdm
from model import resnet34

def write_json(cla, root):
    json_str = json.dumps(cla)
    with open(root, 'w') as f:
        json_file = f.write(json_str)

def main():
    data_transform = {
        "train": transforms.Compose([transforms.RandomResizedCrop(224),
                                     transforms.RandomHorizontalFlip(),
                                     transforms.ToTensor(),
                                     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
        "val": transforms.Compose([transforms.Resize(256),
                                   transforms.CenterCrop(225),
                                   transforms.ToTensor(),
                                   transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    }

    # 打开上一层的文件夹
    data_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    image_path = os.path.join(data_root, "data_set", "insect_data")
    assert os.path.exists(image_path), "{} path does not exist.".format(image_path)
    train_dataset = datasets.ImageFolder(root=os.path.join(image_path, "train"),
                                         transform=data_transform["train"])
    train_num = len(train_dataset)

    # {'daisy':0, 'dandelion':1, 'roses':2, 'sunflower':3, 'tulips':4}
    flower_list = train_dataset.class_to_idx
    cla_dict = dict((val, key) for key, val in flower_list.items())

    json_str = json.dumps(cla_dict, indent=31)
    with open('class_indices.json', 'w') as json_file:
        json_file.write(json_str)

    batch_size = 64
    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=batch_size, shuffle=True,
                                               num_workers=1)

    validate_dataset = datasets.ImageFolder(root=os.path.join(image_path, "validation"),
                                            transform=data_transform["val"])
    val_num = len(validate_dataset)
    validate_loader = torch.utils.data.DataLoader(validate_dataset,
                                                  batch_size=batch_size, shuffle=True,
                                                  num_workers=0)

    net = resnet34()
    model_weight_path = "./resnet34-pre.pth"
    assert os.path.exists(model_weight_path), "file {} does not exist.".format(model_weight_path)
    net.load_state_dict(torch.load(model_weight_path))

    # change fc layer structure
    in_channel = net.fc.in_features
    net.fc = nn.Linear(in_channel, 31)

    loss_function = nn.CrossEntropyLoss()
    params = [p for p in net.parameters() if p.requires_grad]
    optimizer = optim.Adam(params, lr=0.0001)

    epochs = 30
    best_acc = 0.0
    cla_loss, cla_acc = {}, {}
    index = 0
    save_path = 'resNet34_insect.pth'
    train_steps = len(train_loader)
    for epoch in range(epochs):
        # train
        net.train()
        running_loss = 0.0
        train_bar = tqdm(train_loader, file=sys.stdout)
        for step, data in enumerate(train_bar):
            images, labels = data
            optimizer.zero_grad()
            logits = net(images)
            loss = loss_function(logits, labels)
            loss.backward()
            optimizer.step()
            index += 1
            cla_loss['{0:d}'.format(index)] = loss
            running_loss += loss.item()
            train_bar.desc = "train epoch[{}/{}] loss:{:.3f}".format(epoch + 1, epochs, loss)

        # validate
        net.eval()
        acc = 0.0
        with torch.no_grad():
            val_bar = tqdm(validate_loader, file=sys.stdout)
            for val_data in val_bar:
                val_images, val_labels = val_data
                outputs = net(val_images)
                predict_y = torch.max(outputs, dim=1)[1]
                acc += torch.eq(predict_y, val_labels).sum().item()
                val_bar.desc = "valid epoch[{}/{}]".format(epoch + 1, epochs)
        val_accurate = acc / val_num
        cla_acc['{0:d}'.format(epoch + 1)] = val_accurate
        print('[epoch %d] train_loss: %.3f val_accuracy: %.3f' % (epoch + 1, running_loss / train_steps, val_accurate))

        if val_accurate > best_acc:
            best_acc = val_accurate
            torch.save(net.state_dict(), save_path)
    write_json(cla_loss, 'train_loss.json')
    write_json(cla_acc, 'valid_acc.json')
    print('Finished Training')


if __name__ == '__main__':
    main()
