import torch.nn as nn
import timm

class GlaucomaDiagnoser(nn.Module):
    def __init__(self, num_classes=3, base_model='resnet18'):
        super(GlaucomaDiagnoser, self).__init__()
        self.base_model = timm.create_model(base_model, pretrained=True)
        self.features = nn.Sequential(
            *list(self.base_model.children())[:-1],
            nn.Dropout(p=0.3) 
        )

        output_sizes = {
            'resnet18': 512,
            'resnet50': 2048,
            'efficientnet_b4': 1792
        }
        
        if base_model in output_sizes:
            out_size = output_sizes[base_model]
        else:
            raise ValueError(f"Unsupported base model: {base_model}")

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(out_size, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        output = self.classifier(x)
        return output
    