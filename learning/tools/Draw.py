import matplotlib.pyplot as plt


class Draw:
    __name = 'Draw'

    @staticmethod
    def draw_history(history, title='Train_Process'):
        process_ignore = 0  # 忽略前面轮次的数据

        train_acc = history[:, 0]
        train_loss = history[:, 1]
        test_acc = history[:, 2]
        test_loss = history[:, 3]

        for i in range(len(train_acc)):  # 处理异常值
            if train_loss[i] - train_loss[i - 1] > 1:
                train_loss[i] = train_loss[i - 1] + 1
            if test_loss[i] - test_loss[i - 1] > 1:
                test_loss[i] = test_loss[i - 1] + 1

        plt.clf()
        plt.plot(train_acc[process_ignore:])  # 训练集精确度二维坐标
        plt.plot(test_acc[process_ignore:])  # 测试集精确度二维坐标
        plt.plot(train_loss[process_ignore:])  # 训练集损失值二维坐标
        plt.plot(test_loss[process_ignore:])  # 测试集损失值二维坐标
        plt.title(title)
        plt.ylabel('Acc & Loss')  # y坐标：精确度
        plt.xlabel('Epoch')  # x坐标：轮次
        plt.legend(['train_acc', 'test_acc', 'tran_loss', 'test_loss'], loc='upper right')  # 图例
        plt.savefig(title + '.png')

    @staticmethod
    def draw_history_acc(history, title='Train_Process'):
        process_ignore = 0  # 忽略前面轮次的数据

        train_loss = history[:, 0]
        test_loss = history[:, 1]
        
        plt.clf()
        plt.plot(train_loss[process_ignore:])  # 训练集损失值二维坐标
        plt.plot(test_loss[process_ignore:])  # 测试集损失值二维坐标
        plt.title(title)
        plt.ylabel('Loss')  # y坐标：精确度
        plt.xlabel('Epoch')  # x坐标：轮次
        plt.legend(['tran_loss', 'test_loss'], loc='upper right')  # 图例
        plt.savefig(title + '.png')
