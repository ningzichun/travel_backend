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
weather_model.load_state_dict(torch.load('travel/resources/weather2.pkl',map_location=torch.device('cpu')))
weather_model.eval()
print("\nWeather model loaded\n")

from travel.modules.Poem.codes.generate import generatePoet

print("models loaded")