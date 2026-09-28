"""HV World: "Riya's story". Builds index.html (and favicon.svg) from this file and the logos in src/.

Run from the repo root:  python3 src/story.py
Every picture is hand-drawn inline SVG. Scroll steps switch a scene's data-step (1-4) and CSS shows,
hides and animates the parts marked v1..v4. No libraries."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

def read(n):
    return open(os.path.join(HERE, n)).read().strip()

# ---------------------------------------------------------------- logos (unique ids per copy)
_LOGOS = {k: read(f).replace('xmlns="http://www.w3.org/2000/svg" ', '') for k, f in
          {"world": "world.svg", "test": "logo-test.svg", "reset": "logo-reset.svg", "vault": "logo-vault.svg"}.items()}
_n = [0]
def logo(name, cls="", size=None):
    _n[0] += 1
    s = _LOGOS[name]
    for i in re.findall(r'id="([^"]+)"', s):
        s = s.replace('id="%s"' % i, 'id="%s-%d"' % (i, _n[0])).replace("url(#%s)" % i, "url(#%s-%d)" % (i, _n[0]))
    attrs = 'aria-hidden="true" focusable="false"' + (' class="%s"' % cls if cls else "")
    if size: attrs += ' width="%d" height="%d"' % (size, size)
    return re.sub(r"<svg ", "<svg %s " % attrs, s, count=1).replace('aria-hidden="true" aria-hidden="true"', 'aria-hidden="true"')

def logo_at(name, x, y, size):          # a logo placed inside a scene
    _n[0] += 1
    s = _LOGOS[name]
    for i in re.findall(r'id="([^"]+)"', s):
        s = s.replace('id="%s"' % i, 'id="%s-%d"' % (i, _n[0])).replace("url(#%s)" % i, "url(#%s-%d)" % (i, _n[0]))
    s = re.sub(r'<svg[^>]*viewBox="([^"]+)"[^>]*>', lambda m: '<svg x="%g" y="%g" width="%g" height="%g" viewBox="%s">' % (x, y, size, size, m.group(1)), s, count=1)
    return s

# ---------------------------------------------------------------- the characters
SKIN, HAIR, TOP, INK, CHEEK = "#F0C29E", "#2A2238", "#5B6FE0", "#1D1D1F", "#F2A0A0"

def riya(x, y, s=1.0, faces=None, arms=None, cls="", sweat=None, bulb=None):
    """Riya, upper body. faces/arms map a variant to the step classes where it shows (e.g. {'w': 'v1'})."""
    faces = faces or {"n": ""}
    arms = arms or {"down": ""}
    p = []
    p.append('<path d="M-40,-118 C-48,-166 48,-166 40,-118 L44,-64 C30,-52 -30,-52 -44,-64Z" fill="%s"/>' % HAIR)  # hair behind
    p.append('<rect x="-9" y="-64" width="18" height="22" rx="7" fill="%s"/>' % SKIN)
    p.append('<path d="M-60,26 C-60,-26 -42,-46 0,-46 C42,-46 60,-26 60,26 Z" fill="%s"/>' % TOP)
    p.append('<path d="M-14,-46 L0,-30 L14,-46" fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="3" stroke-linecap="round"/>')
    p.append('<circle cx="-34" cy="-92" r="6" fill="%s"/><circle cx="34" cy="-92" r="6" fill="%s"/>' % (SKIN, SKIN))
    p.append('<circle cx="0" cy="-94" r="35" fill="%s"/>' % SKIN)
    p.append('<path d="M-36,-98 C-34,-138 34,-142 37,-100 C26,-118 -8,-122 -36,-98Z" fill="%s"/>' % HAIR)       # fringe
    F = {
        "w": '<path d="M-19,-101 L-7,-106 M19,-101 L7,-106" stroke="%s" stroke-width="3" stroke-linecap="round"/><circle cx="-12" cy="-92" r="3.4" fill="%s"/><circle cx="12" cy="-92" r="3.4" fill="%s"/><path d="M-9,-73 Q0,-80 9,-73" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (INK, INK, INK, INK),
        "t": '<path d="M-18,-92 L-7,-92 M7,-92 L18,-92" stroke="%s" stroke-width="3" stroke-linecap="round"/><path d="M-19,-102 L-7,-104 M19,-102 L7,-104" stroke="%s" stroke-width="3" stroke-linecap="round"/><path d="M-7,-75 L7,-75" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (INK, INK, INK),
        "n": '<path d="M-19,-104 L-7,-104 M19,-104 L7,-104" stroke="%s" stroke-width="3" stroke-linecap="round"/><circle cx="-12" cy="-92" r="3.4" fill="%s"/><circle cx="12" cy="-92" r="3.4" fill="%s"/><path d="M-8,-76 Q0,-72 8,-76" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (INK, INK, INK, INK),
        "h": '<path d="M-17,-91 Q-12,-97 -7,-91 M7,-91 Q12,-97 17,-91" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/><circle cx="-21" cy="-80" r="5" fill="%s" opacity=".7"/><circle cx="21" cy="-80" r="5" fill="%s" opacity=".7"/><path d="M-11,-79 Q0,-66 11,-79" fill="%s"/>' % (INK, CHEEK, CHEEK, INK),
    }
    for k, c in faces.items():
        p.append('<g class="%s">%s</g>' % (("t " + c) if c else "", F[k]))
    def arm(d, hx, hy):
        return '<path d="%s" fill="none" stroke="%s" stroke-width="17" stroke-linecap="round"/><circle cx="%g" cy="%g" r="8.5" fill="%s"/>' % (d, TOP, hx, hy, SKIN)
    A = {
        "down": arm("M-50,-26 C-64,-8 -66,10 -62,24", -62, 28) + arm("M50,-26 C64,-8 66,10 62,24", 62, 28),
        "desk": arm("M-50,-26 C-62,-6 -52,14 -30,20", -26, 20) + arm("M50,-26 C62,-6 52,14 30,20", 26, 20),
        "phone": arm("M-50,-26 C-64,-8 -66,10 -62,24", -62, 28) + arm("M50,-26 C66,-6 52,8 24,2", 20, 0)
                 + '<rect x="4" y="-30" width="24" height="38" rx="5" fill="%s"/><rect x="7" y="-26" width="18" height="28" rx="2" fill="#7FD1AE"/>' % INK,
        "up": arm("M-50,-28 C-70,-58 -72,-86 -64,-110", -64, -114) + arm("M50,-28 C70,-58 72,-86 64,-110", 64, -114),
        "tea": arm("M-50,-26 C-62,-6 -52,12 -24,8", -20, 8) + arm("M50,-26 C62,-6 52,12 24,8", 20, 8)
               + '<path d="M-14,-14 h28 v18 a8,8 0 0 1 -8,8 h-12 a8,8 0 0 1 -8,-8Z" fill="#FFFFFF" stroke="%s" stroke-width="2.5"/><path d="M14,-8 a6,6 0 0 1 0,12" fill="none" stroke="%s" stroke-width="2.5"/><path class="steam" d="M-4,-22 q-4,-6 0,-12 q4,-6 0,-12" fill="none" stroke="#C7C7CC" stroke-width="2.5" stroke-linecap="round"/>' % (INK, INK),
        "reach": arm("M-50,-26 C-64,-8 -66,10 -62,24", -62, 28) + arm("M50,-28 C72,-48 84,-70 94,-96", 96, -100),
        "talk": arm("M-50,-26 C-64,-8 -66,10 -62,24", -62, 28) + arm("M50,-26 C70,-16 80,-30 88,-46", 90, -50),
    }
    for k, c in arms.items():
        p.append('<g class="%s">%s</g>' % (("t " + c) if c else "", A[k]))
    if sweat:
        p.append('<g class="t %s"><path class="sweat" d="M40,-122 q-7,11 0,16 q7,-5 0,-16Z" fill="#8EC5FF"/></g>' % sweat)
    if bulb:
        p.append('<g class="t %s"><g class="glow"><circle cx="0" cy="-196" r="30" fill="#FFE8A3" opacity=".6"/></g><path d="M-14,-194 a14,14 0 1 1 28,0 c0,8 -6,11 -7,18 h-14 c-1,-7 -7,-10 -7,-18Z" fill="#FFD256" stroke="%s" stroke-width="2.5"/><rect x="-7" y="-174" width="14" height="7" rx="2" fill="#9AA0AE"/></g>' % (bulb, INK))
    return '<g class="%s" transform="translate(%g %g) scale(%g)">%s</g>' % (cls, x, y, s, "".join(p))

def interviewer(x, y, cls=""):
    return ('<g class="%s" transform="translate(%g %g)">' % (cls, x, y) +
            '<path d="M-52,30 C-52,-22 -36,-40 0,-40 C36,-40 52,-22 52,30Z" fill="#3A4150"/>'
            '<path d="M-6,-40 L0,-4 L6,-40Z" fill="#B9C1DE"/>'
            '<rect x="-8" y="-58" width="16" height="20" rx="6" fill="#D6A57E"/>'
            '<circle cx="0" cy="-84" r="30" fill="#D6A57E"/>'
            '<path d="M-31,-88 C-30,-120 30,-122 31,-90 C22,-104 -10,-108 -31,-88Z" fill="#4A4F5C"/>'
            '<circle cx="-10" cy="-84" r="3" fill="%s"/><circle cx="10" cy="-84" r="3" fill="%s"/>'
            '<path d="M-7,-68 L7,-68" stroke="%s" stroke-width="3" stroke-linecap="round"/></g>' % (INK, INK, INK))

def bubble(x, y, w, h, text, tail="left", cls="", fill="#FFFFFF", size=17, color=INK, weight=600, tailx=None):
    tx = tailx if tailx is not None else (x + 26 if tail == "left" else x + w - 26)
    tl = ('<path d="M%g,%g l-8,22 l24,-22Z" fill="%s" stroke="#D2D2D7" stroke-width="1.5"/>' % (tx, y + h - 1, fill)) if tail == "left" else \
         ('<path d="M%g,%g l8,22 l-24,-22Z" fill="%s" stroke="#D2D2D7" stroke-width="1.5"/>' % (tx, y + h - 1, fill))
    lines = text.split("|")
    ts = "".join('<text x="%g" y="%g" font-size="%d" font-weight="%d" fill="%s">%s</text>' % (x + 18, y + h / 2 + size * .36 - (len(lines) - 1) * (size + 7) / 2 + i * (size + 7), size, weight, color, t) for i, t in enumerate(lines))
    return ('<g class="%s"><rect x="%g" y="%g" width="%g" height="%g" rx="18" fill="%s" stroke="#D2D2D7" stroke-width="1.5"/>%s'
            '<rect x="%g" y="%g" width="30" height="4" fill="%s"/>%s</g>') % (cls, x, y, w, h, fill, tl, tx - 12, y + h - 3, fill, ts)

def thought(x, y, w, h, inner, cls="", hx=None, hy=None):
    hx = hx if hx is not None else x - 10
    hy = hy if hy is not None else y + h + 20
    return ('<g class="%s"><circle cx="%g" cy="%g" r="6" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="1.5"/><circle cx="%g" cy="%g" r="10" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="1.5"/>'
            '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="1.5"/>%s</g>') % (
        cls, hx, hy, (hx + x) / 2 + 4, (hy + y + h) / 2, x, y, w, h, h / 2, inner)

def chair(cx, y):
    return ('<rect x="%g" y="%g" width="10" height="%g" rx="3" fill="#7F88A6"/><rect x="%g" y="%g" width="10" height="%g" rx="3" fill="#7F88A6"/>'
            '<rect x="%g" y="%g" width="176" height="12" rx="6" fill="#98A1BE"/>') % (cx - 76, y + 8, 416 - y - 8, cx + 66, y + 8, 416 - y - 8, cx - 88, y)

def desk(x, y, w):
    return ('<rect x="%g" y="%g" width="%g" height="16" rx="6" fill="#D8C2A2"/><rect x="%g" y="%g" width="12" height="86" rx="4" fill="#C5AD8B"/>'
            '<rect x="%g" y="%g" width="12" height="86" rx="4" fill="#C5AD8B"/>') % (x, y, w, x + 18, y + 14, x + w - 30, y + 14)

FLOOR = '<rect x="0" y="416" width="600" height="44" fill="#EEF0F4"/><rect x="0" y="414" width="600" height="3" fill="#E1E4EA"/>'

def scene(inner, label, bg="#F5F6FA"):
    return ('<svg class="art" viewBox="0 0 600 460" role="img" aria-label="%s"><rect width="600" height="460" rx="28" fill="%s"/>%s</svg>' % (label, bg, inner))

# ---------------------------------------------------------------- scenes
def prologue():
    stars = "".join('<circle class="twinkle" style="animation-delay:%.1fs" cx="%d" cy="%d" r="2.2" fill="#FFFFFF"/>' % (d, cx, cy)
                    for d, cx, cy in [(0, 92, 84), (.7, 150, 72), (1.3, 120, 118), (2, 176, 104)])
    papers = "".join('<rect x="%d" y="%d" width="70" height="8" rx="3" fill="%s" transform="rotate(%d %d %d)"/>' % (150 + i * 2, 318 - i * 9, c, r, 185, 318 - i * 9)
                     for i, (c, r) in enumerate([("#FFFFFF", -3), ("#F2F2F5", 2), ("#FFFFFF", -1), ("#ECEEF3", 4), ("#FFFFFF", 0)]))
    icons = ('<g class="pop" style="animation-delay:0s"><circle cx="404" cy="104" r="22" fill="#E3F2EA"/><text x="404" y="113" text-anchor="middle" font-size="24" font-weight="700" fill="#127A4F">?</text></g>'
             '<g class="pop" style="animation-delay:.6s"><circle cx="464" cy="104" r="22" fill="#E6EDF9"/><circle cx="464" cy="104" r="11" fill="none" stroke="#4A72C8" stroke-width="3"/><path d="M464,97 v7 l5,4" stroke="#4A72C8" stroke-width="3" fill="none" stroke-linecap="round"/></g>'
             '<g class="pop" style="animation-delay:1.2s"><circle cx="524" cy="104" r="22" fill="#F6EEDC"/><path d="M514,110 c0,-14 4,-19 10,-19 s10,5 10,19Z" fill="none" stroke="#A87A22" stroke-width="3" stroke-linejoin="round"/><circle cx="524" cy="114" r="2.5" fill="#A87A22"/></g>')
    inner = ('<rect x="64" y="56" width="140" height="104" rx="14" fill="#1F2A55"/><circle cx="176" cy="82" r="14" fill="#F6E7B8"/><circle cx="182" cy="78" r="12" fill="#1F2A55"/>' + stars +
             FLOOR + riya(270, 330, 1, faces={"t": ""}, arms={"desk": ""}) + desk(120, 322, 380) + papers +
             '<g><path d="M338,322 h118 l-10,-6 h-98Z" fill="#9AA0AE"/><rect x="350" y="248" width="94" height="66" rx="7" fill="#2B3350"/><rect class="glowlap" x="356" y="254" width="82" height="54" rx="3" fill="#8FA6FF" opacity=".55"/></g>'
             '<g><rect x="468" y="298" width="22" height="24" rx="5" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/><path class="steam" d="M479,292 q-4,-6 0,-12 q4,-6 0,-12" fill="none" stroke="#C7C7CC" stroke-width="2.5" stroke-linecap="round"/></g>' +
             thought(376, 70, 176, 68, icons, hx=318, hy=184))
    return scene(inner, "Riya at her desk late at night, worried about three things: who she is, where her day goes, and follow-ups", "#F2F3F8")

def ch_test():
    q = lambda y, on=False, cls="": ('<g class="%s"><rect x="378" y="%g" width="150" height="26" rx="8" fill="%s" stroke="%s" stroke-width="1.5"/><circle cx="394" cy="%g" r="6" fill="%s" stroke="%s" stroke-width="1.5"/><rect x="408" y="%g" width="%d" height="6" rx="3" fill="%s"/></g>') % (
        cls, y, "#E3F2EA" if on else "#FFFFFF", "#127A4F" if on else "#E5E5EA", y + 13, "#127A4F" if on else "#FFFFFF", "#127A4F" if on else "#C7C7CC", y + 10, 96 if on else 80, "#127A4F" if on else "#D8DAE0")
    bars = "".join('<rect class="bar" style="transition-delay:%.2fs" x="%d" y="%d" width="10" height="%d" rx="3" fill="#127A4F" opacity="%.2f"/>' % (i * .06, 386 + i * 14, 340 - h, h, .55 + .045 * i)
                   for i, h in enumerate([44, 62, 38, 70, 52, 58, 34, 66, 48, 60]))
    phone = ('<g class="t v2 v3"><rect x="360" y="64" width="186" height="334" rx="28" fill="%s"/><rect x="368" y="72" width="170" height="318" rx="22" fill="#FFFFFF"/>' % INK +
             logo_at("test", 380, 88, 24) + '<text x="412" y="106" font-size="14" font-weight="700" fill="%s">HV Test</text>' % INK +
             '<g class="t v2"><rect x="380" y="124" width="146" height="5" rx="3" fill="#E3F2EA"/><rect class="progress" x="380" y="124" width="146" height="5" rx="3" fill="#127A4F"/>'
             '<rect x="380" y="146" width="140" height="8" rx="4" fill="%s"/><rect x="380" y="162" width="104" height="8" rx="4" fill="%s"/>' % (INK, INK) +
             q(190) + q(224, True, "pick") + q(258) + q(292) + '</g>'
             '<g class="t v3"><text x="453" y="140" text-anchor="middle" font-size="12" font-weight="600" fill="#86868B">YOUR SCORE</text>'
             '<circle cx="453" cy="196" r="40" fill="none" stroke="#E3F2EA" stroke-width="10"/><circle class="ring" cx="453" cy="196" r="40" fill="none" stroke="#127A4F" stroke-width="10" stroke-linecap="round" stroke-dasharray="251" stroke-dashoffset="251" transform="rotate(-90 453 196)"/>'
             '<text x="453" y="205" text-anchor="middle" font-size="28" font-weight="700" fill="%s">78</text>' % INK + bars +
             '<text x="453" y="366" text-anchor="middle" font-size="12" font-weight="600" fill="#86868B">10 AREAS · 2 PDFs</text></g></g>')
    inner = (FLOOR +
             '<g class="t v1 v4">' + desk(360, 330, 220) + interviewer(470, 330) + '</g>' +
             bubble(300, 40, 280, 54, "So, what are your strengths?", "right", "t v1", tailx=462) +
             bubble(300, 40, 280, 54, "Tell me about a conflict…", "right", "t v4", tailx=462) +
             chair(190, 396) + riya(190, 370, 1.05, faces={"w": "v1", "n": "v2", "h": "v3 v4"}, arms={"down": "v1", "phone": "v2 v3", "talk": "v4"}, sweat="v1", bulb="v3") +
             thought(60, 60, 150, 58, '<text x="135" y="98" text-anchor="middle" font-size="26" font-weight="700" fill="#C7C7CC">? ? ?</text>', "t v1", hx=160, hy=150) +
             bubble(30, 36, 250, 92, "I talk to them|privately first.|Then we fix it.", "right", "t v4", "#E3F2EA", 16, "#0B4F33", tailx=182) +
             '<g class="t v4 badge"><circle cx="540" cy="232" r="22" fill="#127A4F"/><path d="M530,232 l7,7 l13,-14" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>' +
             phone)
    return scene(inner, "Riya at an interview, then taking HV Test on her phone, seeing her score, and answering with confidence")

def ch_reset():
    def blk(i, y, w, label, fill, txt="#FFFFFF"):
        return ('<g class="blk" style="--d:%.2fs"><rect x="352" y="%g" width="%g" height="40" rx="10" fill="%s"/><text x="366" y="%g" font-size="14" font-weight="600" fill="%s">%s</text>'
                '<g class="t v4 tick"><circle cx="%g" cy="%g" r="11" fill="#FFFFFF"/><path d="M%g,%g l4,4 l8,-9" fill="none" stroke="#127A4F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g></g>') % (
            i * .12, y, w, fill, y + 25, txt, label, 352 + w - 20, y + 20, 352 + w - 25, y + 20)
    notifs = "".join('<g class="notif" style="animation-delay:%.1fs"><rect x="%d" y="%d" width="118" height="34" rx="12" fill="#FFFFFF" stroke="#E5E5EA"/><circle cx="%d" cy="%d" r="8" fill="%s"/><rect x="%d" y="%d" width="70" height="6" rx="3" fill="#D8DAE0"/></g>' % (
        d, x, y, x + 18, y + 17, c, x + 32, y + 14) for d, x, y, c in [(0, 372, 150, "#FF6B6B"), (.5, 440, 214, "#4A72C8"), (1, 380, 278, "#F4B942")])
    inner = ('<g><rect x="48" y="46" width="148" height="104" rx="14" fill="#9CC3F0"/><g class="t v1"><rect class="skycycle" x="48" y="46" width="148" height="104" rx="14" fill="#1F2A55"/></g>'
             '<rect class="t v4" x="48" y="46" width="148" height="104" rx="14" fill="#F4A774"/><circle class="t v4" cx="122" cy="116" r="18" fill="#FFD27A"/></g>'
             '<g transform="translate(262 96)"><circle r="38" fill="#FFFFFF" stroke="%s" stroke-width="4"/><path class="hand hour" d="M0,0 V-20" stroke="%s" stroke-width="5" stroke-linecap="round"/><path class="hand minute" d="M0,0 V-30" stroke="#4A72C8" stroke-width="4" stroke-linecap="round"/><circle r="4" fill="%s"/></g>' % (INK, INK, INK) +
             FLOOR + riya(180, 356, 1, faces={"t": "v1", "n": "v2 v3", "h": "v4"}, arms={"desk": "v1 v2 v3", "tea": "v4"}) + desk(40, 348, 290) +
             '<g class="t v1"><rect x="236" y="318" width="20" height="30" rx="5" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/><rect x="262" y="322" width="20" height="26" rx="5" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/><rect x="288" y="316" width="20" height="32" rx="5" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/></g>'
             '<g class="t v1">' + notifs + '<g transform="rotate(4 470 90)"><rect x="420" y="40" width="112" height="96" rx="8" fill="#FFF8E1" stroke="#EADCB0"/>' +
             "".join('<rect x="434" y="%d" width="12" height="12" rx="3" fill="#FFFFFF" stroke="#C9B98A"/><rect class="wiggle" x="454" y="%d" width="62" height="6" rx="3" fill="#C9B98A"/>' % (58 + i * 20, 61 + i * 20) for i in range(4)) + '</g></g>'
             '<g class="t v2 v3 v4 panel"><rect x="336" y="56" width="236" height="330" rx="22" fill="#FFFFFF" stroke="#E5E5EA" stroke-width="1.5"/>' + logo_at("reset", 352, 72, 26) +
             '<text x="386" y="91" font-size="14" font-weight="700" fill="%s">HV Reset</text><text x="352" y="134" font-size="36" font-weight="300" fill="%s" class="mono">01:14:52</text>' % (INK, INK) +
             '<g class="shift">' + blk(0, 156, 204, "Send applications", "#4A72C8") + blk(1, 204, 204, "Short break", "#EEF0F4", "#6E6E73") + blk(2, 252, 204, "Lunch", "#F4B942", INK) + blk(3, 300, 204, "Outreach", "#4A72C8") + '</g>'
             '<g class="t v3 late"><rect x="478" y="72" width="80" height="26" rx="13" fill="#FBF1DF"/><text x="518" y="90" text-anchor="middle" font-size="13" font-weight="700" fill="#9A6512">+30 min</text></g></g>')
    return scene(inner, "Riya's chaotic day, then HV Reset turning it into calm blocks that shift when she is late, all ticked by sunset")

def ch_vault():
    notes = "".join('<g class="drift" style="animation-delay:%.1fs"><rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" transform="rotate(%d %d %d)"/>%s</g>' % (
        d, x, y, w, h, c, r, x + w / 2, y + h / 2, extra) for d, x, y, w, h, c, r, extra in [
        (0, 330, 70, 84, 70, "#FFE58A", -6, ""), (.6, 440, 110, 84, 70, "#FFD1DC", 5, ""),
        (1.1, 360, 190, 120, 40, "#FFFFFF", -3, '<text x="372" y="215" font-size="13" font-weight="600" fill="#86868B">resume_final_v3.pdf</text>'),
        (.3, 340, 256, 96, 40, "#FFFFFF", 4, '<text x="352" y="281" font-size="13" font-weight="600" fill="#4A72C8">bit.ly/job…</text>')])
    card = lambda x, y, t, sub, hot=False, cls="", d=0: ('<g class="t %s fly" style="--d:%.2fs"><rect x="%g" y="%g" width="68" height="44" rx="8" fill="%s"/><rect x="%g" y="%g" width="46" height="6" rx="3" fill="%s"/><text x="%g" y="%g" font-size="10" font-weight="600" fill="#86868B">%s</text></g>') % (
        cls, d, x, y, "#F6EEDC" if hot else "#F5F5F7", x + 8, y + 10, INK, x + 8, y + 34, sub)
    confetti = "".join('<rect class="conf" style="animation-delay:%.2fs" x="%d" y="-30" width="8" height="12" rx="2" fill="%s" transform="rotate(%d %d 0)"/>' % (
        i * .13, 330 + (i * 37) % 240, c, (i * 47) % 90, 330 + (i * 37) % 240) for i, c in enumerate(["#F4B942", "#4A72C8", "#127A4F", "#FF6B6B", "#A87A22", "#8FA6FF"] * 3))
    inner = (FLOOR +
             '<g class="t v1">' + notes + '<g class="balloon"><path d="M522,300 C520,330 530,350 520,380" fill="none" stroke="#9AA0AE" stroke-width="2"/><ellipse cx="522" cy="276" rx="34" ry="40" fill="#FF8A8A"/><path d="M516,314 h12 l-6,8Z" fill="#FF8A8A"/><text x="522" y="281" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">OFFER?</text></g></g>' +
             chair(170, 393) + riya(170, 366, 1.05, faces={"w": "v1", "n": "v2", "h": "v3 v4"}, arms={"reach": "v1", "down": "v2 v3", "up": "v4"}) +
             '<g class="t v2 v3 v4 panel"><rect x="318" y="52" width="258" height="244" rx="20" fill="#FFFFFF" stroke="#E5E5EA" stroke-width="1.5"/>' + logo_at("vault", 332, 66, 24) +
             '<text x="364" y="84" font-size="14" font-weight="700" fill="%s">HV Vault</text>' % INK +
             "".join('<text x="%d" y="116" font-size="10" font-weight="700" fill="#86868B" letter-spacing="1">%s</text>' % (x, t) for x, t in [(334, "SAVED"), (416, "APPLIED"), (498, "INTERVIEW")]) +
             card(332, 126, "", "Razorpay", False, "v2 v3 v4", 0) + card(332, 178, "", "Meesho", False, "v2 v3 v4", .15) +
             card(414, 126, "", "Cred", True, "v2 v3 v4", .3) + card(496, 126, "", "Zomato", False, "v2 v3 v4", .45) + card(496, 178, "", "Tue 4 PM", False, "v3 v4", .1) + '</g>' +
             '<g class="t v3"><g class="ring-bell"><circle cx="560" cy="44" r="20" fill="#F6EEDC"/><path d="M551,50 c0,-12 3,-17 9,-17 s9,5 9,17Z" fill="none" stroke="#A87A22" stroke-width="2.6" stroke-linejoin="round"/><circle cx="560" cy="54" r="2.4" fill="#A87A22"/></g>'
             '<rect x="318" y="312" width="258" height="40" rx="14" fill="%s"/><text x="334" y="337" font-size="13.5" font-weight="600" fill="#FFFFFF">Kal 4 baje Zomato interview</text>' % "#2E43A6" +
             '<rect x="318" y="360" width="200" height="40" rx="14" fill="#FFFFFF" stroke="#E5E5EA"/><text x="334" y="385" font-size="13.5" font-weight="600" fill="%s">📅 Tue · 4:00 PM ✓</text></g>' % INK +
             '<g class="t v4"><g class="envelope"><rect x="360" y="316" width="150" height="92" rx="10" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/><path d="M360,322 l75,50 l75,-50" fill="none" stroke="#D2D2D7" stroke-width="2"/>'
             '<rect class="letter" x="378" y="300" width="114" height="60" rx="6" fill="#F6EEDC"/><text class="letter" x="435" y="336" text-anchor="middle" font-size="16" font-weight="800" fill="#A87A22">OFFER</text></g>' + confetti + '</g>')
    return scene(inner, "Riya's scattered notes and a floating opportunity, then HV Vault organising everything, a follow-up reminder, and an offer letter")

def finale():
    inner = ('<rect width="600" height="460" rx="28" fill="#F5F6FA"/>' +
             '<path class="loop" d="M125,350 C125,428 475,428 475,350" fill="none" stroke="#E3A23B" stroke-width="3" stroke-dasharray="4 10" stroke-linecap="round"/>'
             '<path d="M117,362 L125,346 L133,362" fill="none" stroke="#E3A23B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
             '<text x="300" y="446" text-anchor="middle" font-size="16" font-weight="700" fill="#9A6512">↻ Grow, and go again</text>' +
             "".join('<g class="link" style="animation-delay:%.1fs"><rect x="%d" y="232" width="70" height="26" rx="13" fill="none" stroke="%s" stroke-width="6"/><rect x="%d" y="232" width="70" height="26" rx="13" fill="none" stroke="%s" stroke-width="6"/></g>' % (
                 d, x, c1, x + 44, c2) for d, x, c1, c2 in [(.2, 172, "#127A4F", "#4A72C8"), (.5, 342, "#4A72C8", "#A87A22")]) +
             logo_at("test", 70, 190, 110) + logo_at("reset", 245, 190, 110) + logo_at("vault", 420, 190, 110) +
             "".join('<text x="%d" y="332" text-anchor="middle" font-size="18" font-weight="700" fill="%s">%s</text>' % (x, INK, t) for x, t in [(125, "Know"), (300, "Plan"), (475, "Act")]) +
             riya(300, 150, .62, faces={"h": ""}, arms={"up": ""}))
    return '<svg class="art" viewBox="0 0 600 460" role="img" aria-label="HV Test, HV Reset and HV Vault linked as a chain, looping back to grow, with Riya cheering">%s</svg>' % inner

# ---------------------------------------------------------------- chapters (scrollytelling)
def chapter(key, num, verb, prod, title, art, steps, url, cta):
    st = "".join('<div class="step" data-step="%d"><div class="cap"><p class="k">%s</p><h3>%s</h3><p>%s</p>%s</div></div>' % (
        i + 1, k, h, p, ('<a class="btn" href="%s">%s</a>' % (url, cta)) if i == len(steps) - 1 else "") for i, (k, h, p) in enumerate(steps))
    return ('<section class="chapter" id="%s"><div class="wrap"><div class="chead rv"><span class="num">Chapter %d · %s</span>'
            '<div class="pname">%s<span>%s</span></div><h2>%s</h2></div>'
            '<div class="scrolly"><div class="stage-wrap"><div class="stage" data-step="1">%s</div></div><div class="steps">%s</div></div></div></section>') % (
        key, num, verb, logo(key, size=40), prod, title, art, st)

CH = [
    chapter("test", 1, "Know", "HV Test", "Who am I, really?", ch_test(), [
        ("The problem", "Riya freezes.", "&ldquo;What are your strengths?&rdquo; She has worked hard for years, but she has never really measured herself."),
        ("HV Test", "So she takes a test.", "Real-life situations, four honest options, no right answers to game. About 10 minutes."),
        ("The result", "Now she can see herself.", "A score out of 100 across 10 areas, a full report and a 30-day plan."),
        ("The change", "Next interview, she's ready.", "She knows her strengths, and she has real stories to prove them.")], "https://harshvittori.github.io/hv-tests/", "Open HV Test"),
    chapter("reset", 2, "Plan", "HV Reset", "Where did my day go?", ch_reset(), [
        ("The problem", "Every day slips away.", "Notifications, coffee, a to-do list that never shrinks. The clock just spins."),
        ("HV Reset", "Her day becomes blocks.", "One block, one task, with a calm focus clock that shows what to do right now."),
        ("Running late?", "The day bends. It doesn't break.", "One tap shifts the rest of the plan. Lunch stays. Nothing is lost."),
        ("The change", "Evening, and it's all done.", "Every block ticked. Tea, and tomorrow's first step already written.")], "https://harshvittori.github.io/harsh-reset/", "Open HV Reset"),
    chapter("vault", 3, "Act", "HV Vault", "Did I ever follow up?", ch_vault(), [
        ("The problem", "Opportunities float away.", "Links in chats, five versions of her resume, sticky notes. The good ones go quiet."),
        ("HV Vault", "Everything, in one place.", "Every job and company on one board: saved, applied, interview."),
        ("HV AI", "Nothing slips anymore.", "Follow-ups remind her on time. She just says &ldquo;Kal 4 baje interview&rdquo; and it's on the calendar."),
        ("The change", "And then, the offer.", "Not luck. A system that kept every opportunity alive.")], "https://harshvittori.github.io/hv-vault-web/", "Open HV Vault"),
]

TOGGLE_CSS = "".join('.stage[data-step="%d"] .v%d{opacity:1;translate:0 0}\n.stage[data-step="%d"] .v%d,.stage[data-step="%d"] .v%d *{animation-play-state:running}\n' % (n, n, n, n, n, n) for n in range(1, 5))

CSS = r"""
:root{--ink:#1D1D1F;--soft:#6E6E73;--faint:#86868B;--line:#D2D2D7;--gray:#F5F5F7;--accent:#2E43A6;--accent-hover:#1D2B72;
  --test:#127A4F;--reset:#4A72C8;--vault:#A87A22;--font:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue",Helvetica,Arial,sans-serif;color-scheme:light}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:#FFFFFF;color:var(--ink);font:17px/1.47 var(--font);letter-spacing:-.022em;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
h1,h2,h3,p{margin:0}
.wrap{width:min(1120px,100% - 40px);margin:0 auto}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 22px;border-radius:980px;background:var(--accent);color:#fff;font-size:16px;font-weight:500;margin-top:20px}
.btn:hover{background:var(--accent-hover);text-decoration:none}
.btn.ghost{background:#fff;color:var(--ink);box-shadow:inset 0 0 0 1px var(--line)}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:10px}
.skip{position:absolute;left:-999px;top:8px;z-index:50;background:var(--ink);color:#fff;padding:10px 16px;border-radius:8px}.skip:focus{left:16px}
header{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.82);-webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid rgba(0,0,0,.07)}
.nav{display:flex;align-items:center;height:52px;gap:22px;font-size:14px}
.brand{display:flex;align-items:center;gap:9px;color:var(--ink);font-weight:600;font-size:16px}.brand:hover{text-decoration:none}
.brand svg{width:26px;height:26px;border-radius:7px}
.nav nav{display:flex;gap:22px;margin-left:auto}.nav nav a{color:var(--ink);opacity:.78}.nav nav a:hover{opacity:1;text-decoration:none}
.nav nav a.all{color:var(--accent);opacity:1;font-weight:600}
.pacts{display:flex;align-items:center;flex-wrap:wrap;gap:8px 18px;margin-top:18px}.pacts .btn{margin:0}.pcard .lm{color:var(--accent);font-weight:500;font-size:15px}
.more{margin-top:32px;font-size:17px}.more a{color:var(--accent);font-weight:600;text-decoration:none}.more a:hover{text-decoration:underline}
@media (max-width:600px){.nav nav a.opt{display:none}.nav nav{gap:16px}}

/* hero */
.hero{display:grid;grid-template-columns:.9fr 1.1fr;gap:48px;align-items:center;padding:72px 0 84px}
.hero .eyebrow{font-size:15px;font-weight:600;color:var(--soft)}
.hero h1{font-size:clamp(46px,7vw,84px);font-weight:700;letter-spacing:-.045em;line-height:1.02;margin:12px 0 18px}
.hero .lead{font-size:clamp(19px,2.2vw,24px);color:var(--soft);line-height:1.35}
.hero .lead b{color:var(--ink);font-weight:600}
.worries{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.worries span{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:980px;background:var(--gray);font-size:15px;font-weight:500}
.worries i{width:10px;height:10px;border-radius:50%;display:inline-block}
.scroll-hint{display:inline-flex;align-items:center;gap:8px;margin-top:28px;font-size:17px}
.scroll-hint svg{width:18px;height:18px}
@media (prefers-reduced-motion:no-preference){.scroll-hint svg{animation:bob 1.8s ease-in-out infinite}}
@media (max-width:880px){.hero{grid-template-columns:1fr;gap:28px;padding:40px 0 56px}.hero .art-box{order:-1}}
.art-box{border-radius:28px;overflow:hidden;box-shadow:0 30px 60px -36px rgba(20,30,60,.4)}
.art{display:block;width:100%;height:auto;overflow:hidden;border-radius:28px}

/* chapters */
.chapter{padding:96px 0 40px;border-top:1px solid #EEF0F4}
.chead{text-align:center;max-width:720px;margin:0 auto 24px}
.num{font-size:14px;font-weight:600;color:var(--soft);letter-spacing:0}
.pname{display:flex;align-items:center;justify-content:center;gap:10px;margin:14px 0 8px;font-size:20px;font-weight:600}
.pname svg{border-radius:11px}
.chead h2{font-size:clamp(36px,5.6vw,64px);font-weight:700;letter-spacing:-.04em;line-height:1.05}
#test .num{color:var(--test)}#reset .num{color:var(--reset)}#vault .num{color:var(--vault)}
.scrolly{display:grid;grid-template-columns:1.15fr .85fr;gap:56px;position:relative}
.stage-wrap{position:sticky;top:calc(52px + 7vh);height:min(76vh,560px);display:flex;align-items:center}
.stage{width:100%;border-radius:28px;overflow:hidden;box-shadow:0 30px 60px -36px rgba(20,30,60,.4)}
.steps{padding:6vh 0 18vh}
.step{min-height:78vh;display:flex;align-items:center}
.cap{max-width:420px;opacity:.28;transition:opacity .45s ease}
.step.on .cap{opacity:1}
.cap .k{font-size:14px;font-weight:600;color:var(--soft);margin-bottom:8px}
#test .step.on .k{color:var(--test)}#reset .step.on .k{color:var(--reset)}#vault .step.on .k{color:var(--vault)}
.cap h3{font-size:clamp(28px,3.4vw,40px);font-weight:700;letter-spacing:-.035em;line-height:1.08}
.cap p:not(.k){font-size:19px;color:var(--soft);margin-top:12px;line-height:1.4}
@media (max-width:880px){
  .chapter{padding:64px 0 10px}
  .scrolly{display:block}
  .stage-wrap{top:56px;height:auto;z-index:3;padding:6px 0 0;background:linear-gradient(#fff 85%,rgba(255,255,255,0))}
  .stage{box-shadow:0 18px 40px -30px rgba(20,30,60,.5)}
  .steps{position:relative;z-index:1;padding:4vh 0 12vh}
  .step{min-height:80vh;align-items:flex-end;padding-bottom:4vh}
  .cap{opacity:1;background:rgba(255,255,255,.96);border:1px solid #EEF0F4;border-radius:20px;padding:18px 20px;box-shadow:0 18px 40px -24px rgba(20,30,60,.35);max-width:none;width:100%}
  .cap h3{font-size:24px}.cap p:not(.k){font-size:16px;margin-top:6px}
}

/* scene toggles and animation */
.art .t{opacity:0;translate:0 10px;transition:opacity .55s ease,translate .7s cubic-bezier(.2,.8,.2,1)}
.art .t,.art .t *{animation-play-state:paused}
__TOGGLES__
.sweat{animation:drip 1.3s ease-in infinite}
.glow{transform-box:fill-box;transform-origin:center;animation:glow 1.6s ease-in-out infinite}
.progress{transform-box:fill-box;transform-origin:left;animation:fill 2.4s ease-in-out infinite}
.pick rect,.pick circle{animation:pick 2.4s ease-in-out infinite}
.ring{transition:stroke-dashoffset 1.4s cubic-bezier(.2,.8,.2,1) .2s}
.stage[data-step="3"] .ring{stroke-dashoffset:55}
.bar{transform-box:fill-box;transform-origin:bottom;transform:scaleY(.05);transition:transform .9s cubic-bezier(.2,.8,.2,1)}
.stage[data-step="3"] .bar{transform:scaleY(1)}
.badge{transform-box:fill-box;transform-origin:center}
.stage[data-step="4"] .badge{animation:popin .6s cubic-bezier(.2,1.6,.4,1) both;animation-play-state:running}
.hand{transform-box:view-box;transform-origin:0 0}
.hand.minute{animation:spin 4s linear infinite}.hand.hour{animation:spin 48s linear infinite}
.stage[data-step="1"] .hand.minute{animation-duration:.6s;animation-play-state:running}.stage[data-step="1"] .hand.hour{animation-duration:3.6s;animation-play-state:running}
.stage:not([data-step="1"]) .hand{animation-play-state:running}
.skycycle{animation:sky 3s ease-in-out infinite}
.notif{animation:notif 1.5s ease-in-out infinite}
.wiggle{transform-box:fill-box;transform-origin:left;animation:wig 1.2s ease-in-out infinite}
.blk{transform-box:fill-box}
.stage[data-step="2"] .blk,.stage[data-step="3"] .blk,.stage[data-step="4"] .blk{animation:slidein .7s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d);animation-play-state:running}
.shift{transition:translate .8s cubic-bezier(.2,.8,.2,1)}
.stage[data-step="3"] .shift{translate:0 22px}
.tick{transform-box:fill-box;transform-origin:center}
.stage[data-step="4"] .tick{animation:popin .5s cubic-bezier(.2,1.6,.4,1) both;animation-play-state:running}
.stage[data-step="4"] .blk:nth-child(2) .tick{animation-delay:.15s}.stage[data-step="4"] .blk:nth-child(3) .tick{animation-delay:.3s}.stage[data-step="4"] .blk:nth-child(4) .tick{animation-delay:.45s}
.steam{animation:steam 2.2s ease-in-out infinite}
.drift{animation:drift 3.4s ease-in-out infinite}
.balloon{animation:float 4s ease-in-out infinite}
.fly{transform-box:fill-box}
.stage[data-step="2"] .fly{animation:fly .8s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d);animation-play-state:running}
.ring-bell{transform-box:fill-box;transform-origin:50% 20%;animation:bell 1s ease-in-out infinite}
.envelope .letter{animation:letter 1.6s cubic-bezier(.2,.8,.2,1) both}
.conf{animation:conf 2.6s linear infinite}
.pop{transform-box:fill-box;transform-origin:center;animation:pop 3.6s ease-in-out infinite}
.twinkle{animation:twinkle 2.4s ease-in-out infinite}
.glowlap{animation:lap 3s ease-in-out infinite}
.link{animation:linkin 1s cubic-bezier(.2,1.4,.4,1) both}
.loop{animation:dash 3s linear infinite}
@keyframes drip{0%{transform:translateY(0);opacity:1}80%{opacity:1}100%{transform:translateY(22px);opacity:0}}
@keyframes glow{50%{transform:scale(1.25);opacity:.9}}
@keyframes fill{0%{transform:scaleX(.15)}70%,100%{transform:scaleX(.7)}}
@keyframes pick{0%,35%{opacity:.35}50%,100%{opacity:1}}
@keyframes popin{from{transform:scale(0)}to{transform:scale(1)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes sky{0%,100%{opacity:0}50%{opacity:1}}
@keyframes notif{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes wig{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.7)}}
@keyframes slidein{from{transform:translateX(40px);opacity:0}to{transform:none;opacity:1}}
@keyframes steam{0%,100%{opacity:.2;transform:translateY(2px)}50%{opacity:1;transform:translateY(-3px)}}
@keyframes drift{0%,100%{transform:translate(0,0) rotate(0)}50%{transform:translate(6px,-8px) rotate(2deg)}}
@keyframes float{0%{transform:translateY(0)}50%{transform:translateY(-30px)}100%{transform:translateY(0)}}
@keyframes fly{from{transform:translate(-160px,40px) rotate(-8deg);opacity:0}to{transform:none;opacity:1}}
@keyframes bell{0%,100%{transform:rotate(0)}20%{transform:rotate(14deg)}40%{transform:rotate(-12deg)}60%{transform:rotate(8deg)}80%{transform:rotate(-4deg)}}
@keyframes letter{from{transform:translateY(40px)}to{transform:translateY(-6px)}}
@keyframes conf{from{transform:translateY(0) rotate(0);opacity:1}to{transform:translateY(470px) rotate(360deg);opacity:.2}}
@keyframes pop{0%,15%{transform:scale(0)}25%,85%{transform:scale(1)}100%{transform:scale(0)}}
@keyframes twinkle{50%{opacity:.2}}
@keyframes lap{50%{opacity:.25}}
@keyframes linkin{from{transform:scale(.4);opacity:0}to{transform:none;opacity:1}}
@keyframes dash{to{stroke-dashoffset:-56}}
@keyframes bob{50%{transform:translateY(4px)}}
.art .link,.art .pop{transform-box:fill-box;transform-origin:center}
@media (prefers-reduced-motion:reduce){.art *,.art .t{animation:none!important;transition:none!important}.art .ring{stroke-dashoffset:55}.art .bar{transform:none}}

/* finale + people + builder */
.finale{padding:110px 0;text-align:center;background:var(--gray)}
.finale h2{font-size:clamp(40px,6.4vw,76px);font-weight:700;letter-spacing:-.045em;line-height:1.02}
.finale .sub{font-size:clamp(19px,2.2vw,24px);color:var(--soft);margin-top:12px}
.finale .art-box{max-width:720px;margin:48px auto 0;box-shadow:none}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:56px auto 0;max-width:960px;text-align:left}
.pcard{background:#fff;border:1px solid #E4E5EA;border-radius:22px;padding:26px;display:flex;flex-direction:column}
.pcard .h{display:flex;align-items:center;gap:12px}.pcard .h svg{border-radius:12px}
.pcard b{font-size:21px;font-weight:600;letter-spacing:-.02em}
.pcard p{color:var(--soft);margin-top:10px;flex:1}
.pcard .btn{align-self:flex-start}
@media (max-width:820px){.cards{grid-template-columns:1fr}}
.people{padding:100px 0;text-align:center}
.people h2{font-size:clamp(32px,4.6vw,52px);font-weight:700;letter-spacing:-.035em;line-height:1.08}
.people .sub{font-size:20px;color:var(--soft);margin-top:10px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:900px;margin:44px auto 0;text-align:left}
.tile{background:var(--gray);border-radius:18px;padding:22px}
.tile b{font-size:18px;font-weight:600}.tile span{display:block;color:var(--soft);font-size:15px;margin-top:4px}
@media (max-width:760px){.tiles{grid-template-columns:1fr 1fr}}@media (max-width:460px){.tiles{grid-template-columns:1fr}}
.builder{padding:90px 0;text-align:center;background:var(--gray)}
.builder p{font-size:17px;color:var(--soft);font-weight:600}
.builder h2{font-size:clamp(32px,5vw,56px);font-weight:700;letter-spacing:-.04em;margin-top:6px}
.builder a.more{display:inline-block;margin-top:14px;font-size:19px}.builder a.more::after{content:" ›"}
footer{background:var(--gray);border-top:1px solid var(--line);color:var(--faint);font-size:12px;padding:18px 0 28px}
footer .row{display:flex;flex-wrap:wrap;gap:10px 20px;justify-content:space-between}
footer nav{display:flex;flex-wrap:wrap;gap:6px 18px}footer a{color:var(--soft)}
@media (prefers-reduced-motion:no-preference){.rv{opacity:0;transform:translateY(24px);transition:opacity .9s cubic-bezier(.2,.8,.2,1),transform .9s cubic-bezier(.2,.8,.2,1)}.rv.in{opacity:1;transform:none}}
""".replace("__TOGGLES__", TOGGLE_CSS)

JS = r"""
(function () {
  document.getElementById("yr").textContent = new Date().getFullYear();
  // scrollytelling: the step crossing the middle of the screen drives its chapter's scene
  document.querySelectorAll(".scrolly").forEach(function (sc) {
    var stage = sc.querySelector(".stage"), steps = sc.querySelectorAll(".step");
    if (!("IntersectionObserver" in window)) { stage.setAttribute("data-step", "4"); steps.forEach(function (s) { s.classList.add("on"); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        steps.forEach(function (s) { s.classList.toggle("on", s === e.target); });
        stage.setAttribute("data-step", e.target.getAttribute("data-step"));
      });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
    steps.forEach(function (s) { io.observe(s); });
    steps[0].classList.add("on");
  });
  var els = document.querySelectorAll(".rv");
  if (!("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("in"); }); return; }
  var io2 = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io2.unobserve(e.target); } }); }, { rootMargin: "0px 0px -6% 0px", threshold: .05 });
  els.forEach(function (e) { io2.observe(e); });
})();
"""

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>HV World | Riya's story: Know. Plan. Act.</title>
<meta name="description" content="Follow Riya through the three problems that hold people back, and see how HV Test, HV Reset and HV Vault fix each one. HV World, designed and built by Harsh Vittori.">
<link rel="canonical" href="https://harshvittori.github.io/story/">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="website"><meta property="og:site_name" content="HV World">
<meta property="og:title" content="HV World: Riya's story. Know. Plan. Act.">
<meta property="og:description" content="Three problems hold people back. Three products fix them. Designed and built by Harsh Vittori.">
<meta property="og:url" content="https://harshvittori.github.io/story/"><meta property="og:image" content="https://harshvittori.github.io/story/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"HV World","url":"https://harshvittori.github.io/","founder":{"@type":"Person","name":"Harsh Vittori","sameAs":["https://www.linkedin.com/in/harshvittori"]}}</script>
<style>__CSS__</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="wrap nav"><a class="brand" href="#top">__LOGO_NAV__HV World</a>
<nav aria-label="Main"><a href="#test">Know</a><a href="#reset">Plan</a><a href="#vault">Act</a><a class="opt" href="#products">Products</a><a class="all" href="/">All features</a></nav></div></header>
<main id="main">
  <section id="top"><div class="wrap hero">
    <div class="rv">
      <p class="eyebrow">HV World · a story in three products</p>
      <h1>This is Riya.</h1>
      <p class="lead">She works hard. She applies everywhere. <b>So why does she feel stuck?</b></p>
      <div class="worries"><span><i style="background:#127A4F"></i>Who am I, really?</span><span><i style="background:#4A72C8"></i>Where did my day go?</span><span><i style="background:#A87A22"></i>Did I follow up?</span></div>
      <a class="scroll-hint" href="#test">Follow her story __ARROW__</a>
    </div>
    <div class="art-box rv">__PROLOGUE__</div>
  </div></section>
  __CHAPTERS__
  <section class="finale" id="products"><div class="wrap">
    <h2 class="rv">Know. Plan. Act.</h2>
    <p class="sub rv">Three problems. Three products. One chain that keeps Riya growing.</p>
    <div class="art-box rv">__FINALE__</div>
    <div class="cards">
      <div class="pcard rv"><div class="h">__L_TEST__<b>HV Test</b></div><p>Know yourself. Real-life scenarios, a score, a report and a 30-day plan.</p><div class="pacts"><a class="btn" href="https://harshvittori.github.io/hv-tests/">Open HV Test</a><a class="lm" href="/test/">Learn more</a></div></div>
      <div class="pcard rv"><div class="h">__L_RESET__<b>HV Reset</b></div><p>Plan your day. One block, one task, and a day that bends instead of breaking.</p><div class="pacts"><a class="btn" href="https://harshvittori.github.io/harsh-reset/">Open HV Reset</a><a class="lm" href="/reset/">Learn more</a></div></div>
      <div class="pcard rv"><div class="h">__L_VAULT__<b>HV Vault</b></div><p>Act on every opportunity. One board, automatic follow-ups and HV AI.</p><div class="pacts"><a class="btn" href="https://harshvittori.github.io/hv-vault-web/">Open HV Vault</a><a class="lm" href="/vault/">Learn more</a></div></div>
    </div>
    <p class="more rv"><a href="/">See every feature, HV AI, privacy and FAQ →</a></p>
  </div></section>
  <section class="people"><div class="wrap">
    <h2 class="rv">Riya could be anyone.</h2>
    <p class="sub rv">The same three problems, in every walk of life.</p>
    <div class="tiles rv">
      <div class="tile"><b>Students</b><span>Internships, study days, placements.</span></div>
      <div class="tile"><b>Job seekers</b><span>A real system for the search.</span></div>
      <div class="tile"><b>Professionals</b><span>Deep work, and the next move.</span></div>
      <div class="tile"><b>Freelancers</b><span>Warm leads, balanced days.</span></div>
      <div class="tile"><b>Career switchers</b><span>A new field, with a plan.</span></div>
      <div class="tile"><b>Mentors</b><span>A clear structure to share.</span></div>
    </div>
  </div></section>
  <section class="builder"><div class="wrap rv"><p>Designed and built by</p><h2>Harsh Vittori</h2><a class="more" href="https://www.linkedin.com/in/harshvittori" target="_blank" rel="noopener">Connect on LinkedIn</a></div></section>
</main>
<footer><div class="wrap row"><span>© <span id="yr">2026</span> Harsh Vittori · HV World</span>
<nav aria-label="Footer"><a href="/">All features</a><a href="/test/">About HV Test</a><a href="/reset/">About HV Reset</a><a href="/vault/">About HV Vault</a><a href="https://harshvittori.github.io/hv-tests/">HV Test</a><a href="https://harshvittori.github.io/harsh-reset/">HV Reset</a><a href="https://harshvittori.github.io/hv-vault-web/">HV Vault</a><a href="https://www.linkedin.com/in/harshvittori" target="_blank" rel="noopener">LinkedIn</a><a href="https://github.com/harshvittori" target="_blank" rel="noopener">GitHub</a></nav></div></footer>
<script>__JS__</script>
</body>
</html>
"""

def build():
    html = (PAGE.replace("__CSS__", CSS).replace("__JS__", JS).replace("__ARROW__", ARROW)
            .replace("__LOGO_NAV__", logo("world")).replace("__PROLOGUE__", prologue()).replace("__CHAPTERS__", "\n".join(CH))
            .replace("__FINALE__", finale()).replace("__L_TEST__", logo("test", size=44)).replace("__L_RESET__", logo("reset", size=44)).replace("__L_VAULT__", logo("vault", size=44)))
    assert "__" not in re.sub(r"<script>.*?</script>", "", html, flags=re.S).replace("__proto__", ""), "unfilled placeholder"
    os.makedirs(os.path.join(OUT, "story"), exist_ok=True)
    open(os.path.join(OUT, "story", "index.html"), "w").write(html)
    open(os.path.join(OUT, "favicon.svg"), "w").write(read("world.svg") + "\n")
    print("ok", len(html), "bytes")

if __name__ == "__main__":
    build()
