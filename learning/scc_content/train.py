import sys
sys.path.append('..')
sys.path.append('../tools')

import time

import torch
import torch.nn as nn
from torch.optim import Adam, SGD
from torch.utils.data import DataLoader, random_split
import torch.utils.data as torch_data

# import torch_directml
import numpy as np

from scc_content.CNN import CNN
from tools.Draw import Draw
from tools.LoadData import LoadData

if __name__ == '__main__':

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')  # 选择训练设备
    # device = torch_directml.device()    # 使用directML
    print(device)

    BATCH_SIZE = 1024  # batch大小
    EPOCH = 1000  # 训练次数

    ''' 定义模型 '''

    model = CNN()
    # model = torch.load('result_1000/scc_content_1000')   # 加载模型
    model.to(device)
    # print(model)

    # if torch.cuda.device_count() > 1:  # 并行GPU
    #     print('use 2 GPUs!')
    #     model = nn.DataParallel(model)

    ''' 定义损失函数和优化器 '''

    loss_func = nn.CrossEntropyLoss()  # 损失函数
    optimizer = Adam(model.parameters(), lr=0.0001)  # 优化器

    ''' 处理数据集 '''

    train_loaders = []
    test_loaders = []

    features, labels = LoadData.load_scc_content_features('E:\\Dataset\\SCC\\train')  # 加载特征

    dataset = torch_data.TensorDataset(features, labels)  # 生成数据集

    dataset_len = len(dataset)
    print('dateset size:', dataset_len)
    train_dataset, test_dataset = random_split(dataset,
                                            [int(0.8 * dataset_len), dataset_len - int(0.8 * dataset_len)],
                                            generator=torch.Generator().manual_seed(0))  # 划分训练集、测试集

    train_loaders.append(DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=1,
                            pin_memory=True))  # 加载训练集
    test_loaders.append(DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=1,
                            pin_memory=True))  # 加载测试集

    ''' 训练函数 '''

    def train(train_dataset_size, train_loader):
        model.train()  # 模型切换训练状态

        if hasattr(torch.cuda, 'empty_cache'):  # 及时清理内存
            torch.cuda.empty_cache()

        train_correct = 0
        train_loss = 0
        for X1, y in train_loader:
            out = model(X1.to(device))  # 模型的输出
            loss = loss_func(out, y.to(device))  # 计算损失值

            train_loss += loss.item() * len(X1)  # 一个batch的损失值和

            optimizer.zero_grad()  # 梯度清零
            loss.backward()  # 反向传播
            optimizer.step()  # 优化权值

            _, protected = torch.max(out, 1)  # 获取最大值位置

            train_correct += np.sum(protected.detach().cpu().numpy() == np.array(y))  # 计算准确数

        return round(train_correct / train_dataset_size, 2), round(train_loss / train_dataset_size, 2)  # 训练准确率

    ''' 测试函数 '''

    def test(test_dataset_size, test_loader):
        model.eval()  # 模型切换训练状态

        if hasattr(torch.cuda, 'empty_cache'):  # 及时清理内存
            torch.cuda.empty_cache()

        test_correct = 0
        test_loss = 0
        with torch.no_grad():
            for X1, y in test_loader:
                out = model(X1.to(device))  # 模型的输出
                loss = loss_func(out, y.to(device))  # 计算损失值

                test_loss += loss.item() * len(X1)  # 一个batch的损失值和

                _, protected = torch.max(out, 1)  # 获取最大值位置

                test_correct += np.sum(protected.detach().cpu().numpy() == np.array(y))  # 计算准确数

        return round(test_correct / test_dataset_size, 2), round(test_loss / test_dataset_size, 2)  # 训练准确率

    ''' 训练数据 '''

    history = []

    for epoch in range(EPOCH):
        print('epoch:', epoch)

        start = time.time()

        results = [0, 0, 0, 0]
        for train_loader in train_loaders:
            acc_tr, loss_tr = train(len(train_dataset), train_loader)
            results[0] += acc_tr
            results[1] += loss_tr
        for test_loader in test_loaders:
            acc_te, loss_te = test(len(test_dataset), test_loader)
            results[2] += acc_te
            results[3] += loss_te

        results[0] = round(results[0] / (32 * 32), 2)   # 平均精度
        results[2] = round(results[2] / (32 * 32), 2)

        end = time.time()

        # print('train acc:', acc_tr, ', test acc:', acc_te, round((end - start) / 60, 2), 'min')
        print('train loss:', loss_tr, ', test loss:', loss_te, round((end - start) / 60, 2), 'min')

        history.append([results[1], results[3]])

        if (epoch + 1) % 100 == 0:
            torch.save(model, 'model\\scc_content_' + str(epoch + 1))
            Draw.draw_history_acc(np.array(history), title='scc_content_' + str(epoch + 1))
