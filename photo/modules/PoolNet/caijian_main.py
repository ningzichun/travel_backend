import argparse
import os
from .dataset.dataset import get_loader
from .solver import Solver


class pic_config:
    def __init__(self,_test_root,_test_list):
        resnet_path = './photo/modules/PoolNet/model/resnet50_caffe.pth'
        self.n_color=3
        self.lr=5e-5
        self.wd=0.0005
        self.arch='resnet'
        self.pretrained_model=resnet_path
        self.epoch=24
        self.batch_size=1
        self.num_thread=1
        self.load=''
        self.epoch_save=3
        self.iter_size=10
        self.show_every=50
        self.test_root=_test_root
        self.test_list=_test_list
        self.model='./photo/modules/PoolNet/model/final.pth'
        self.mode='test'
        self.cuda=0

def main(config):
    if config.mode == 'test':
        test_loader = get_loader(config, mode='test')
        #if not os.path.exists(config.test_fold): os.mkdir(config.test_fold)
        test = Solver(None, test_loader, config)
        src=test.test()
        return src
    else:
        raise IOError("illegal input!!!")

def get_cv(path,name):
    configs=pic_config(path,name)

    box=main(configs)
    return box


