import sys
sys.path.append('..')

import os
import numpy as np
import matplotlib.pyplot as plt
import torch
import math
import time

from tools.LoadSeq import LoadSeq

class LoadData:
    __name = 'Load Data'

    @staticmethod
    def load_scc_content_features(dir_path='I:\\yujunyi\\dataset\\SCC\\train', clz_no=-1):

        print('loading data...')

        # dataset = np.random.rand(256, 1, 128, 128)
        # labels = np.random.randint(0, 2, (256, 32, 32))

        cls_list = ['CC', 'A', 'TGM']

        dataset = []
        labels = []

        for i, cls_name in enumerate(cls_list): # 遍历每个类别
            class_path = dir_path + '/' + cls_name    # 类别地址
            label_num = 0   # 标签数量

            if i != clz_no and clz_no != -1:
                continue

            for file_name in os.listdir(class_path):   # 遍历类别文件，得到CTU
                try:
                    frames = LoadSeq.load_frame(class_path, file_name, gap=10) # 加载Y分量
                    units = LoadSeq.load_units(frames)  # 划分成CTU

                    if len(dataset) == 0:
                        dataset = units
                    else:
                        dataset = np.append(dataset, units, axis=0)

                    label_num = label_num + len(units)  # 记录标签数量
                except ValueError:
                    pass

            label = np.zeros((label_num, 32, 32), dtype=np.uint8) + i
            if len(labels) == 0:    # 生成标签
                labels = label
            else:
                labels = np.append(labels, label, axis=0)

        return torch.tensor(dataset, dtype=torch.float32) / 255, torch.tensor(labels, dtype=torch.long)
