"""Rapporteur (rôle du Directeur) : écrit le rapport du jour en français."""
import os


def write(date, results, guard_issues, guard_notes, analytics, uploaded, path):
    L = [f"# Rapport Sleepy Mimo — {date}", ""]
    ok = all(not r["problemes"] for r in results) and not guard_issues
    L.append("**Statut : ✅ tout est prêt**" if ok else "**Statut : ⚠️ certaines vidéos ont été bloquées, voir ci-dessous**")
    L.append("")
    L.append("## Vidéos produites")
    for r in results:
        etat = "envoyée en PRIVÉ sur la chaîne" if r.get("video_id") else ("bloquée" if r["problemes"] else "prête (non envoyée)")
        L.append(f"- **{r['type']}** — {r['titre']}  ")
        L.append(f"  Durée : {r['infos'].get('duree', '?')} s · Son moyen : {r['infos'].get('volume_moyen', '?')} dB · État : {etat}")
        if r.get("video_id"):
            L.append(f"  Lien : https://studio.youtube.com/video/{r['video_id']}/edit")
        for p in r["problemes"]:
            L.append(f"  - ❌ {p}")
    L.append("")
    L.append("## Gardien des règles")
    L += [f"- ❌ {i}" for i in guard_issues] or ["- ✅ Aucun problème détecté."]
    L += [f"- ℹ️ {n}" for n in guard_notes]
    L.append("")
    L.append("## Statistiques de la chaîne")
    if analytics:
        L.append(f"- Abonnés : {analytics['abonnes']} · Vues totales : {analytics['vues']} · Vidéos : {analytics['videos']}")
        for v in analytics["dernieres"]:
            L.append(f"  - {v['titre']} — {v['vues']} vues ({v['statut']})")
    else:
        L.append("- Non disponibles (connexion YouTube pas encore configurée).")
    L.append("")
    L.append("## Ce que tu dois faire aujourd'hui (5 minutes)")
    if uploaded:
        L.append("1. Ouvre YouTube Studio → Contenu. Les nouvelles vidéos sont en **Privé**.")
        L.append("2. Regarde-les rapidement. Si une est ratée, supprime-la.")
        L.append("3. Passe les autres en **Public** (ou programme-les à des heures différentes).")
    else:
        L.append("1. Va dans l'onglet **Actions** de ton dépôt GitHub → la dernière exécution → **Artifacts**.")
        L.append("2. Télécharge les vidéos et miniatures, regarde-les, puis mets-les en ligne toi-même.")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write("\n".join(L) + "\n")
    return "\n".join(L)
