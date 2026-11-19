"""Agent 12 — Analyste : lit les statistiques de la chaîne pour le rapport quotidien."""


def stats(yt, n=8):
    ch = yt.channels().list(part="statistics,contentDetails,snippet", mine=True).execute()["items"][0]
    s = ch["statistics"]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    items = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=n).execute().get("items", [])
    ids = [i["contentDetails"]["videoId"] for i in items]
    vids = []
    if ids:
        for v in yt.videos().list(part="snippet,statistics,status", id=",".join(ids)).execute()["items"]:
            vids.append(dict(titre=v["snippet"]["title"], vues=int(v["statistics"].get("viewCount", 0)),
                             statut=v["status"]["privacyStatus"]))
    return dict(chaine=ch["snippet"]["title"], abonnes=s.get("subscriberCount"), vues=s.get("viewCount"),
                videos=s.get("videoCount"), dernieres=vids)
