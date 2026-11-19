"""Agent 3 — Compositeur : compose des mélodies originales et arrange des comptines
du domaine public (aucun enregistrement ni arrangement d'un tiers n'est utilisé)."""
import math, wave
import numpy as np
from scipy.signal import fftconvolve

SR = 44100
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
CHORDS = {'C': [0, 4, 7], 'F': [5, 9, 12], 'G': [7, 11, 14], 'Am': [9, 12, 16]}

# Mélodies traditionnelles du domaine public (notes, durées en temps), accords par segment
PUBLIC_DOMAIN = {
    "Twinkle Twinkle Little Star": (72,
        "C1 C1 G1 G1 A1 A1 G2 F1 F1 E1 E1 D1 D1 C2 G1 G1 F1 F1 E1 E1 D2 G1 G1 F1 F1 E1 E1 D2 "
        "C1 C1 G1 G1 A1 A1 G2 F1 F1 E1 E1 D1 D1 C2",
        "C2 C2 F2 C2 F2 C2 G2 C2 C2 F2 C2 G2 C2 F2 C2 G2 C2 C2 F2 C2 F2 C2 G2 C2"),
    "Are You Sleeping (Frère Jacques)": (76,
        "C1 D1 E1 C1 C1 D1 E1 C1 E1 F1 G2 E1 F1 G2 G.5 A.5 G.5 F.5 E1 C1 G.5 A.5 G.5 F.5 E1 C1 C1 G,1 C2 C1 G,1 C2",
        "C4 C4 C4 C4 C4 C4 G2 C2 G2 C2"),
    "Row Row Row Your Boat": (80,
        "C1.5 C1.5 C1 D.5 E1.5 E1 D.5 E1 F.5 G3 C'.5 C'.5 C'.5 G.5 G.5 G.5 E.5 E.5 E.5 C.5 C.5 C.5 G1 F.5 E1 D.5 C3",
        "C3 C3 C3 C3 C3 C3 G3 C3"),
    "Brahms' Lullaby": (66,
        "E.5 E.5 G1.5 E.5 E1 G2 E.5 G.5 C'1 B1.5 A.5 A1 G1 D.5 E.5 F1 D1 D.5 E.5 F2 D.5 F.5 B.5 A.5 G1 B1 "
        "C'2 C.5 C.5 C'2 A.5 F.5 G2 E.5 C.5 F1 G1 A1 G2 C.5 C.5 C'2 A.5 F.5 G2 E.5 C.5 F1 E1 D1 C3",
        "C1 C3 C3 C3 G3 G3 G3 G3 C3 F3 C3 F3 C3 F3 C3 G3 C3"),
    "Mary Had a Little Lamb": (70,
        "E1 D1 C1 D1 E1 E1 E2 D1 D1 D2 E1 G1 G2 E1 D1 C1 D1 E1 E1 E1 E1 D1 D1 E1 D1 C4",
        "C4 C4 G4 C4 C4 C4 G4 C4"),
    "London Bridge": (72,
        "G1.5 A.5 G1 F1 E1 F1 G2 D1 E1 F2 E1 F1 G2 G1.5 A.5 G1 F1 E1 F1 G2 D2 G1 E1 C4",
        "C4 C4 G4 C4 C4 C4 G4 C4"),
}

VOICES = ["box", "soft", "harp", "bell"]
VOICE_NAMES = {"box": "Music Box", "soft": "Soft Piano", "harp": "Gentle Harp", "bell": "Twinkle Bells"}


def _tokens(s):
    for tok in s.split():
        i = len(tok.rstrip("0123456789."))
        yield tok[:i], float(tok[i:])


def parse_melody(s):
    return [(NOTE[n[0]] + 12 * n.count("'") - 12 * n.count(","), d) for n, d in _tokens(s)]


def parse_chords(s):
    return list(_tokens(s))


