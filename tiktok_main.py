"""Production quotidienne TikTok (en français), SÉPARÉE de YouTube : son propre workflow, ses propres vidéos.
Écrit output_tiktok/tiktok1.mp4, tiktok2.mp4… et output_tiktok/tiktok.md (légendes à copier). Ne publie rien."""
import os, datetime, shutil
from agents import consignes, tiktok_fr

OUT = "output_tiktok"


def log(msg):
    print(f" [{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def main():
    date = os.environ.get("RUN_DATE") or datetime.date.today().isoformat()
    cfg, _ = consignes.load()
    ids = [x.strip() for x in (os.environ.get("TIKTOK_IDS") or "").split(",") if x.strip()]
    only = int(os.environ.get("TIKTOK_INDEX") or 0) or None      # rendu en parallèle : une vidéo par machine
    n = len(ids) or int(os.environ.get("TIKTOK_COUNT") or cfg.get("n_tiktok") or 0)
    if not n:
        log("TikTok : nombre de vidéos = 0 (consignes.yml). Rien à produire.")
        return
    shutil.rmtree(OUT, ignore_errors=True)
    if only and only > n:
        log(f"TikTok : pas de vidéo n°{only} aujourd'hui (il y en a {n}).")
        return
    notes = tiktok_fr.produce(date, n, OUT, log=log, ids=ids or None, only=only)
    for note in notes:
        log(note)
    if not any(f.endswith(".mp4") for f in os.listdir(OUT) if os.path.isdir(OUT)):
        raise SystemExit("Aucune vidéo TikTok produite.")


if __name__ == "__main__":
    main()
