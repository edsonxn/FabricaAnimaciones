import sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
src, dst, prev = sys.argv[1:4]
a = np.array(Image.open(src)).astype(float)
h, w = a.shape[:2]
rgb = a[..., :3]; mx = rgb.max(2); mn = rgb.min(2); s = (mx - mn) / (mx + 1e-3)
yy = np.arange(h)[:, None] * np.ones((1, w)); xx = np.ones((h, 1)) * np.arange(w)[None, :]
m = (a[..., 3] > 0) & (mx > 120) & (s < 0.13) & (yy > 180)
m |= (a[..., 3] > 0) & (mx > 165) & (s < 0.16) & (yy > 0.5 * h) & (xx > 0.62 * w)
m = nd.binary_opening(m, iterations=1)
m = nd.binary_closing(m, iterations=3)
m = nd.binary_dilation(m, iterations=2) & (s < 0.25) & (yy > 0.5 * h)
lab, n = nd.label(m)
sz = nd.sum(m, lab, range(1, n + 1))
keep = np.isin(lab, 1 + np.where(sz > 40)[0])
al = a[..., 3].copy()
al[keep] = 0
# resto pálido bajo las manos: la luz se queda según su saturación (sin borde recortado)
zona = (yy > 205) & (xx > 0.45 * w)
al[zona] *= np.clip((s[zona] - 0.12) / 0.25, 0, 1)
al = np.minimum(al, nd.gaussian_filter(al, 1.2) * 1.15)
a[..., 3] = al
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")
out.save(dst)
bg = Image.new("RGBA", out.size, (40, 90, 40, 255)); bg.alpha_composite(out)
bg.convert("RGB").resize((w * 400 // h, 400)).save(prev)
print("quitados", keep.sum())
