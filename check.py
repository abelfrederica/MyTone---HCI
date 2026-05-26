import torch
import timm
import torch.nn as nn

# --- Model arsitektur ---
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

# --- Load checkpoint ---
ckpt_path = "model/weights/best_farl64_classifier.pt"
checkpoint = torch.load(ckpt_path, map_location="cpu")

print("Checkpoint keys:", checkpoint.keys())

# Ambil hanya bagian model_state
state_dict = checkpoint["model_state"]

# Load ke model
model = FARLClassifier()
missing, unexpected = model.load_state_dict(state_dict, strict=False)

print("Missing keys:", missing)
print("Unexpected keys:", unexpected)

# Test forward pass
x = torch.randn(1, 3, 224, 224)
out = model(x)
print("Output shape:", out.shape)
