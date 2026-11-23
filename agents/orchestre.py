"""Agent 21 — Orchestre : joue les morceaux avec de vrais instruments échantillonnés (banque FluidR3, gratuite).
Arrangement complet : mélodie, cordes douces, basse, arpèges de harpe/guitare, petites percussions pour les chansons,
contre-chant de flûte au 2e passage. Rendu par FluidSynth avec réverbération et chorus."""
import os, subprocess, tempfile, wave
import numpy as np

SR = 44100
SOUNDFONT = next((p for p in ["sf2/FluidR3_GM.sf2", "/usr/share/sounds/sf2/FluidR3_GM.sf2", "/usr/share/sounds/sf2/default-GM.sf2"] if os.path.exists(p)), None)
# instrument de la mélodie (numéros General MIDI)
MELODY = {"box": 10, "soft": 0, "harp": 46, "bell": 8}
CHORDS = {'C': [0, 4, 7], 'F': [5, 9, 12], 'G': [7, 11, 14], 'Am': [9, 12, 16]}


def available():
    if not SOUNDFONT:
        return False
    try:
        subprocess.run(["fluidsynth", "--version"], capture_output=True, check=True)
        import mido  # noqa
        return True
    except Exception:
        return False


def _midi(bpm, mel, ch, voice, transpose, reps, seed, lively, melody_octave):
    import mido
    rng = np.random.default_rng(seed)
    tpb = 480
    mid = mido.MidiFile(ticks_per_beat=tpb)
    events = []  # (tick, type, channel, note/program, velocity)

    def note(ch_, start_beats, dur_beats, n, vel):
        s = int(start_beats * tpb + rng.normal(0, 6)) if start_beats > 0 else 0
        e = int((start_beats + dur_beats) * tpb) - 10
        v = int(np.clip(vel * (1 + rng.normal(0, 0.07)), 20, 120))
        events.append((max(0, s), 1, ch_, n, v))
        events.append((max(s + 20, e), 0, ch_, n, 0))

    programs = {0: MELODY.get(voice, 10), 1: 49, 2: 32, 3: 46 if voice != "harp" else 24, 4: 73}
    L = sum(d for _, d in mel)
    for r in range(reps):
        off = r * L
        t = off
        oc = melody_octave
        for m, d in mel:
            note(0, t, d * 0.95, 60 + m + oc + transpose, 78 if r % 2 == 0 else 70)
            t += d
        t = off
        for c, d in ch:
            tones = CHORDS[c]
            for k in tones:
                note(1, t, d, 48 + transpose + k, 38)
            note(2, t, min(d, 2), 36 + transpose + tones[0], 62)
            if d >= 2:
                note(2, t + 2, d - 2, 36 + transpose + tones[0] + (7 if c != "Am" else 3), 50)
            arp = tones + [tones[0] + 12]
            for i in range(int(d * 2)):
                note(3, t + i * 0.5, 0.5, 60 + transpose + arp[i % len(arp)] - 12 * (i % 2 == 0), 42 if r > 0 else 30)
            if lively:
                for i in range(int(d * 2)):
                    if i % 2 == 1:
                        note(9, t + i * 0.5, 0.25, 70, 34)          # maracas sur les contretemps
                    if i % 4 == 0:
                        note(9, t + i * 0.5, 0.25, 75, 28)          # claves très doux
            t += d
        if r % 2 == 1 and reps > 1:                                  # contre-chant de flûte
            t = off
            for c, d in ch:
                note(4, t + d / 2, d / 2, 72 + transpose + CHORDS[c][1], 40)
                t += d
    tr = mido.MidiTrack(); mid.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    for c_, prog in programs.items():
        tr.append(mido.Message("program_change", channel=c_, program=prog, time=0))
        tr.append(mido.Message("control_change", channel=c_, control=91, value=70, time=0))   # réverbération
        tr.append(mido.Message("control_change", channel=c_, control=93, value=30, time=0))   # chorus
        tr.append(mido.Message("control_change", channel=c_, control=10, value={0: 64, 1: 44, 2: 64, 3: 84, 4: 74}[c_], time=0))
    events.sort(key=lambda e: (e[0], e[1]))
    last = 0
    for tick, kind, c_, n, v in events:
        msg = "note_on" if kind == 1 else "note_off"
        tr.append(mido.Message(msg, channel=c_, note=int(np.clip(n, 0, 127)), velocity=v, time=tick - last))
        last = tick
    return mid, L * 60 / bpm * reps


def render(bpm, mel, ch, voice, octave, transpose, min_seconds, seed=0, lively=False):
    """Renvoie un signal stéréo (n, 2) à 44,1 kHz, avec fondu de fin."""
    L = sum(d for _, d in mel) * 60 / bpm
    reps = max(1, int(np.ceil(min_seconds / L)))
    mid, dur = _midi(bpm, mel, ch, voice, transpose, reps, seed, lively, octave)
    with tempfile.TemporaryDirectory() as td:
        mp, wp = os.path.join(td, "m.mid"), os.path.join(td, "o.wav")
        mid.save(mp)
        subprocess.run(["fluidsynth", "-ni", "-q", "-g", "0.55", "-r", str(SR), "-F", wp, SOUNDFONT, mp],
                       check=True, capture_output=True)
        w = wave.open(wp)
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64).reshape(-1, w.getnchannels()) / 32768
    n = int(SR * (dur + 4))
    x = x[:n] if len(x) >= n else np.concatenate([x, np.zeros((n - len(x), x.shape[1]))])
    k = int(SR * 4); x[-k:] *= np.linspace(1, 0, k)[:, None]
    rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    x = x * (0.085 / rms)                     # volume régulier d'un morceau à l'autre
    return x / max(1.0, np.abs(x).max() / 0.85)
