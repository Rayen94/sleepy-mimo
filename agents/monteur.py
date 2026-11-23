"""Agent 5 — Monteur : transforme les images en vidéo (tous les cœurs du processeur en parallèle),
enchaîne les décors avec des fondus et pose la musique."""
import os, subprocess, json, math
from multiprocessing import Pool

FPS = 30
X264 = ["-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-pix_fmt", "yuv420p",
        "-profile:v", "high", "-x264-params", "repeat-headers=1"]


def _raster(svg):
    import cairosvg
    return cairosvg.svg2png(bytestring=svg.encode())


def _pool():
    return Pool(max(1, os.cpu_count() or 1))


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def encode(svg_frames, out, gop, audio=None, extra=(), crf=23):
    """Rastérise les images en parallèle et les envoie directement à ffmpeg (pas de fichiers temporaires)."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-"]
    if audio:
        cmd += ["-i", audio]
    cmd += X264 + ["-crf", str(crf), "-g", str(gop)]
    if audio:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart"]
    else:
        cmd += ["-an", "-f", "mpegts"]
    cmd += list(extra) + [out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with _pool() as pool:
        for png in pool.imap(_raster, svg_frames, chunksize=4):
            p.stdin.write(png)
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg a échoué pour {out}")
    return out


def assemble_long(scenes, wav, out, workdir, n_loop, n_trans):
    """scenes : liste de dicts {loop: fichier .ts, trans_in: fichier .ts ou None, start: seconde de début dans l'audio}.
    Construit la vidéo en enchaînant les boucles (copie sans réencodage) et les fondus, calée sur l'audio."""
    L, T = n_loop / FPS, n_trans / FPS
    D = duration(wav)
    entries, vt = [], 0.0
    for i, sc in enumerate(scenes):
        end = scenes[i + 1]["start"] if i + 1 < len(scenes) else D
        if sc.get("trans_in"):
            entries.append(sc["trans_in"]); vt += T
        if i + 1 < len(scenes):
            n = max(1, round((end - T / 2 - vt) / L))
        else:
            n = max(1, math.ceil((end - vt) / L))
        entries += [sc["loop"]] * n; vt += n * L
    lst = os.path.join(workdir, "concat.txt")
    with open(lst, "w") as f:
        for e in entries:
            f.write(f"file '{os.path.abspath(e)}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", f"{D:.3f}", "-movflags", "+faststart", out], check=True)
    return duration(out)


def loudness(path):
    p = subprocess.run(["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    mean = maxv = None
    for line in p.stderr.splitlines():
        if "mean_volume" in line: mean = float(line.split(":")[1].split()[0])
        if "max_volume" in line: maxv = float(line.split(":")[1].split()[0])
    return mean, maxv


def decode_ok(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    return p.returncode == 0 and not p.stderr.strip(), p.stderr.strip()[:300]
