"""Agent 3 — Compositeur : compose des mélodies originales et arrange des comptines
du domaine public (aucun enregistrement ni arrangement d'un tiers n'est utilisé)."""
import math, wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt, sosfilt_zi

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


def bass(f, dur):
    n = int(SR * (dur + 1.5)); t = np.arange(n) / SR
    y = np.sin(2*np.pi*f*t) + 0.25*np.sin(4*np.pi*f*t)*np.exp(-t*3)
    env = np.minimum(1, t / 0.03) * np.exp(-t * 0.9) * np.where(t > dur, np.exp(-(t - dur) * 4), 1)
    return y * env


def render(bpm, mel, ch, voice, octave, transpose, min_seconds, seed=0):
    """Mélodie + accords tenus + basse douce + contre-mélodie en arpège (une reprise sur deux).
    Petites variations de tempo et de force pour un jeu plus humain."""
    hum = np.random.default_rng(seed)
    b = 60 / bpm
    L = sum(d for _, d in mel) * b
    reps = max(1, math.ceil(min_seconds / L))
    out = np.zeros(int(SR * (L * reps + 8)))

    def add(x, at):
        i = max(0, int(at * SR)); out[i:i + len(x)] += x[:len(out) - i]

    for r in range(reps):
        off = r * L; t = off
        oc = octave + (12 if voice in ("box", "bell") and r % 2 == 1 else 0)
        for j, (m, d) in enumerate(mel):
            jit = 0 if j == 0 else float(np.clip(hum.normal(0, 0.007), -0.015, 0.015))
            vel = (0.32 if r % 2 == 0 else 0.27) * float(np.clip(1 + hum.normal(0, 0.07), 0.8, 1.2))
            add(tone(hz(60 + m + oc + transpose), d * b, voice) * vel, t + jit); t += d * b
        t = off
        for c, d in ch:
            add(pad([48 + transpose + k for k in CHORDS[c]], d * b) * 0.10, t)
            add(bass(hz(36 + transpose + CHORDS[c][0]), d * b) * 0.10, t)
            if r % 2 == 1 and reps > 1:
                tones = CHORDS[c] + [CHORDS[c][0] + 12]
                for k in range(int(d)):
                    m = 60 + transpose + tones[k % len(tones)]
                    add(tone(hz(m), b, "harp") * 0.06 * float(np.clip(1 + hum.normal(0, 0.1), 0.7, 1.3)), t + (k + 0.5) * b)
            t += d * b
    out = out[:int(SR * (L * reps + 4))]
    k = int(SR * 4); out[-k:] *= np.linspace(1, 0, k)
    return out


_IR = None
_WARM = butter(2, 6500, 'low', fs=SR, output='sos')


def reverb(dry):
    global _IR
    if _IR is None:
        g = np.random.default_rng(0)
        t = np.arange(int(SR * 2.8)) / SR
        _IR = [g.standard_normal(len(t)) * np.exp(-t * 2.6) * 0.02 for _ in range(2)]
    dry = sosfilt(_WARM, dry)
    L = fftconvolve(dry, _IR[0])[:len(dry)]; R = fftconvolve(dry, _IR[1])[:len(dry)]
    st = np.stack([dry * 0.8 + L * 0.9, dry * 0.8 + R * 0.9], 1)
    return st / max(1.0, np.abs(st).max() / 0.6)


def limit(x, knee=0.6, ceil=0.9):
    """Limiteur doux : rien ne change sous le seuil, aucune saturation au-dessus."""
    a = np.abs(x)
    over = a > knee
    x = x.copy()
    x[over] = np.sign(x[over]) * (knee + (ceil - knee) * np.tanh((a[over] - knee) / (ceil - knee)))
    return x


def write_wav(path, chunks):
    wf = wave.open(path, "wb"); wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    for c in chunks:
        wf.writeframes((np.clip(limit(c), -1, 1) * 32767).astype("<i2").tobytes())
    wf.close()


def track_spec(item, rng):
    """item = ('pd', nom) ou ('orig', nom). Retourne bpm, mélodie, accords."""
    kind, name = item
    if kind == "pd":
        bpm, m, c = PUBLIC_DOMAIN[name]
        return bpm, parse_melody(m), parse_chords(c)
    return compose(rng)


# ---------------------------------------------------------------- Sons d'ambiance
AMBIENCE = {"moon": "shush", "clouds": "shush", "ocean": "ocean", "snow": "wind", "forest": "night", "rain": "rain"}
AMBIENCE_NAMES = {"shush": "Soft White Noise", "ocean": "Ocean Waves", "wind": "Soft Wind", "night": "Night Sounds",
                  "rain": "Rain Sounds"}


