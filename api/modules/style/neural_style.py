import numpy as np
import torch
from PIL import Image
from torch.autograd import Variable

from api.modules.style import utils
from api.modules.style.transformer_net import TransformerNet

def stylize(content_image,style_model):
    content_image = utils.tensor_load_rgbimage(content_image)
    content_image = content_image.unsqueeze(0)
    with torch.no_grad():
        content_image = Variable(utils.preprocess_batch(content_image))

    output = style_model(content_image)
    return utils.tensor_save_bgrimage(output.data[0])


def main():
    content_scale = 1
    while(1):
        content_image = input("input image: ")
        img = Image.open(content_image)
        output_image = content_image+".out.jpg"
        stylize(content_image,output_image,content_scale).save(output_image)

if __name__ == "__main__":
    main()
