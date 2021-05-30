import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from PIL import Image, ImageFont
from travel.models import Net
font_size=35
font = ImageFont.truetype('travel/resources/kumo.ttf', 35)
print("loading models...")

#weather_model = torch.load('travel/resources/weather.pkl',map_location=torch.device('cpu'))
weather_model = Net()
weather_model.load_state_dict(torch.load('travel/resources/weather.pkl',map_location=torch.device('cpu')))
weather_model.eval()
print("\nWeather model loaded\n")

from api.modules.style.transformer_net import TransformerNet
candy = TransformerNet();candy.load_state_dict(torch.load("travel/resources/candy.pth"))
mosaic = TransformerNet();mosaic.load_state_dict(torch.load("travel/resources/mosaic.pth"))
starry_night = TransformerNet();starry_night.load_state_dict(torch.load("travel/resources/starry-night.pth"))
udnie = TransformerNet();udnie.load_state_dict(torch.load("travel/resources/udnie.pth"))
styles = {
    'candy': candy, 'mosaic': mosaic, 'starry_night': starry_night,'udnie': udnie
}
print("\Style transform model loaded\n")

from travel.modules.Poem.codes.generate import generatePoet

from photo.modules.PoolNet.networks.poolnet import build_model,weights_init
poolnet_pretrained = build_model('resnet')
poolnet_pretrained.eval()
poolnet_pretrained.apply(weights_init)
poolnet_pretrained.base.load_pretrained_model(torch.load('./travel/resources/resnet50_caffe.pth'))
poolnet_pretrained.load_state_dict(torch.load('./travel/resources/final.pth', map_location='cpu'))
poolnet_pretrained.eval()
pool_model = poolnet_pretrained

print("All models loaded")