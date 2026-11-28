"""Rendu 3D des vidéos TikTok : états de scène -> images (three.js dans un Chrome sans écran) -> assemblage par le monteur.

Chaque image est décrite par un petit dictionnaire (décor, caméra, personnages et leurs poses). render3d/render.js les dessine
dans le navigateur (WebGL logiciel SwiftShader : aucune carte graphique nécessaire) puis le monteur ajoute les sous-titres nets.
"""
import json
import math
import os
import shutil
import subprocess

RENDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render3d")


def disponible():
    ok_node = shutil.which("node") is not None
    ok_mod = os.path.isdir(os.path.join(RENDER, "node_modules", "three")) and os.path.isdir(os.path.join(RENDER, "node_modules", "puppeteer-core"))
    ok_chrome = any(shutil.which(c) for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")) or bool(os.environ.get("CHROME_PATH"))
    return ok_node and ok_mod and ok_chrome


def rendre(states, out_dir, w=1080, h=1920, workers=None, log=print):
    """Écrit out_dir/f000000.jpg, f000001.jpg... une image par état. Plusieurs navigateurs travaillent en parallèle."""
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)
    fs = os.path.join(out_dir, "etats.json")
    with open(fs, "w") as f:
        json.dump(states, f)
    n = len(states)
    workers = workers or int(os.environ.get("RENDU3D_PROCESSUS") or max(1, min(4, (os.cpu_count() or 2) // 2 or 1)))
    size = math.ceil(n / workers)
    procs = []
    for k in range(workers):
        a, b = k * size, min(n, (k + 1) * size)
        if a >= n:
            break
        procs.append(subprocess.Popen(["node", "render.js", os.path.abspath(fs), os.path.abspath(out_dir), str(a), str(b), str(w), str(h)], cwd=RENDER))
    log(f"rendu 3D : {n} images, {len(procs)} navigateur(s)")
    codes = [p.wait() for p in procs]
    if any(codes):
        raise RuntimeError(f"rendu 3D échoué (codes {codes})")
    missing = [i for i in range(n) if not os.path.exists(os.path.join(out_dir, f"f{i:06d}.jpg"))]
    if missing:
        raise RuntimeError(f"rendu 3D : {len(missing)} images manquantes (première : {missing[0]})")
    os.remove(fs)
    return out_dir
