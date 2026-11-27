"""Moteur de voix naturelles (Kokoro, modèle libre Apache 2.0, fonctionne sans carte graphique).
Les fichiers du modèle sont téléchargés une fois depuis GitHub (voir le workflow)."""
import os
import numpy as np

MODELS = os.environ.get("MODELS_DIR", "models")
_K = None


def available():
    try:
        import kokoro_onnx  # noqa
        return os.path.exists(os.path.join(MODELS, "kokoro-v1.0.int8.onnx")) and os.path.exists(os.path.join(MODELS, "voices-v1.0.bin"))
    except Exception:
        return False


def engine():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(os.path.join(MODELS, "kokoro-v1.0.int8.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))
    return _K


def synth(text, voice, speed=1.0, lang="en-us"):
    """Renvoie (signal mono float, fréquence d'échantillonnage)."""
    y, sr = engine().create(text, voice=voice, speed=speed, lang=lang)
    return np.asarray(y, dtype=np.float64), sr
