"""Réécoute les vidéos finies : piste son présente ? voix audibles du début à la fin ? (Whisper)"""
import glob, json, os, subprocess
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
asr = WhisperModel("small", device="cpu", compute_type="int8")
out = ["# Vérification du son"]
for mp4 in sorted(glob.glob("verif/**/*.mp4", recursive=True)):
    info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,channels,sample_rate",
                           "-show_entries", "format=duration", "-of", "json", mp4], capture_output=True, text=True).stdout
    j = json.loads(info)
    dur = float(j["format"]["duration"])
    out.append(f"\n## {os.path.basename(mp4)} ({os.path.getsize(mp4)//1e6:.0f} Mo, {dur/60:.1f} min)")
    out.append("flux : " + ", ".join(f"{s['codec_type']}:{s.get('codec_name')}" for s in j["streams"]))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vn", "-ac", "1", "-ar", "16000", "/tmp/a.wav"])
    y, sr = sf.read("/tmp/a.wav")
    per_min = [20 * np.log10(np.sqrt((y[i:i + 60 * sr] ** 2).mean()) + 1e-9) for i in range(0, len(y), 60 * sr)]
    out.append("niveau par minute (dB) : " + " ".join(f"{v:.0f}" for v in per_min))
    n = 6
    for k in range(n):
        t0 = (dur - 25) * k / (n - 1)
        sf.write("/tmp/w.wav", y[int(t0 * sr): int((t0 + 20) * sr)], sr)
        segs, _ = asr.transcribe("/tmp/w.wav", language="ar", beam_size=2, vad_filter=True)
        txt = " ".join(s.text for s in segs).strip()
        out.append(f"- {int(t0//60)}:{int(t0%60):02d} → {len(txt.split())} mots : {txt[:160]}")
    print("\n".join(out[-9:]), flush=True)
os.makedirs("perso/resultats", exist_ok=True)
open("perso/resultats/verif.md", "w").write("\n".join(out) + "\n")
