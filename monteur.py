"""Agent 5 — Monteur : assemble l'animation en boucle et la musique en vidéo finale."""
import subprocess, json


def _run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def encode_loop(frames_dir, out, fps=24):
    _run(["ffmpeg", "-y", "-framerate", str(fps), "-i", f"{frames_dir}/%04d.png", "-c:v", "libx264",
          "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", "-g", "288", out])


def mux(loop, wav, out):
    d = duration(wav)
    _run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", loop, "-i", wav, "-map", "0:v", "-map", "1:a",
          "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", f"{d:.3f}", "-movflags", "+faststart", out])
    return duration(out)


def loudness(path):
    p = subprocess.run(["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    mean = maxv = None
    for line in p.stderr.splitlines():
        if "mean_volume" in line: mean = float(line.split(":")[1].split()[0])
        if "max_volume" in line: maxv = float(line.split(":")[1].split()[0])
    return mean, maxv
