
import torch.nn as nn
from torchvision import models

class PlantDiseaseMobileNet(nn.Module):

    def __init__(self, num_classes):
        super(PlantDiseaseMobileNet, self).__init__()

        # Load pretrained MobileNetV2
        self.model = models.mobilenet_v2(
            weights=models.MobileNet_V2_Weights.DEFAULT
        )

        # Freeze pretrained feature layers
        for param in self.model.features.parameters():
            param.requires_grad = False

        # Replace final classification layer
        input_features = self.model.classifier[1].in_features

        self.model.classifier[1] = nn.Linear(
            input_features,
            num_classes
        )

    def forward(self, x):
        return self.model(x)
