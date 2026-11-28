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
    n = int(os.environ.get("TIKTOK_COUNT") or cfg.get("n_tiktok") or 0)
    if not n:
        log("TikTok : nombre de vidéos = 0 (consignes.yml). Rien à produire.")
        return
    shutil.rmtree(OUT, ignore_errors=True)
    notes = tiktok_fr.produce(date, n, OUT, log=log)
    for note in notes:
        log(note)
    if not os.path.exists(f"{OUT}/tiktok1.mp4"):
        raise SystemExit("Aucune vidéo TikTok produite.")


if __name__ == "__main__":
    main()
