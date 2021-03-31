import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from PIL import Image
class Net(nn.Module):
    # 定义初始化方法
    def __init__(self):
        # 继承父类所有属性
        super().__init__()
        # 彩色图片故输入channel为3 16为卷积核个数则会形成16通道(图层) 3为3*3的卷积核.
        # nn.Conv2d()适合图片
        self.conv1 = nn.Conv2d(3, 16, 3, )
        # nn.BatchNorm2d()适合图片 16是上一层的输出
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, 3, )
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 64, 3, )
        self.bn3 = nn.BatchNorm2d(64)
        self.conv4 = nn.Conv2d(64, 128, 3)
        self.bn4 = nn.BatchNorm2d(128)
        # droput是随机丢弃掉一部分神经元(的输出)来抑制过拟合
        # 添加Dropout层
        # nn.Dropout()适合Linear
        self.drop = nn.Dropout(0.5)
        # nn.Dropout2d()适合图片
        self.drop2d = nn.Dropout2d(0.5)
        # nn.Dropout2d()适合三维数据
        self.pool = nn.MaxPool2d((2, 2))
        self.fc1 = nn.Linear(128 * 4 * 4, 1024)
        self.bn_f1 = nn.BatchNorm1d(1024)
        self.fc2 = nn.Linear(1024, 256)
        self.bn_f2 = nn.BatchNorm1d(256)
        self.fc3 = nn.Linear(256, 4)

    def forward(self, input):
        x = F.relu(self.conv1(input))
        x = self.bn1(x)
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.bn2(x)
        x = self.pool(x)
        x = F.relu(self.conv3(x))
        x = self.bn3(x)
        x = self.pool(x)
        x = F.relu((self.conv4(x)))
        x = self.bn4(x)
        x = self.pool(x)
        x = self.drop2d(x)
        # print(x.shape)
        # 会输出torch.Size([64, 128, 4, 4])
        x = x.view(-1, 128 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = self.bn_f1(x)
        # Dropout一般在BN层之后
        x = self.drop(x)
        x = F.relu(self.fc2(x))
        x = self.bn_f2(x)
        x = self.drop(x)
        x = self.fc3(x)
        return x
