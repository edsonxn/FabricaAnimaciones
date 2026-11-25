# -*- coding: utf-8 -*-
"""Mate de la persona con DeepLabV3-ResNet101 (torchvision, GPU, ~0,3 s/cuadro) → fuente/alfa/a_%04d.png
(rembg en CPU iba a ~15 s/cuadro con la PC ocupada). Salta intro e insertos (recortar.hay_el)."""
import cv2, numpy as np, torch
from pathlib import Path
from torchvision.models.segmentation import deeplabv3_resnet101, DeepLabV3_ResNet101_Weights
from recortar import CU, AL, hay_el

AL.mkdir(exist_ok=True)
m = deeplabv3_resnet101(weights=DeepLabV3_ResNet101_Weights.DEFAULT).cuda().eval().half()
mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).cuda().half()
std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).cuda().half()
fs = [f for f in sorted(CU.glob("c_*.jpg")) if hay_el(int(f.stem[2:]) - 1)]
for k, f in enumerate(fs):
    sal = AL / f.name.replace("c_", "a_").replace(".jpg", ".png")
    if sal.exists():
        continue
    im = cv2.imread(str(f))[..., ::-1].copy()
    x = torch.from_numpy(im).cuda().half().permute(2, 0, 1)[None] / 255
    with torch.no_grad():
        o = m((x - mean) / std)["out"].float().softmax(1)[0, 15].cpu().numpy()
    cv2.imwrite(str(sal), (np.clip(o, 0, 1) * 255).astype(np.uint8))
    if k % 200 == 0:
        print(k, len(fs), flush=True)
print("listo", len(fs))
