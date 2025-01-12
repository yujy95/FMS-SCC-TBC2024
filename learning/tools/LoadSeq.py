import numpy as np
import os
import math
import matplotlib.pyplot as plt


class LoadSeq:
    __name = 'Load Frame'

    ''' 读取序列的Y分量 '''

    @staticmethod
    def load_frame(dir_path = '/Volumes/External/dataset/SCC/train', file_name='hall_352x288_420.yuv', gap=1, bit_depth=8, frame_num=0):

        data = []

        name_info = file_name[:-4].split('_')  # 文件名信息

        width, height = name_info[1].split('x')  # 视频宽高
        width = int(width)
        height = int(height)
        color_type = name_info[-1]

        if color_type == '420':
            frame_size = 1.5
        elif color_type == '422':
            frame_size = 2
        elif color_type == '444':
            frame_size = 3
        
        file_path = dir_path + '/' + file_name  # 文件地址

        with open(file_path, 'rb') as fp:
            file_size = os.path.getsize(file_path)  # 文件大小
            if frame_num == 0:
                frame_num = file_size / (width * height * frame_size)  # 帧数量

            print(file_path, ':', frame_num)
            for i in range(int(frame_num)):  # 遍历所有帧
                try:
                    if bit_depth == 8:
                        data_bytes = np.frombuffer(fp.read(int(height * width * frame_size)), 'uint8')
                    elif bit_depth == 10:
                        data_bytes = np.frombuffer(fp.read(int(height * width * frame_size)), 'uint16')

                    if i % gap == 0:  # 每x帧取1帧
                        frame_data = np.reshape(data_bytes[:height * width], (height, width))  # Y分量（二维数组）
                        data.append(frame_data)
                        # plt.imshow(frame_data)
                        # plt.show()
                except ValueError:
                    print(ValueError)
                    pass
            
        if bit_depth == 8:
            return np.array(data, dtype=np.uint8)
        elif bit_depth == 10:
            return np.array(data, dtype=np.uint16)

    ''' 将帧序列转换为CTU '''

    @staticmethod
    def load_units(frames, epoch=[0, 1], bit_depth=8, height_unit=128, width_unit=128, use_offset=True):
        
        data = []

        for i, frame in enumerate(frames): # 遍历每一帧

            if i % epoch[1] != epoch[0]:    # 间隔跳帧
                continue

            height = frame.shape[0]  # 帧高度
            width = frame.shape[1]  # 帧宽度

            height_num = math.ceil(height / height_unit)  # 高CTU个数
            width_num = math.ceil(width / width_unit)  # 宽CTU个数

            if height < height_num * height_unit:  # 0填充
                padding_pixels = np.zeros((height_num * height_unit - height, width))
                frame = np.vstack((frame, padding_pixels))
                height = height_num * height_unit
            if width < width_num * width_unit:  # 0填充
                padding_pixels = np.zeros((height, width_num * width_unit - width))
                frame = np.hstack((frame, padding_pixels))
                width = width_num * width_unit

            if use_offset:  # 偏移（由于相邻帧差距不大，使用偏移增加样本多样性）
                if i % 2 == 0:
                    offset = 0
                else:
                    offset = 64
            else:
                offset = 0

            for h in range(height_num):
                for w in range(width_num):
                    if ((h + 1) != height_num and (w + 1) != width_num) or offset == 0:
                        data_unit = frame[h * height_unit + offset: (h + 1) * height_unit + offset, w * width_unit + offset: (w + 1) * width_unit + offset]

                        # plt.imshow(data_unit)
                        # plt.show()

                        # if i == 0 and h == 0 and w == 0:
                        #     d = np.reshape(data_unit, (128 * 128))
                        #     np.savetxt('org_255.txt', d, delimiter=',')

                        data.append([data_unit])
                        data.append([data_unit.T])

        if bit_depth == 8:
            return np.array(data, dtype=np.uint8)
        elif bit_depth == 10:
            return np.array(data, dtype=np.uint16)
    
    ''' 将帧序列转换为CTU '''

    @staticmethod
    def load_units_pic(frame, height_unit=64, width_unit=64, add_dim=False):
        
        data = []

        height = frame.shape[0]  # 帧高度
        width = frame.shape[1]  # 帧宽度

        height_num = math.ceil(height / height_unit)  # 高CTU个数
        width_num = math.ceil(width / width_unit)  # 宽CTU个数

        for h in range(height_num):
            for w in range(width_num):
                if ((h + 1) != height_num and (w + 1) != width_num):
                    data_unit = frame[h * height_unit: (h + 1) * height_unit, w * width_unit: (w + 1) * width_unit]

                    # plt.imshow(data_unit)
                    # plt.show()

                    if add_dim:
                        data_unit = [data_unit]

                    data.append(data_unit)

        return np.array(data, dtype=np.uint8)

    ''' 打印视频帧 '''

    @staticmethod
    def print_seq(file_name, color_type='420', bit_depth=8):

        width = 1920
        height = 1080

        if color_type == '420':
            frame_size = 1.5
        elif color_type == '422':
            frame_size = 2
        elif color_type == '444':
            frame_size = 3

        with open(file_name, 'rb') as fp:
            file_size = os.path.getsize(file_name)  # 文件大小
            frame_num = file_size / (width * height * frame_size)  # 帧数量

            print(file_name, ':', frame_num)
            for i in range(1):  # 遍历所有帧
                try:
                    if bit_depth == 8:
                        data_bytes = np.frombuffer(fp.read(int(height * width * frame_size)), 'uint8')
                    elif bit_depth == 10:
                        data_bytes = np.frombuffer(fp.read(int(height * width * frame_size)), 'uint16')

                    frame_data = np.reshape(data_bytes[:height * width], (height, width))  # Y分量（二维数组）
                    plt.imshow(frame_data)
                    plt.show()
                except ValueError:
                    print(ValueError)
                    pass

    ''' 打印图像帧 '''

    @staticmethod
    def print_pic(file_name = 'D:\\DeepSCC\\SCC_Test\\fast_scc_net_train\\CC\\37\\luma\\1920_1080_0.bin'):

        width = 2560
        height = 1440
    
        with open(file_name, 'rb') as fp:
            data_bytes = np.frombuffer(fp.read(int(height * width)), 'uint8')
            frame_data = np.reshape(data_bytes[:height * width], (height, width))  # Y分量（二维数组）
            plt.imshow(frame_data)
            plt.show()

# LoadSeq.print_pic('E:\\yujunyi\\dataset\\SCC\\train\\Mixed\\MissionControlClip1_2560x1440_60p_8b_444.yuv')