def compose(rng):
    """Compose une berceuse originale : forme A A' B A'', gamme pentatonique."""
    scale = [-5, -3, 0, 2, 4, 7, 9, 12, 14, 16]
    rhythms = [[1, 1, 1, 1], [2, 1, 1], [1, 1, 2], [2, 2], [1.5, .5, 2], [3, 1], [1, 1, 1, 1]]
    progs = [["C", "F", "G", "C"], ["C", "Am", "F", "G"], ["C", "G", "Am", "F"], ["F", "C", "G", "C"], ["C", "F", "C", "G"]]

    def phrase(start, end_on_tonic):
        idx, bars = start, []
        for b in range(4):
            r = list(rhythms[rng.integers(len(rhythms))])
            bar = []
            for d in r:
                idx = int(np.clip(idx + rng.integers(-2, 3), 1, len(scale) - 2))
                bar.append([scale[idx], d])
            bars.append(bar)
        bars[3] = [[0 if end_on_tonic else 7, 4]] if rng.random() < 0.6 else [[bars[3][0][0], 2], [0 if end_on_tonic else 7, 2]]
        return bars

    A = phrase(int(rng.integers(3, 6)), False)
    A2 = [b[:] for b in A[:3]] + [[[0, 4]]]
    B = phrase(int(rng.integers(5, 8)), False)
    A3 = [b[:] for b in A[:3]] + [[[0, 2], [0, 2]]]
    mel = [tuple(n) for part in (A, A2, B, A3) for bar in part for n in bar]
    pr = progs[rng.integers(len(progs))]
    ch = [(c, 4) for _ in range(3) for c in pr] + [(c, 4) for c in pr[:3]] + [("C", 4)]
    return int(rng.integers(60, 74)), mel, ch


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def tone(f, dur, voice):
    tail = {"box": 2.5, "soft": 3.5, "harp": 2.5, "bell": 4.0}[voice]
    n = int(SR * (dur + tail)); t = np.arange(n) / SR
    if voice == "box":
        y = np.sin(2*np.pi*f*t) + 0.35*np.sin(4*np.pi*f*t)*np.exp(-t*4) + 0.12*np.sin(2*np.pi*4.17*f*t)*np.exp(-t*8)
        env = np.exp(-t * 1.8)
    elif voice == "soft":
        y = np.sin(2*np.pi*f*t) + 0.25*np.sin(4*np.pi*f*t)*np.exp(-t*2) + 0.06*np.sin(6*np.pi*f*t)*np.exp(-t*3)
        env = np.exp(-t * 1.1)
    elif voice == "harp":
        y = sum((0.6 ** k) * np.sin(2*np.pi*f*(k+1)*t) * np.exp(-t*(1.5+k)) for k in range(5))
        env = np.exp(-t * 1.6)
    else:
        y = np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2.0*f*t)*np.exp(-t*2) + 0.15*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*3) \
            + 0.05*np.sin(2*np.pi*5.4*f*t)*np.exp(-t*6)
        env = np.exp(-t * 1.3)
    return y * env * np.minimum(1, t / 0.005)


def pad(notes, dur):
    n = int(SR * (dur + 1.5)); t = np.arange(n) / SR
    env = np.minimum(1, t / 0.8) * np.where(t > dur, np.exp(-(t - dur) * 2.5), 1)
    y = sum(np.sin(2*np.pi*hz(m)*t) + 0.3*np.sin(2*np.pi*hz(m)*2.001*t) for m in notes)
    return y * env / len(notes)


def render(bpm, mel, ch, voice, octave, transpose, min_seconds):
    b = 60 / bpm
    L = sum(d for _, d in mel) * b
    reps = max(1, math.ceil(min_seconds / L))
    out = np.zeros(int(SR * (L * reps + 8)))
    for r in range(reps):
        off = r * L; t = off
        oc = octave + (12 if voice in ("box", "bell") and r % 2 == 1 else 0)
        for m, d in mel:
            x = tone(hz(60 + m + oc + transpose), d * b, voice) * (0.32 if r % 2 == 0 else 0.26)
            i = int(t * SR); out[i:i + len(x)] += x[:len(out) - i]; t += d * b
        t = off
        for c, d in ch:
            x = pad([48 + transpose + k for k in CHORDS[c]], d * b) * 0.10
            i = int(t * SR); out[i:i + len(x)] += x[:len(out) - i]; t += d * b
    out = out[:int(SR * (L * reps + 4))]
    k = int(SR * 4); out[-k:] *= np.linspace(1, 0, k)
    return out


_IR = None


def reverb(dry):
    global _IR
    if _IR is None:
        g = np.random.default_rng(0)
        t = np.arange(int(SR * 2.8)) / SR
        _IR = [g.standard_normal(len(t)) * np.exp(-t * 2.6) * 0.02 for _ in range(2)]
    L = fftconvolve(dry, _IR[0])[:len(dry)]; R = fftconvolve(dry, _IR[1])[:len(dry)]
    st = np.stack([dry * 0.8 + L * 0.9, dry * 0.8 + R * 0.9], 1)
    return st / max(1.0, np.abs(st).max() / 0.6)


def write_wav(path, chunks):
    wf = wave.open(path, "wb"); wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    for c in chunks:
        wf.writeframes((np.clip(c, -1, 1) * 32767).astype("<i2").tobytes())
    wf.close()


def track_spec(item, rng):
    """item = ('pd', nom) ou ('orig', nom). Retourne bpm, mélodie, accords."""
    kind, name = item
    if kind == "pd":
        bpm, m, c = PUBLIC_DOMAIN[name]
        return bpm, parse_melody(m), parse_chords(c)
    return compose(rng)


def build_long(plan, rng, path):
    """plan : liste de dicts {item, voice, octave, transpose, seconds, tempo}. Écrit le WAV, renvoie les chapitres."""
    stamps, pos = [], 0.0

    def gen():
        nonlocal pos
        for p in plan:
            bpm, mel, ch = p["spec"]
            st = reverb(render(bpm * p["tempo"], mel, ch, p["voice"], p["octave"], p["transpose"], p["seconds"]))
            stamps.append((pos, p))
            data = np.concatenate([st, np.zeros((SR * 2, 2))])
            pos += len(data) / SR
            yield data
    write_wav(path, gen())
    return stamps, pos


def build_short(spec, voice, octave, transpose, seconds, path):
    bpm, mel, ch = spec
    st = reverb(render(bpm, mel, ch, voice, octave, transpose, seconds + 1))[:int(SR * seconds)]
    k = int(SR * 2.5); st[-k:] *= np.linspace(1, 0, k)[:, None]
    write_wav(path, [st])
    return seconds
