import sys
sys.path.append('..')
sys.path.append('../tools')

import torch
import numpy as np
import matplotlib.pyplot as plt
from tools.LoadData import LoadData
from torch.utils.data import DataLoader
import torch.utils.data as torch_data

if __name__ == '__main__':

    cls_list = ['CC', 'A', 'TGM']
    cls_no = [0, 1, 2]
    cls_pre = 0

    BATCH_SIZE = 4096  # batch大小

    device = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')  # 选择训练设备
    print(device)

    # model = torch.jit.load('H:\\yujunyi\\SCC_Test\\deep_learning\\scc_content_300.pt')   # 加载模型
    model = torch.load('model\\scc_content_100')   # 加载模型
    model.to(device)

    features, labels = LoadData.load_scc_content_features('H:\\yujunyi\\dataset\\SCC\\test2', clz_no=cls_pre)  # 加载特征
    dataset = torch_data.TensorDataset(features, labels)  # 生成数据集

    test_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=1, pin_memory=True)  # 加载训练集

    def test_out():
        model.eval()  # 模型切换训练状态

        if hasattr(torch.cuda, 'empty_cache'):  # 及时清理内存
            torch.cuda.empty_cache()

        resualt = []
        with torch.no_grad():
            for i, (X1, y) in enumerate(test_loader):
                out = model(X1.to(device))  # 模型的输出

                if len(resualt) == 0:
                    resualt = out[:, cls_no[cls_pre], :, :].flatten().detach().cpu().numpy()
                else:
                    resualt = np.append(resualt, out[:, cls_no[cls_pre], :, :].flatten().detach().cpu().numpy())

        return resualt  # 训练准确率
    
    def test_cor():
        model.eval()  # 模型切换训练状态

        if hasattr(torch.cuda, 'empty_cache'):  # 及时清理内存
            torch.cuda.empty_cache()

        test_correct = 0
        test_len = 0
        with torch.no_grad():
            for i, (X1, y) in enumerate(test_loader):
                out = model(X1.to(device))  # 模型的输出

                # if i == 0:
                #     print(out[0])

                _, protected = torch.max(out, 1)  # 获取最大值位置
                test_correct += np.sum(protected.detach().cpu().numpy() == np.array(y))  # 计算准确数
                test_len += len(out)

        return test_correct / (test_len * 32 * 32)  # 训练准确率

    # pic_name = cls_list[cls_pre]
    # plt.hist(test_out(), bins=100)
    # plt.title(pic_name)
    # plt.savefig('result_' + pic_name + '_' + cls_list[cls_no[cls_pre]] + '.png')
    print(test_cor())