class Ambience:
    """Bruit d'ambiance continu (filtres gardés d'un morceau à l'autre pour éviter les clics)."""
    FILTERS = {
        "shush": [butter(2, 2800, "low", fs=SR, output="sos"), butter(1, 120, "high", fs=SR, output="sos")],
        "rain":  [butter(2, [700, 7000], "band", fs=SR, output="sos")],
        "ocean": [butter(2, 500, "low", fs=SR, output="sos")],
        "wind":  [butter(2, [250, 1100], "band", fs=SR, output="sos")],
        "night": [butter(2, 400, "low", fs=SR, output="sos")],
    }
    LEVEL = {"shush": 0.020, "rain": 0.030, "ocean": 0.050, "wind": 0.030, "night": 0.015}

    def __init__(self, seed=1):
        self.rng = np.random.default_rng(seed)
        self.state = {}
        self.clock = {}

    def make(self, kind, n, fade_in=False, fade_out=False):
        noise = self.rng.standard_normal((n, 2))
        sts = self.state.setdefault(kind, [[sosfilt_zi(f) * 0 for _ in range(2)] for f in self.FILTERS[kind]])
        for fi, f in enumerate(self.FILTERS[kind]):
            for c in range(2):
                noise[:, c], sts[fi][c] = sosfilt(f, noise[:, c], zi=sts[fi][c])
        t0 = self.clock.get(kind, 0.0)
        t = t0 + np.arange(n) / SR
        self.clock[kind] = t0 + n / SR
        if kind == "ocean":
            env = 0.3 + 0.7 * (0.5 - 0.5 * np.cos(2 * np.pi * t / 9.0)) ** 1.6
            env2 = 0.3 + 0.7 * (0.5 - 0.5 * np.cos(2 * np.pi * (t + 3.1) / 11.0)) ** 1.6
            noise[:, 0] *= env; noise[:, 1] *= env2
        elif kind == "wind":
            env = 0.6 + 0.25 * np.sin(2 * np.pi * t / 13.0) + 0.15 * np.sin(2 * np.pi * t / 5.3 + 1)
            noise *= env[:, None]
        elif kind == "rain":
            noise *= (0.9 + 0.1 * np.sin(2 * np.pi * t / 7.0))[:, None]
        noise *= self.LEVEL[kind] / (np.sqrt(np.mean(noise ** 2)) + 1e-9)
        if kind == "night":  # quelques grillons très discrets
            for _ in range(int(n / SR / 2.5)):
                st = int(self.rng.uniform(0, max(1, n - SR)))
                ln = int(SR * 0.35); tt = np.arange(ln) / SR
                chirp = np.sin(2 * np.pi * 4300 * tt) * (np.sin(2 * np.pi * 28 * tt) > 0.3) * np.sin(np.pi * tt / 0.35) * 0.006
                pan = self.rng.uniform(0.2, 0.8)
                noise[st:st + ln, 0] += chirp[:n - st] * pan; noise[st:st + ln, 1] += chirp[:n - st] * (1 - pan)
        k = min(n // 2, int(SR * 3))
        if fade_in:
            noise[:k] *= np.linspace(0, 1, k)[:, None]
        if fade_out:
            noise[-k:] *= np.linspace(1, 0, k)[:, None]
        return noise


def play(bpm, mel, ch, voice, octave, transpose, seconds, seed=0, lively=False):
    """Musique stéréo prête à mixer : vrais instruments (orchestre) si disponibles, sinon synthèse maison."""
    from . import orchestre
    if orchestre.available():
        return orchestre.render(bpm, mel, ch, voice, octave, transpose, seconds, seed=seed, lively=lively)
    return reverb(render(bpm, mel, ch, voice, octave, transpose, seconds, seed=seed))


def pass_schedule(bpm, mel, reps):
    """Instants (en s) de chaque note, passage par passage, comme dans render()."""
    b = 60 / bpm
    L = sum(d for _, d in mel) * b
    out = []
    for r in range(reps):
        t, row = r * L, []
        for m, d in mel:
            row.append((t, m, d * b)); t += d * b
        out.append(row)
    return out, L


def intro_audio(seconds=5.0):
    """Petit carillon d'ouverture « Sleepy Mimo »."""
    n = int(SR * seconds)
    out = np.zeros(n + SR * 5)
    for i, m in enumerate([72, 76, 79, 84, 79, 88]):
        x = tone(hz(m), 1.2, "bell") * (0.22 if i < 5 else 0.18)
        j = int(SR * (0.35 + i * 0.32)); out[j:j + len(x)] += x[:len(out) - j]
    x = pad([60, 64, 67, 72], 3.5) * 0.08
    j = int(SR * 0.3); out[j:j + len(x)] += x[:len(out) - j]
    st = reverb(out)[:n]
    k = int(SR * 1.0); st[-k:] *= np.linspace(1, 0, k)[:, None]
    return st


def build_long(plan, rng, path, ambience=True, intro=5.0, vocals=True, story_audio=None, outro_audio=None):
    """plan : liste de dicts {item, voice, octave, transpose, seconds, tempo, theme, lyrics}.
    Écrit le WAV. Renvoie les chapitres, la durée totale et les paroles minutées (pour le karaoké)."""
    from . import chanteur, parolier
    stamps, karaoke, pos = [], [], 0.0
    amb = Ambience(int(rng.integers(1e9)))
    sing_ok = vocals and chanteur.available()

    def gen():
        nonlocal pos
        if intro:
            data = intro_audio(intro)
            if ambience and plan:
                data = data + amb.make(AMBIENCE[plan[0]["theme"]], len(data), fade_in=True) * 0.6
            pos += len(data) / SR
            yield data
        if story_audio is not None:
            data = story_audio.copy()
            if ambience and plan:
                data = data + amb.make(AMBIENCE[plan[0]["theme"]], len(data)) * 0.5
            pos += len(data) / SR
            yield data
        for i, p in enumerate(plan):
            bpm, mel, ch = p["spec"]
            song = p.get("lyrics")
            st = play(bpm * p["tempo"], mel, ch, p["voice"], p["octave"], p["transpose"], p["seconds"], seed=i, lively=bool(song))
            if sing_ok and song and parolier.check(song, len(mel)):
                reps = max(1, math.ceil(p["seconds"] / (sum(d for _, d in mel) * 60 / (bpm * p["tempo"]))))
                sched, _ = pass_schedule(bpm * p["tempo"], mel, reps)
                syl = [s for line in parolier.lines(song) for s in line]
                events = []
                for r in range(min(2, reps)):
                    k = 0
                    for line in parolier.lines(song):
                        times = []
                        for disp, sung in line:
                            t0, m, d = sched[r][k]
                            events.append((sung, [(60 + m + p["transpose"], d * 0.97)], t0))
                            times.append(pos + t0); k += 1
                        karaoke.append(dict(syllables=[d for d, _ in line], times=times,
                                            end=pos + sched[r][k - 1][0] + sched[r][k - 1][2]))
                voice = chanteur.sing(events, len(st) / SR)
                vrev = reverb(voice[:, 0] * 0.5 + voice[:, 1] * 0.5)
                n = min(len(st), len(vrev))
                st = st * 0.8
                st[:n] += vrev[:n] * 0.75
            stamps.append((pos, p))
            data = np.concatenate([st, np.zeros((SR * 2, 2))])
            if ambience:
                kind = AMBIENCE[p["theme"]]
                last = i == len(plan) - 1 or AMBIENCE[plan[i + 1]["theme"]] != kind
                first = (i == 0 and not intro) or (i > 0 and AMBIENCE[plan[i - 1]["theme"]] != kind)
                data += amb.make(kind, len(data), fade_in=first, fade_out=last)
            pos += len(data) / SR
            yield data
        if outro_audio is not None:
            data = outro_audio.copy()
            if ambience and plan:
                data = data + amb.make(AMBIENCE[plan[-1]["theme"]], len(data), fade_in=True) * 0.5
            pos += len(data) / SR
            yield data
    write_wav(path, gen())
    return stamps, pos, karaoke


def build_short(spec, voice, octave, transpose, seconds, path, theme=None, ambience=True, seed=0):
    bpm, mel, ch = spec
    st = play(bpm, mel, ch, voice, octave, transpose, seconds + 1, seed=seed)[:int(SR * seconds)]
    if ambience and theme:
        st = st + Ambience(seed + 7).make(AMBIENCE[theme], len(st), fade_in=True)
    k = int(SR * 2.5); st[-k:] *= np.linspace(1, 0, k)[:, None]
    k = int(SR * 0.3); st[:k] *= np.linspace(0, 1, k)[:, None]
    write_wav(path, [st])
    return seconds
