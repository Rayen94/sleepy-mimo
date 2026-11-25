"""Pour chaque réplique : est-ce qu'on l'entend vraiment dans la vidéo finie, au bon moment ?"""
import os, sys, json, subprocess
import numpy as np, soundfile as sf
sys.path.insert(0, ".")
from perso import episodes as E, film as F, voix as V
from faster_whisper import WhisperModel
asr = WhisperModel("small", device="cpu", compute_type="int8")
out = []
for num in (1, 2, 3, 4):
    mp4 = next((os.path.join(d, f) for d, _, fs in os.walk("verif") for f in fs if f == f"rayen_yakin_ep{num}.mp4"), None)
    if not mp4 or not os.path.isdir(f"voix_ep{num}"):
        out.append(f"ep{num}: fichiers absents"); continue
    ep = E.EPISODES[num]
    voices = V.load_voices(ep, f"voix_ep{num}")
    shots, total = F.plan(ep, voices)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vn", "-ac", "1", "-ar", "16000", "/tmp/a.wav"])
    y, sr = sf.read("/tmp/a.wav")
    bad = 0; n = 0
    for s in shots:
        if s.get("replay"):
            continue
        for ln in s["lines_t"]:
            n += 1
            t0 = s["start"] + ln["start"]; t1 = t0 + ln["dur"]
            seg = y[int(t0 * sr): int(t1 * sr)]
            rms_win = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)
            v = voices[ln["key"]][0]
            rms_v = 20 * np.log10(np.sqrt((v ** 2).mean()) + 1e-9) if len(v) else -120
            sf.write("/tmp/l.wav", seg, sr)
            segs, _ = asr.transcribe("/tmp/l.wav", language="ar", beam_size=2)
            hyp = " ".join(x.text for x in segs).strip()
            c = V.cer(ln["text"], hyp)
            flag = c > 0.6 or rms_v < -45
            bad += flag
            out.append(f"ep{num} {ln['key']} {ln['who']:8s} t={t0:6.1f} dur={ln['dur']:.1f} voix={rms_v:.0f}dB fenêtre={rms_win:.0f}dB cer={c:.2f} {'❌' if flag else 'ok'} | {ln['text']} | {hyp}")
    out.append(f"== ep{num}: {bad}/{n} répliques douteuses")
    print(out[-1], flush=True)
os.makedirs("perso/resultats", exist_ok=True)
open("perso/resultats/diag.txt", "w").write("\n".join(out) + "\n")
