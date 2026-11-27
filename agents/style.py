"""Style visuel de l'épisode en cours : « s1 » (dessin enfantin, saison 1) ou « s2 » (animaux réalistes 2.5D, saison 2)."""
_S2 = False


def set_style(name):
    global _S2
    _S2 = (name == "s2")


def s2():
    return _S2
