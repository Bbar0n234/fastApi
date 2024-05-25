import torch
import torch.nn as nn

from torchvision.transforms import transforms

import torch.nn.functional as F

from PIL import Image

idx_to_cls_dict = {0: 'abraham_grampa_simpson', 1: 'agnes_skinner', 2: 'apu_nahasapeemapetilon', 3: 'barney_gumble',
                   4: 'bart_simpson', 5: 'carl_carlson', 6: 'charles_montgomery_burns', 7: 'chief_wiggum',
                   8: 'cletus_spuckler', 9: 'comic_book_guy', 10: 'disco_stu', 11: 'edna_krabappel', 12: 'fat_tony',
                   13: 'gil', 14: 'groundskeeper_willie', 15: 'homer_simpson', 16: 'kent_brockman',
                   17: 'krusty_the_clown', 18: 'lenny_leonard', 19: 'lionel_hutz', 20: 'lisa_simpson',
                   21: 'maggie_simpson', 22: 'marge_simpson', 23: 'martin_prince', 24: 'mayor_quimby',
                   25: 'milhouse_van_houten', 26: 'miss_hoover', 27: 'moe_szyslak', 28: 'ned_flanders',
                   29: 'nelson_muntz', 30: 'otto_mann', 31: 'patty_bouvier', 32: 'principal_skinner',
                   33: 'professor_john_frink', 34: 'rainier_wolfcastle', 35: 'ralph_wiggum', 36: 'selma_bouvier',
                   37: 'sideshow_bob', 38: 'sideshow_mel', 39: 'snake_jailbird', 40: 'troy_mcclure',
                   41: 'waylon_smithers'}


def conv_block(in_ch, out_ch, kernel_size=3, padding=0, pooling_size=2):
    return nn.Sequential(
        nn.Conv2d(in_channels=in_ch, out_channels=out_ch, kernel_size=kernel_size, padding=padding),
        nn.BatchNorm2d(num_features=out_ch),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=pooling_size)
    )


def linear_block(in_ch, out_ch):
    return nn.Sequential(
        nn.Linear(in_features=in_ch, out_features=out_ch),
        nn.BatchNorm1d(num_features=out_ch),
        nn.ReLU()
    )


class ModelInterface:
    def __init__(self, model_class, weights_path, idx_to_cls_dict):
        model = model_class()
        model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
        model.eval()
        self.model = model

        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor()
        ])
        self.transform = transform

        self.idx_to_cls_dict = idx_to_cls_dict

    def predict(self, image):
        with torch.no_grad():
            input_sample = self.transform(image).unsqueeze(0)
            output = self.model(input_sample)
            pred_label = self.idx_to_cls_dict[int(F.softmax(output.detach()).argmax(1))]

            return {"Prediction label": pred_label}


class BaseLineModel(nn.Module):
    def __init__(self, out_features=42):
        super().__init__()

        self.conv1 = conv_block(3, 32)

        self.conv2 = conv_block(32, 64)

        self.conv3 = conv_block(64, 128)

        self.conv4 = conv_block(128, 128)

        self.conv5 = conv_block(128, 256, padding=1)

        self.conv6 = conv_block(256, 512, padding=1)

        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.flatten = nn.Flatten()

        self.linear1 = linear_block(512, 256)

        self.linear2 = linear_block(256, 128)

        self.linear3 = nn.Linear(128, out_features)

    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)
        out = self.conv4(out)
        out = self.conv5(out)
        out = self.conv6(out)

        out = self.avg_pool(out)
        out = self.flatten(out)

        out = self.linear1(out)

        out = self.linear2(out)

        out = self.linear3(out)

        return out
