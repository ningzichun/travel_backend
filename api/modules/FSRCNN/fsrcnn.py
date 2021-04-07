import argparse

import torch
import torch.backends.cudnn as cudnn
import numpy as np
import PIL.Image as pil_image

from .models import FSRCNN
from .utils import convert_ycbcr_to_rgb, preprocess, calc_psnr


def itFSRCNN(image,scale):
    if scale==4:
        weights_file='./travel/resources/fsrcnn_x4.pth'
    elif scale==3:
        weights_file='./travel/resources/fsrcnn_x3.pth'
    elif scale==2:
        weights_file='./travel/resources/fsrcnn_x2.pth'

    cudnn.benchmark = True
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    model = FSRCNN(scale_factor=scale).to(device)

    state_dict = model.state_dict()
    for n, p in torch.load(weights_file, map_location=lambda storage, loc: storage).items():
        if n in state_dict.keys():
            state_dict[n].copy_(p)
        else:
            raise KeyError(n)

    model.eval()

    #image = pil_image.open(image_file).convert('RGB')

    image_width = image.width
    image_height = image.height

    lr = image  #原图片
    bicubic = lr.resize((lr.width * scale, lr.height * scale), resample=pil_image.BICUBIC)    #bicubic放大

    lr, _ = preprocess(lr, device)
    _, ycbcr = preprocess(bicubic, device)

    with torch.no_grad():
        preds = model(lr).clamp(0.0, 1.0)

    preds = preds.mul(255.0).cpu().numpy().squeeze(0).squeeze(0)

    output = np.array([preds, ycbcr[..., 1], ycbcr[..., 2]]).transpose([1, 2, 0])
    output = np.clip(convert_ycbcr_to_rgb(output), 0.0, 255.0).astype(np.uint8)
    output = pil_image.fromarray(output)
    return output

