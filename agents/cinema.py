"""Étalonneur « cinéma » (saison 2) : donne aux images dessinées un rendu de caméra de nature.

Appliqué sur chaque image rastérisée, sans toucher au dessin :
  - mise au point douce sur le lointain (haut de l'image) et le tout premier plan (bas), comme avec un téléobjectif ;
  - lueur (bloom) autour des lumières : lune, lucioles, yeux ;
  - étalonnage : contraste en S, ombres bleutées, hautes lumières chaudes, couleurs un peu plus riches ;
  - vignettage léger ;
  - grain fin qui casse les aplats et évite les bandes dans les dégradés sombres après compression vidéo.
"""
import io
import numpy as np
from PIL import Image, ImageFilter

_MAPS = {}
_NOISE = {}


def _maps(w, h):
    key = (w, h)
    if key not in _MAPS:
        y = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
        x = np.linspace(-1.0, 1.0, w, dtype=np.float32)[None, :]
        vertical = h > w                         # Shorts : le « lointain » occupe une zone plus haute
        far, near = (0.26, 0.93) if vertical else (0.34, 0.90)
        top = np.clip((far - y) / far, 0.0, 1.0) ** 1.4
        bot = np.clip((y - near) / (1.0 - near), 0.0, 1.0) ** 1.2
        soft = np.maximum(top * 0.95, bot * 0.85)
        soft = np.broadcast_to(soft, (h, w)).astype(np.float32)
        if vertical:
            soft = soft * 0.0                    # les Shorts portent du texte partout : pas de flou
        else:                                    # on épargne le logo en haut à droite
            wm = np.clip((x - 0.74) / 0.04, 0.0, 1.0) * np.clip((0.14 - y) / 0.03, 0.0, 1.0)
            soft = soft * (1.0 - wm)
        soft = soft[..., None].astype(np.float32)
        r2 = (x * 0.78) ** 2 + ((y - 0.5) * 2.0) ** 2 * 0.82
        vig = (1.0 - 0.30 * np.clip(r2, 0.0, 1.5) ** 1.6).astype(np.float32)[..., None]
        _MAPS[key] = (soft, vig)
    return _MAPS[key]


def _noise(w, h):
    key = (w, h)
    if key not in _NOISE:
        rng = np.random.default_rng(7)
        _NOISE[key] = rng.standard_normal((h + 96, w + 96)).astype(np.float32)
    return _NOISE[key]


def _blur(img, size, radius):
    """Flou gaussien rapide : on travaille en basse résolution puis on remonte."""
    w, h = img.size
    small = img.resize(size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(radius))
    return small.resize((w, h), Image.BILINEAR)


def look(png_bytes):
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    w, h = img.size
    soft, vig = _maps(w, h)
    a = np.asarray(img, dtype=np.float32) / 255.0

    # 1) mise au point douce (lointain en haut, premier plan en bas)
    blurred = np.asarray(_blur(img, (w // 2, h // 2), 4.0), dtype=np.float32) / 255.0
    a = a * (1.0 - soft) + blurred * soft

    # 2) lueur autour des zones lumineuses
    quarter = img.resize((w // 4, h // 4), Image.BILINEAR)
    q = np.asarray(quarter, dtype=np.float32) / 255.0
    lum_q = q @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    bright = np.clip((lum_q - 0.52) / 0.48, 0.0, 1.0)[..., None] * q
    glow = Image.fromarray((np.clip(bright, 0, 1) * 255).astype(np.uint8))
    g1 = np.asarray(glow.filter(ImageFilter.GaussianBlur(5)).resize((w, h), Image.BILINEAR), dtype=np.float32) / 255.0
    g2 = np.asarray(glow.filter(ImageFilter.GaussianBlur(16)).resize((w, h), Image.BILINEAR), dtype=np.float32) / 255.0
    bloom = np.clip(g1 * 0.55 + g2 * 0.75, 0.0, 1.0)
    a = 1.0 - (1.0 - a) * (1.0 - bloom * 0.55)

    # 3) étalonnage
    a = 0.5 + (a - 0.5) * 1.07                                  # contraste
    lum = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    lum3 = lum[..., None]
    a = lum3 + (a - lum3) * 1.09                               # couleurs plus riches
    sh = ((1.0 - lum) ** 2)[..., None]
    hi = (lum ** 2)[..., None]
    a = a + sh * np.array([-0.010, 0.002, 0.032], dtype=np.float32) + hi * np.array([0.030, 0.012, -0.022], dtype=np.float32)

    # 4) vignettage + grain fin
    a = a * vig
    n = _noise(w, h)
    ox, oy = np.random.randint(0, 96, 2)
    a = a + (n[oy:oy + h, ox:ox + w] * (1.6 / 255.0))[..., None]

    out = Image.fromarray((np.clip(a, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8))
    buf = io.BytesIO()
    out.save(buf, "PNG", compress_level=1)
    return buf.getvalue()
