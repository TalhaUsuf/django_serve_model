from torchvision import models, transforms
from torchsummary import summary
import torch
from PIL import Image
import numpy as np
import os

# MODEL_PATH = os.environ["MODEL_PATH"]


class extract_features:
    def __init__(self, resize : int = 256, imagesize : int = 224):
        self.resize = resize
        self.sz = imagesize
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = models.resnet101(pretrained=True).to(self.device)
        self.pre_process = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        # self.preprocess_img()
        # self.predict()



    def preprocess_img(self, pth):

        self.img = torch.unsqueeze(self.pre_process(Image.open(pth)), 0).to(self.device)
        
    def predict(self, pth):
        self.preprocess_img(pth)
        with torch.no_grad():
            
            output = self.model(self.img)
            output = output.detach().cpu().numpy()
            output = np.squeeze(output).tolist()

            return output




