import pydicom
from PIL import Image
import numpy as np
from torchvision import transforms
from torch.utils.data import DataLoader

# services
from swagger_server.services.orthanc_service import orthancClient
from swagger_server.services.segmentation.utils import MaskDataset
from swagger_server.services.segmentation.unet import init_model

# logger
from swagger_server import logger



def auto_segment(id):
    # parse data
    dcm_file = orthancClient.download_dicom_by_id(instance_id=id)
    pil_instance = Image.fromarray(convert_dcm_to_image(dcm_file))

    # apply unet
    unet = init_model()
    val_dataset = MaskDataset(pil_instance)
    val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)
    tensor_instance = iter(val_loader).next()
    tensor_mask = unet(tensor_instance)

    # convert result
    pil_mask = make_black_transparent(tensor_to_image(tensor_mask))
    np_mask = np.array(pil_mask)
    mask_shape = np_mask.shape

    # find border pixels
    border_pixels = find_border(np_mask, mask_shape)
    return sort_border_pixel_by_pen(border_pixels)


def sort_border_pixel_by_pen(mass):
    n = len(mass)
    used = [False] * n
    v = 0
    INF = 512 * 512
    new_arr = []
    big_arr = []
    first = v
    av_s = 0
    av_k = 0
    for i in range(n):
        new_arr.append(mass[v][1])
        new_arr.append(mass[v][0])
        used[v] = True
        to = -1
        min_dist = INF
        for j in range(n):
            if not used[j] and min_dist > abs(mass[v][0] - mass[j][0]) + abs(mass[v][1] - mass[j][1]):
                min_dist = abs(mass[v][0] - mass[j][0]) + abs(mass[v][1] - mass[j][1])
                to = j
        if av_s < (min_dist - 10) * av_k:
            new_arr.append(mass[first][1])
            new_arr.append(mass[first][0])
            if len(new_arr) > 10:
                big_arr.append(new_arr[:])
            new_arr.clear()
            first = to
            av_s = 0
            av_k = 0

        av_s += min_dist
        av_k += 1
        v = to
    return big_arr


def find_border(np_mask, mask_shape):
    mass = []
    for i in range(1, mask_shape[0] - 1):
        for j in range(1, mask_shape[1] - 1):
            if sum(np_mask[i][j]) > 0:
                if sum(np_mask[i - 1][j]) == 0 or sum(np_mask[i][j - 1]) == 0 or sum(np_mask[i][j + 1]) == 0 or sum(
                        np_mask[i + 1][j]) == 0:
                    mass.append([i, j])

    return mass


def tensor_to_image(tensor_img):
    resize_F = transforms.Resize((512, 512))
    img = resize_F(tensor_img).cpu().detach().numpy()[0]
    # convert image back to Height,Width,Channels
    img = np.transpose(img, (1, 2, 0)).squeeze()

    # dim = np.zeros((224,224))
    # img = np.stack((img,dim, dim), axis=2)

    return Image.fromarray((img * 255).astype(np.uint8)).convert("RGBA")


def make_black_transparent(img, conf=100):
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] < conf and item[1] < conf and item[2] < conf:
            newData.append((0, 0, 0, 0))
        elif item[0] > 0 and item[1] > 0 and item[2] > 0:
            newData.append((item[0], 0, 0, 255))
        else:
            newData.append(item)

    img.putdata(newData)
    return img


def convert_dcm_to_image(dcm_file):
    ds = pydicom.dcmread(dcm_file)

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    return image_2d_scaled
