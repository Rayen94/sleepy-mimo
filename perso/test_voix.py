"""Cherche de VRAIES voix tunisiennes (LinTO, CC BY 4.0) pour servir de référence à Habibi-TTS :
découpe des extraits de 6,5 s, les transcrit avec Whisper, fait parler Habibi avec chacun,
et garde celles qui sont les mieux comprises."""
import io, json, os, sys, time, subprocess
import numpy as np, soundfile as sf
import parselmouth
from huggingface_hub import list_repo_files, hf_hub_download
import pyarrow.parquet as pq

OUT = "perso/tests"; REFS = "perso/refs"
os.makedirs(OUT, exist_ok=True); os.makedirs(REFS, exist_ok=True)
REPO = "linagora/linto-dataset-audio-ar-tn"
log = open(f"{OUT}/log2.txt", "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); log.write(s + "\n"); log.flush()


files = [f for f in list_repo_files(REPO, repo_type="dataset") if f.endswith(".parquet")]
want = ["STT-TTS15s", "AmenyKH/test", "ApprendreLeTunisien/test", "OneStory/test", "Youtube_TN_Shorts", "TunSwitchTO/test"]
picked = [next(f for f in files if k in f) for k in want if any(k in f for f in files)]
P("picked", picked)


def decode(cell):
    if isinstance(cell, dict):
        b = cell.get("bytes")
        if b:
            p = "/tmp/_a.bin"; open(p, "wb").write(b)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-ar", "24000", "-ac", "1", "/tmp/_a.wav"])
            if os.path.exists("/tmp/_a.wav"):
                y, sr = sf.read("/tmp/_a.wav"); os.remove("/tmp/_a.wav"); return y, sr
        if cell.get("array") is not None:
            return np.asarray(cell["array"]), cell.get("sampling_rate", 16000)
    return None, None


cands = []
for f in picked:
    try:
        path = hf_hub_download(REPO, f, repo_type="dataset")
        pf = pq.ParquetFile(path)
        t = pf.read_row_group(0)
    except Exception as e:
        P("skip", f, e); continue
    cols = t.column_names
    P(f, cols, t.num_rows)
    acol = next(c for c in cols if "audio" in c.lower() and c != "audio_id")
    for i in range(min(t.num_rows, 25)):
        cell = t[acol][i].as_py()
        if i == 0:
            P("  cell", type(cell).__name__, {k: (type(v).__name__, len(v) if hasattr(v, "__len__") else v) for k, v in cell.items()} if isinstance(cell, dict) else "")
        y, sr = decode(cell)
        if y is None:
            continue
        if y.ndim > 1:
            y = y.mean(1)
        win = int(6.5 * sr)
        starts = [0] if len(y) <= win * 1.2 else list(range(0, len(y) - win, win))[:6]
        for s0 in starts:
            seg = y[s0:s0 + win]
            if len(seg) < 4 * sr:
                continue
            f0 = parselmouth.Sound(seg, sr).to_pitch().selected_array["frequency"]; f0 = f0[f0 > 0]
            if len(f0) < 120:
                continue
            fr = seg[: len(seg) // 512 * 512].reshape(-1, 512)
            e = np.sqrt((fr ** 2).mean(1) + 1e-12)
            snr = 20 * np.log10(np.percentile(e, 95) / max(np.percentile(e, 10), 1e-6))
            voiced = len(f0) / (len(seg) / sr * 100)
            cands.append(dict(src=f, i=i, f0=float(np.median(f0)), snr=float(snr), voiced=voiced, y=seg, sr=sr))
P("candidats", len(cands))


def top(lst, n):
    out, per, seen = [], {}, set()
    for c in sorted(lst, key=lambda c: -(c["snr"] + 20 * c["voiced"])):
        key = (c["src"], c["i"])
        if per.get(c["src"], 0) < 2 and key not in seen:
            out.append(c); per[c["src"]] = per.get(c["src"], 0) + 1; seen.add(key)
        if len(out) >= n:
            break
    return out


fem = top([c for c in cands if c["f0"] > 170], 6)
mal = top([c for c in cands if 85 < c["f0"] < 150], 6)

from faster_whisper import WhisperModel
asr = WhisperModel("medium", device="cpu", compute_type="int8")


def transcribe(p):
    segs, _ = asr.transcribe(p, language="ar", beam_size=5)
    return " ".join(s.text for s in segs).strip()


refs = []
for g, lst in (("F", fem), ("M", mal)):
    for k, c in enumerate(lst):
        p = f"{REFS}/tn_{g}{k}.wav"
        y = c["y"] / (np.abs(c["y"]).max() + 1e-9) * 0.9
        sf.write(p, y, c["sr"])
        txt = transcribe(p)
        refs.append(dict(name=f"tn_{g}{k}", path=p, text=txt, gender=g, f0=c["f0"], snr=c["snr"], src=c["src"]))
        P(g, k, round(c["f0"]), round(c["snr"], 1), c["src"].split("/")[1], "|", txt)

import torch
torch.set_num_threads(os.cpu_count() or 4)
from importlib.resources import files as pfiles
from cached_path import cached_path
from omegaconf import OmegaConf
from hydra.utils import get_class
from f5_tts.infer.utils_infer import load_model, load_vocoder, preprocess_ref_audio_text
from habibi_tts.infer.utils_infer import infer_process
from habibi_tts.model.utils import dialect_id_map
cfg = OmegaConf.load(str(pfiles("f5_tts").joinpath("configs/F5TTS_v1_Base.yaml")))
model = load_model(get_class(f"f5_tts.model.{cfg.model.backbone}"), cfg.model.arch,
                   str(cached_path("hf://SWivid/Habibi-TTS/Unified/model_200000.safetensors")), mel_spec_type="vocos",
                   vocab_file=str(cached_path("hf://SWivid/Habibi-TTS/Unified/vocab.txt")), device="cpu")
voc = load_vocoder(vocoder_name="vocos", device="cpu")
sys.path.insert(0, ".")
from perso.voix import cer

TEST = "يا زرقة، راني ما نردّش بيك، موش كي تقعد آخر مرّة. توّا نمشي للبحر وحدي."
for r in refs:
    if len(r["text"]) < 12:
        r["cer"] = 9; continue
    try:
        ra, rt = preprocess_ref_audio_text(r["path"], r["text"])
        t0 = time.time()
        wav, sr, _ = infer_process(ra, rt, TEST, model, voc, mel_spec_type="vocos", nfe_step=16, cfg_strength=2.0,
                                   sway_sampling_coef=-1.0, speed=1.0, device="cpu", dialect_id=dialect_id_map["TUN"])
        p = f"{OUT}/{r['name']}.wav"; sf.write(p, wav, sr)
        hyp = transcribe(p)
        r["cer"] = cer(TEST, hyp); r["hyp"] = hyp; r["secs"] = time.time() - t0
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p, "-b:a", "48k", p[:-4] + ".mp3"]); os.remove(p)
        P(r["name"], "cer", round(r["cer"], 2), "|", hyp)
    except Exception as e:
        r["cer"] = 9; P(r["name"], "erreur", e)
json.dump(refs, open(f"{REFS}/tn_refs.json", "w"), ensure_ascii=False, indent=1)
P("FINI")
