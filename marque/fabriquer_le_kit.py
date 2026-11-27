import sys; sys.path.insert(0,'/home/claude/sleepy-mimo')
import cairosvg
from agents import style, decors as D, personnages as PE, illustrateur as I
style.set_style("s2")
# ---------- Avatar 800x800 : tête de Mimo sur la lune
def avatar(path):
    W=800
    body=[f'<defs><radialGradient id="av" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="#5B6BD6"/><stop offset="1" stop-color="#1B1F5E"/></radialGradient>'
          '<radialGradient id="mg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFF3B0" stop-opacity="0.95"/><stop offset="0.55" stop-color="#FFE98A" stop-opacity="0.5"/><stop offset="1" stop-color="#FFE98A" stop-opacity="0"/></radialGradient></defs>',
          f'<rect width="{W}" height="{W}" fill="url(#av)"/>',
          '<circle cx="400" cy="400" r="380" fill="url(#mg)"/>',
          '<circle cx="400" cy="400" r="260" fill="#FFF1B8"/>']
    import random; r=random.Random(4)
    for _ in range(26):
        x,y=r.randint(30,770),r.randint(30,200); body.append(f'<circle cx="{x}" cy="{y}" r="{r.choice([2,3,4])}" fill="#fff" opacity="{r.choice([0.5,0.8,1])}"/>')
    s=4.0
    b=PE.draw("mimo", 0, 0, s, mouth=0.35, blink=False, facing=1)
    body.append(f'<g transform="translate(60 300)">{b}</g>')
    open('/tmp/kit/av_body.svg','w').write(I.svg(W,W,"".join(body)))
    cairosvg.svg2png(bytestring=I.svg(W,W,"".join(body)).encode(), write_to=path)
avatar('/tmp/kit/avatar_test.png')

# ---------- Bannière 2560x1440 (zone visible partout : 1546x423 au centre)
def banner(path):
    W,H=2560,1440
    dec="meadow_night"
    parts=[D.DECORS[dec](0.25, 5)]
    g=D.ground(dec)
    for who,x,s,face in (("mimo",330,1.9,1),("fox",1110,1.5,-1),("owl",60,1.0,1),("bunny",1230,1.1,-1)):
        if who in ("owl","bunny"): continue
        y=g+40-134*s
        parts.append(PE.draw(who,x-90*s,y,s,mouth=0.3 if who=="mimo" else 0.0,facing=face,wave=0.0))
    parts.append(D.foreground(dec,0.25))
    body='<g transform="scale(2)">'+"".join(parts)+'</g>'
    body+='<rect x="480" y="470" width="1600" height="470" rx="60" fill="#10163F" opacity="0.38"/>'
    body+=I.text(1280,690,"Sleepy Mimo",210,"#FFFFFF")
    body+=I.text(1280,810,"Cozy animal bedtime stories &amp; lullabies",78,"#FFE37A")
    body+=I.text(1280,900,"A new adventure every day",56,"#FFD1E8",700)
    cairosvg.svg2png(bytestring=I.svg(W,H,body).encode(), write_to=path)
banner('/tmp/kit/banner_test.png')
