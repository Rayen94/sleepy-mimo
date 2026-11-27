"""Agent 19 — Comédiens : donnent une voix à chaque personnage (anglais).
Voix de synthèse gratuites (espeak-ng + MBROLA) transformées avec Praat pour créer des timbres différents :
narrateur doux, Mimo (voix d'enfant), Luna la chouette (grave et sage), Pip le lapin (très aigu), Twinkle l'étoile, Wooly l'agneau."""
import os, subprocess, tempfile
import numpy as np

SR = 44100
# voix de base, vitesse, décalage des formants, hauteur moyenne (Hz), étendue de la mélodie
CAST = {
    "narrator": ("mb-us1", 128, 1.00, 205, 1.15),
    "mimo":     ("mb-us1", 135, 1.18, 305, 1.45),
    "owl":      ("mb-us3", 122, 0.97, 118, 1.25),
    "bunny":    ("mb-us1", 150, 1.24, 385, 1.5),
    "star":     ("mb-us1", 132, 1.12, 340, 1.6),
    "lamb":     ("mb-us1", 130, 1.20, 330, 1.4),
    "kitten":   ("mb-us1", 135, 1.20, 350, 1.5),
    "duck":     ("mb-us1", 145, 1.25, 400, 1.5),
    "fox":      ("mb-us3", 135, 1.10, 200, 1.3),
    "fish":     ("mb-us3", 120, 0.95, 105, 1.2),
    "hedgehog": ("mb-us1", 140, 1.18, 330, 1.45),
    "otter":    ("mb-us3", 140, 1.12, 215, 1.35),
    "fawn":     ("mb-us1", 135, 1.22, 360, 1.5),
    "beaver":   ("mb-us3", 128, 1.02, 150, 1.25),
    "bat":      ("mb-us1", 150, 1.26, 410, 1.6),
    "turtle":   ("mb-us3", 112, 0.96, 112, 1.15),
}


# voix naturelles : (voix Kokoro, vitesse, décalage des formants, facteur de hauteur)
NATURAL = {
    "narrator": ("af_heart", 0.92, 1.00, 1.00),
    "mimo":     ("af_sky",   1.00, 1.10, 1.32),
    "owl":      ("bf_emma",  0.88, 0.98, 0.92),
    "bunny":    ("af_nova",  1.08, 1.14, 1.65),
    "star":     ("af_bella", 0.95, 1.06, 1.22),
    "lamb":     ("am_puck",  1.00, 1.10, 1.30),
    "kitten":   ("af_nicole", 1.00, 1.12, 1.45),
    "duck":     ("af_jessica", 1.05, 1.16, 1.55),
    "fox":      ("am_liam",  1.02, 1.06, 1.20),
    "fish":     ("am_michael", 0.92, 0.94, 0.85),
    "hedgehog": ("af_sarah",  1.00, 1.08, 1.28),
    "otter":    ("am_eric",   1.06, 1.06, 1.10),
    "fawn":     ("af_aoede",  0.96, 1.12, 1.45),
    "beaver":   ("am_adam",   0.98, 0.98, 0.92),
    "bat":      ("af_kore",   1.10, 1.16, 1.65),
    "turtle":   ("bm_george", 0.84, 0.96, 0.80),
}


def speak(who, text):
    from . import voixia
    if voixia.available():
        return speak_natural(who, text)
    return speak_basic(who, text)


def _finish(y):
    env = np.convolve(np.abs(y), np.ones(400) / 400, mode="same")
    idx = np.where(env > env.max() * 0.03)[0]
    if len(idx):
        y = y[max(0, idx[0] - 200): idx[-1] + 2000]
    y = y / (np.abs(y).max() + 1e-9) * 0.9
    hop = SR // 100
    n = len(y) // hop
    rms = np.sqrt(np.mean(y[:n * hop].reshape(n, hop) ** 2, axis=1))
    mouth = np.clip(rms / (np.percentile(rms, 95) + 1e-9), 0, 1)
    return y, np.convolve(mouth, np.ones(3) / 3, mode="same")


def speak_natural(who, text):
    import parselmouth
    from parselmouth.praat import call
    from . import voixia
    voice, speed, formant, pf = NATURAL[who]
    y, sr = voixia.synth(text, voice, speed)
    snd = parselmouth.Sound(y, sampling_frequency=sr)
    if abs(pf - 1) > 0.01 or abs(formant - 1) > 0.01:
        f0 = snd.to_pitch().selected_array["frequency"]
        med = float(np.median(f0[f0 > 0])) if (f0 > 0).any() else 180.0
        snd = call(snd, "Change gender", 75, 600, formant, med * pf, 1.1, 1.0)
    y = call(snd, "Resample", SR, 50).values[0]
    return _finish(y)


def speak_basic(who, text):
    """Renvoie (signal mono 44,1 kHz normalisé, enveloppe d'amplitude à 100 Hz pour animer la bouche)."""
    import parselmouth
    from parselmouth.praat import call
    voice, speed, formant, pitch, rng = CAST[who]
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "l.wav")
        subprocess.run(["espeak-ng", "-v", voice, "-s", str(speed), "-w", wav, text], check=True, capture_output=True)
        snd = parselmouth.Sound(wav)
    snd = call(snd, "Change gender", 75, 600, formant, pitch, rng, 1.0)
    y = call(snd, "Resample", SR, 50).values[0]
    # enlever les silences au début et à la fin
    env = np.convolve(np.abs(y), np.ones(400) / 400, mode="same")
    idx = np.where(env > env.max() * 0.03)[0]
    if len(idx):
        y = y[max(0, idx[0] - 200): idx[-1] + 2000]
    y = y / (np.abs(y).max() + 1e-9) * 0.9
    hop = SR // 100
    n = len(y) // hop
    rms = np.sqrt(np.mean(y[:n * hop].reshape(n, hop) ** 2, axis=1))
    mouth = np.clip(rms / (np.percentile(rms, 95) + 1e-9), 0, 1)
    mouth = np.convolve(mouth, np.ones(3) / 3, mode="same")
    return y, mouth
