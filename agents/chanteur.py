"""Agent 13 — Chanteur : chante les paroles sur la mélodie.
Chaque syllabe est prononcée par une voix de synthèse (espeak-ng + MBROLA, gratuits),
puis accordée exactement sur la note (PSOLA via Praat/parselmouth), allongée sur la voyelle,
avec un léger vibrato, puis doublée et passée en réverbération pour une voix douce."""
import os, subprocess, tempfile
import numpy as np

SR = 44100
VOICE = os.environ.get("SINGER_VOICE", "mb-us1")


def available():
    try:
        import parselmouth  # noqa
        from . import voixia
        if voixia.available():
            return True
        subprocess.run(["espeak-ng", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def _hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def _speak(text, path):
    subprocess.run(["espeak-ng", "-v", VOICE, "-s", "115", "-p", "60", "-w", path, text],
                   check=True, capture_output=True)


_CACHE = {}
_RAW = {}
SING_VOICE = os.environ.get("SING_VOICE", "af_sky")


def _raw(text):
    """Syllabe parlée, avant accordage (voix naturelle si disponible, sinon voix de secours)."""
    import parselmouth
    from . import voixia
    if text not in _RAW:
        if voixia.available():
            y, sr = voixia.synth(text, SING_VOICE, 0.9)
            _RAW[text] = parselmouth.Sound(y, sampling_frequency=sr)
        else:
            with tempfile.TemporaryDirectory() as td:
                wav = os.path.join(td, "s.wav")
                _speak(text, wav)
                _RAW[text] = parselmouth.Sound(wav)
    return _RAW[text].copy()


def _syllable(text, segments):
    """segments : liste de (midi, durée en s). Renvoie un signal mono à 44,1 kHz."""
    import parselmouth
    from parselmouth.praat import call
    key = (text, tuple((m, round(d, 3)) for m, d in segments))
    if key in _CACHE:
        return _CACHE[key]
    target = sum(d for _, d in segments)
    snd = _raw(text)
    # enlever les silences au début et à la fin
    x = snd.values[0]
    env = np.convolve(np.abs(x), np.ones(80) / 80, mode="same")
    thr = env.max() * 0.04
    idx = np.where(env > thr)[0]
    if len(idx) == 0:
        return np.zeros(int(SR * target))
    a, b = max(0, idx[0] - 40), min(len(x), idx[-1] + 40)
    snd = parselmouth.Sound(x[a:b], sampling_frequency=snd.sampling_frequency)
    total = snd.duration
    pitch = snd.to_pitch(time_step=0.005, pitch_floor=75, pitch_ceiling=600)
    f0 = pitch.selected_array["frequency"]
    ts = pitch.xs()
    voiced = ts[f0 > 0]
    v0, v1 = (voiced[0], voiced[-1]) if len(voiced) > 1 else (total * 0.2, total * 0.8)
    vlen = max(0.03, v1 - v0)
    stretch = max(0.5, 1 + (target - total) / vlen)

    manip = call(snd, "To Manipulation", 0.005, 75, 600)
    dt = call(manip, "Extract duration tier")
    call(dt, "Remove points between", 0, total)
    for t, f in [(max(0, v0 - 0.002), 1.0), (v0 + 0.01, stretch), (max(v0 + 0.011, v1 - 0.01), stretch),
                 (min(total, v1 + 0.002), 1.0)]:
        call(dt, "Add point", t, f)
    call([manip, dt], "Replace duration tier")
    pt = call(manip, "Extract pitch tier")
    call(pt, "Remove points between", 0, total)
    # points de hauteur dans le temps d'origine : on répartit les notes sur la voyelle
    cum, durs = 0.0, [d for _, d in segments]
    vt = vlen
    for i, (m, d) in enumerate(segments):
        f = _hz(m)
        s0 = v0 + vt * cum / target
        s1 = v0 + vt * (cum + d) / target
        call(pt, "Add point", s0 + (0.004 if i else 0), f)
        # vibrato doux sur les notes longues
        n = int((s1 - s0) * stretch * 5.5)
        if d > 0.45 and n >= 2:
            for k in range(1, n * 2):
                tt = s0 + (s1 - s0) * (0.35 + 0.65 * k / (n * 2))
                call(pt, "Add point", tt, f * 2 ** ((0.25 if k % 2 else -0.25) / 12))
        call(pt, "Add point", max(s0 + 0.005, s1 - 0.004), f)
        cum += d
    call(pt, "Add point", 0, _hz(segments[0][0]))
    call(pt, "Add point", total, _hz(segments[-1][0]))
    call([manip, pt], "Replace pitch tier")
    out = call(manip, "Get resynthesis (overlap-add)")
    y = call(out, "Resample", SR, 50).values[0]
    n = int(SR * target)
    y = y[:n] if len(y) >= n else np.concatenate([y, np.zeros(n - len(y))])
    k1, k2 = min(len(y), int(SR * 0.012)), min(len(y), int(SR * 0.06))
    y[:k1] *= np.linspace(0, 1, k1)
    y[-k2:] *= np.linspace(1, 0, k2)
    y /= (np.abs(y).max() + 1e-9)
    _CACHE[key] = y
    return y


def sing(events, length_s):
    """events : liste de (texte, [(midi, durée)], début en s). Renvoie une piste stéréo (voix doublée)."""
    from scipy.signal import butter, sosfilt
    out = np.zeros(int(SR * (length_s + 1)))
    for text, segs, start in events:
        y = _syllable(text, segs)
        i = int(start * SR)
        out[i:i + len(y)] += y[:len(out) - i] * 0.9
    out = sosfilt(butter(2, [140, 7500], "band", fs=SR, output="sos"), out)
    # doublage léger (deux voix très proches) pour adoucir le timbre de synthèse
    d1, d2 = int(SR * 0.013), int(SR * 0.021)
    L = out + 0.45 * np.concatenate([np.zeros(d1), out[:-d1]])
    R = out + 0.45 * np.concatenate([np.zeros(d2), out[:-d2]])
    st = np.stack([L, R], 1)[:int(SR * length_s)]
    return st / (np.abs(st).max() + 1e-9)
