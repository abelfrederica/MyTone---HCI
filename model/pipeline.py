import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
import timm

# =========================
# CLASS LABELS
# =========================

classes = [
    "Autumn",
    "Spring",
    "Summer",
    "Winter"
]

# =========================
# MODEL ARCHITECTURE
# =========================

class FARLClassifier(nn.Module):

    def __init__(self):

        super().__init__()

        self.backbone = timm.create_model(
            "vit_base_patch16_224",
            pretrained=False,
            num_classes=0,
            global_pool="avg"
        )

        self.head = nn.Sequential(

            nn.ReLU(inplace=True),

            nn.Dropout(p=0.5),

            nn.Linear(768, 256),

            nn.ReLU(inplace=True),

            nn.Dropout(p=0.5),

            nn.Linear(256, 4)
        )

    def forward(self, x):

        feats = self.backbone(x)

        if isinstance(feats, (list, tuple)):
            feats = feats[0]

        if feats.ndim > 2:
            feats = torch.flatten(feats, 1)

        return self.head(feats)

# =========================
# LOAD MODEL
# =========================
model = FARLClassifier()

checkpoint = torch.load(
    "model/weights/best_farl64_classifier.pt",
    map_location="cpu"
)
model.load_state_dict(checkpoint["model_state"], strict=False)

model.eval()

# =========================
# IMAGE TRANSFORM
# =========================

transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# =========================
# PREDICTION FUNCTION
# =========================
def predict_image(img_path):
    image = Image.open(img_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    predicted_class = classes[predicted.item()].lower()
    confidence_score = round(confidence.item() * 100, 2)

    return predicted_class, confidence_score