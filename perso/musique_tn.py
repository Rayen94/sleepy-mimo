"""Musique originale de la série (mode hijaz, guitare, cordes, ney, darbouka) — rendue avec FluidSynth."""
import os, subprocess, tempfile
import numpy as np, soundfile as sf
import mido

SR = 44100
SF2 = next((p for p in ["sf2/FluidR3_GM.sf2", "/usr/share/sounds/sf2/FluidR3_GM.sf2"] if os.path.exists(p)), None)

N = {"A3": 57, "Bb3": 58, "C#4": 61, "D4": 62, "E4": 64, "F4": 65, "G4": 67, "A4": 69, "Bb4": 70, "C5": 72,
     "C#5": 73, "D5": 74, "E5": 76, "F5": 77, "G5": 79, "A5": 81}
MEL = [[("A4", 1), ("C5", .5), ("D5", .5), ("E5", 1.5), ("D5", .5)],
       [("C#5", .5), ("D5", .5), ("E5", .5), ("F5", .5), ("E5", 2)],
       [("F5", 1), ("E5", .5), ("D5", .5), ("C#5", 1), ("D5", 1)],
       [("E5", 3), (None, 1)],
       [("A5", 1), ("G5", .5), ("F5", .5), ("E5", 1), ("F5", .5), ("E5", .5)],
       [("D5", 1), ("C#5", .5), ("D5", .5), ("E5", 2)],
       [("F5", .5), ("E5", .5), ("D5", .5), ("C#5", .5), ("Bb4", 1), ("C#5", 1)],
       [("A4", 4)]]
CH = [(57, 60, 64), (57, 61, 64), (50, 53, 57), (57, 61, 64), (50, 53, 57), (57, 61, 64), (46, 50, 53), (57, 61, 64)]


def _midi(path, bpm, mood, bars_rep=2):
    mid = mido.MidiFile(ticks_per_beat=480)
    T = 480
    tracks = {}

    def tr(ch, prog, vol):
        t = mido.MidiTrack(); mid.tracks.append(t)
        if ch != 9:
            t.append(mido.Message("program_change", channel=ch, program=prog, time=0))
        t.append(mido.Message("control_change", channel=ch, control=7, value=vol, time=0))
        t.append(mido.Message("control_change", channel=ch, control=91, value=70, time=0))
        tracks[ch] = (t, [])
        return tracks[ch][1]

    meta = mido.MidiTrack(); mid.tracks.insert(0, meta)
    meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    ev_mel = tr(0, 77 if mood == "theme" else 73, 100 if mood == "theme" else 70)
    ev_gtr = tr(1, 24, 92)
    ev_str = tr(2, 49, 70 if mood != "sad" else 85)
    ev_bas = tr(3, 32, 90)
    ev_drm = tr(9, 0, 90 if mood == "theme" else 60)
    beat = 0.0
    for rep in range(bars_rep):
        for b in range(8):
            t0 = (rep * 8 + b) * 4
            root, third, fifth = CH[b]
            # mélodie
            if mood in ("theme", "sad") or (mood == "light" and rep == 1):
                x = t0
                for n, d in MEL[b]:
                    if n:
                        v = 92 if mood == "theme" else 64
                        ev_mel.append((x, N[n] - (12 if mood == "sad" else 0), v, d * 0.95))
                    x += d
            # guitare en arpèges
            arp = [root + 12, third + 12, fifth + 12, third + 24, fifth + 12, third + 12, root + 24, fifth + 12]
            for k in range(8):
                ev_gtr.append((t0 + k * 0.5, arp[k], 70 if k % 2 else 82, 0.9))
            # cordes
            for n in (third + 12, fifth + 12, root + 24):
                ev_str.append((t0, n, 55, 3.95))
            # basse
            ev_bas.append((t0, root - 12, 85, 1.8)); ev_bas.append((t0 + 2, root - 12 + (7 if b % 2 else 0), 75, 1.8))
            # darbouka (maqsum)
            if mood != "sad":
                for (pos, note, v) in [(0, 64, 100), (0.5, 60, 80), (1.5, 60, 85), (2, 64, 95), (3, 60, 85), (3.5, 60, 60)]:
                    ev_drm.append((t0 + pos, note, v if mood == "theme" else int(v * 0.6), 0.2))
                for k in range(8):
                    ev_drm.append((t0 + k * 0.5 + 0.25, 54, 35, 0.1))
    for ch, (t, evs) in tracks.items():
        msgs = []
        for (s, n, v, d) in evs:
            msgs.append((int(s * T), mido.Message("note_on", channel=ch, note=int(n), velocity=int(v))))
            msgs.append((int((s + d) * T), mido.Message("note_off", channel=ch, note=int(n), velocity=0)))
        msgs.sort(key=lambda m: (m[0], m[1].type == "note_on"))
        last = 0
        for at, m in msgs:
            t.append(m.copy(time=at - last)); last = at
    mid.save(path)
    return bars_rep * 8 * 4 * 60.0 / bpm


_CACHE = {}


def cue(mood):
    """Une boucle stéréo (numpy, 44.1 kHz) : theme | light | sad."""
    if mood in _CACHE:
        return _CACHE[mood]
    bpm = {"theme": 92, "light": 96, "sad": 68}[mood]
    d = tempfile.mkdtemp()
    mpath, wpath = os.path.join(d, "m.mid"), os.path.join(d, "m.wav")
    L = _midi(mpath, bpm, mood)
    if SF2:
        subprocess.run(["fluidsynth", "-ni", "-g", "0.8", "-F", wpath, "-r", str(SR), SF2, mpath], check=True,
                       capture_output=True)
        y, _ = sf.read(wpath)
        if y.ndim == 1:
            y = np.stack([y, y], 1)
    else:
        y = np.zeros((int(L * SR), 2))
    y = y[: int(L * SR)]
    rms = np.sqrt((y ** 2).mean() + 1e-12)
    y = y * (0.09 / rms)
    _CACHE[mood] = y
    return y


def bed(mood, seconds, fade=1.5):
    """Musique de la durée voulue (boucle avec fondus)."""
    y = cue(mood)
    n = int(seconds * SR)
    reps = int(np.ceil(n / len(y))) + 1
    out = np.concatenate([y] * reps)[:n].copy()
    k = min(int(fade * SR), n // 3)
    if k > 0:
        out[:k] *= np.linspace(0, 1, k)[:, None]; out[-k:] *= np.linspace(1, 0, k)[:, None]
    return out
