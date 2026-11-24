"""Fabrique une partie des voix d'un épisode (plusieurs machines en parallèle)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from perso import episodes as E, voix as V
num, k, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
V.synth_shard(E.EPISODES[num], k, n, f"voix_ep{num}")
