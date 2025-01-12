import torch.nn as nn
import torch


class CNN(nn.Module):


    def __init__(self, cls_num=3):
        super(CNN, self).__init__()

        # input:128*128*1
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=16)
        )

        # input:64*64*16
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=32)
        )

        # input:32*32*32
        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=64)
        )

        # input:16*16*64
        self.conv4 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=128)
        )

        # input:8*8*128
        self.conv5 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=256)
        )

        # input:4*4*256
        self.conv6 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=512)
        )

        # input:2*2*512,output:1*1*1024
        self.conv7 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=1024, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=1024)
        )

        # input:1*1*1024
        self.deconv1 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=1024, out_channels=512, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=512)
        )

        # input:2*2*1024
        self.deconv2 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=1024, out_channels=256, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=256)
        )

        # input:4*4*512
        self.deconv3 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=512, out_channels=128, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=128)
        )

        # input:8*8*256
        self.deconv4 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=256, out_channels=64, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=64)
        )

        # input:16*16*128,output:32*32*32
        self.deconv5 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=128, out_channels=32, kernel_size=2, stride=2),
            nn.ReLU(),
            # nn.BatchNorm2d(num_features=32)
        )

        # input:32*32*64, output:32*32*cls_num
        self.conv8 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=cls_num, kernel_size=1, stride=1),
            nn.Softmax(dim=1)
        )

        for m in self.children():  # 初始化参数（正态分布）
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
                nn.init.normal_(m.weight)
                nn.init.normal_(m.bias)

    def forward(self, x):
        x1 = self.conv1(x)                  # output:64*64*16
        x2 = self.conv2(x1)                 # output:32*32*32
        x3 = self.conv3(x2)                 # output:16*16*64
        x4 = self.conv4(x3)                 # output:8*8*128
        x5 = self.conv5(x4)                 # output:4*4*256
        x6 = self.conv6(x5)                 # output:2*2*512
        x7 = self.conv7(x6)                 # output:1*1*1024

        dx1 = self.deconv1(x7)              # output:2*2*512
        dx2 = self.deconv2(torch.cat((dx1, x6), 1)) # output:4*4*256
        dx3 = self.deconv3(torch.cat((dx2, x5), 1)) # output:8*8*128
        dx4 = self.deconv4(torch.cat((dx3, x4), 1)) # output:16*16*64
        dx5 = self.deconv5(torch.cat((dx4, x3), 1)) # output:32*32*32

        x8 = self.conv8(torch.cat((dx5, x2), 1))    # output:32*32*cls_num

        return x8