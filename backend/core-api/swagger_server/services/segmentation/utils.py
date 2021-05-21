from torchvision import transforms
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import numpy as np
from PIL import Image

from config import Config

PRETRAINED_IMG_SIZE = Config.PRETRAINED_IMG_SIZE

class MaskDataset(Dataset):
  def __init__(self, im):
    self.im = im
    self.transform = transforms.Compose([transforms.Resize((PRETRAINED_IMG_SIZE, PRETRAINED_IMG_SIZE)), transforms.ToTensor()])

  def __getitem__(self, i):
    return self.transform(self.im)

  def __len__(self):
    return 1