"""HV World: "Riya's story". Builds index.html (and favicon.svg) from this file and the logos in src/.

Run from the repo root:  python3 src/story.py
Every picture is hand-drawn inline SVG. Scroll steps switch a scene's data-step (1-4) and CSS shows,
hides and animates the parts marked v1..v4. No libraries."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import transitions
import people

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

# Links into the apps (HV Test, HV Reset, HV Vault) open in a new tab, so HV World stays open behind them.
def app_links_new_tab(html):
    return re.sub(r'<a\b([^>]*\bhref="https://harshvittori\.github\.io/(?:hv-reset|hv-vault-web|hv-tests)/[^"]*"[^>]*)>',
                  lambda m: m.group(0) if "target=" in m.group(1) else '<a' + m.group(1) + ' target="_blank" rel="noopener">', html)

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
SKIN, SHADE, HAIR, SHINE, INK = "#D9A07A", "#BF8460", "#231715", "#4A3430", "#1D1D1F"
BLAZER, LAPEL, TEE, LIP, CHEEK, GOLD = "#2F3B6E", "#44528F", "#F6EFE6", "#B4545E", "#E8826F", "#E3AE45"
TOP = BLAZER

def riya(x, y, s=1.0, faces=None, arms=None, cls="", sweat=None, bulb=None):
    """Riya, 25: long hair, blazer over a tee, small gold earrings. Upper body, head centred at (0,-94).
    faces/arms map a variant to the step classes where it shows (e.g. {'w': 'v1'})."""
    faces = faces or {"n": ""}
    arms = arms or {"down": ""}
    p = []
    # hair behind the shoulders
    p.append('<path d="M-35,-112 C-48,-158 48,-158 35,-112 C42,-92 46,-64 44,-40 C46,-30 40,-24 34,-26 C20,-30 -20,-30 -34,-26 C-40,-24 -46,-30 -44,-40 C-46,-64 -42,-92 -35,-112Z" fill="%s"/>' % HAIR)
    # neck
    p.append('<rect x="-9" y="-66" width="18" height="26" rx="7" fill="%s"/><path d="M-9,-60 Q0,-53 9,-60 V-50 Q0,-45 -9,-50Z" fill="%s" opacity=".55"/>' % (SKIN, SHADE))
    # tee, then the blazer's two halves with lapels, and a thin chain
    p.append('<path d="M-17,-47 Q0,-40 17,-47 L12,26 H-12Z" fill="%s"/>' % TEE)
    p.append('<path d="M-8,-44 Q0,-35 8,-44" fill="none" stroke="%s" stroke-width="1.6"/><circle cx="0" cy="-36.5" r="2" fill="%s"/>' % (GOLD, GOLD))
    for m in (1, -1):
        p.append('<path d="M%g,26 C%g,-22 %g,-42 %g,-47 L%g,-4 L%g,26Z" fill="%s"/>' % (-62 * m, -62 * m, -46 * m, -16 * m, -5 * m, -9 * m, BLAZER))
        p.append('<path d="M%g,-47 L%g,-30 L%g,-24 L%g,-4" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (-16 * m, -26 * m, -14 * m, -5 * m, LAPEL))
    # ears and earrings
    p.append('<circle cx="-30" cy="-92" r="5.5" fill="%s"/><circle cx="30" cy="-92" r="5.5" fill="%s"/><circle cx="-30" cy="-84" r="2.6" fill="%s"/><circle cx="30" cy="-84" r="2.6" fill="%s"/>' % (SKIN, SKIN, GOLD, GOLD))
    # face
    p.append('<path d="M-29,-104 C-29,-129 29,-129 29,-104 C29,-80 17,-60 0,-58 C-17,-60 -29,-80 -29,-104Z" fill="%s"/>' % SKIN)
    p.append('<path d="M-1,-88 Q2.6,-80 -1.6,-77.5" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % SHADE)
    # hair in front: side-parted fringe and two long strands
    p.append('<path d="M-31,-100 C-36,-136 -4,-146 18,-139 C35,-132 38,-113 31,-95 C27,-111 17,-121 1,-123 C-11,-117 -22,-110 -31,-100Z" fill="%s"/>' % HAIR)
    p.append('<path d="M-30,-106 C-37,-86 -36,-66 -41,-44 L-33,-44 C-30,-64 -28,-86 -26,-102Z" fill="%s"/><path d="M31,-100 C36,-84 36,-66 41,-46 L33,-46 C30,-64 29,-84 28,-98Z" fill="%s"/>' % (HAIR, HAIR))
    p.append('<path d="M-14,-136 C-4,-141 10,-141 18,-136" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round" opacity=".8"/>' % SHINE)
    D = "#2A1C18"
    eyes = lambda: "".join('<ellipse cx="%g" cy="-93" rx="3.6" ry="4.3" fill="%s"/><circle cx="%g" cy="-94.6" r="1.2" fill="#FFFFFF"/><path d="M%g,-97.5 Q%g,-100.5 %g,-97.5" fill="none" stroke="%s" stroke-width="1.7" stroke-linecap="round"/>' % (
        x, D, x + 1.2, x - 5, x, x + 5, D) for x in (-11, 11))
    brow = lambda d: '<path d="%s" fill="none" stroke="%s" stroke-width="2.8" stroke-linecap="round"/>' % (d, HAIR)
    cheeks = lambda o: '<circle cx="-19" cy="-80" r="5" fill="%s" opacity="%s"/><circle cx="19" cy="-80" r="5" fill="%s" opacity="%s"/>' % (CHEEK, o, CHEEK, o)
    F = {
        "n": brow("M-17,-103 Q-11,-106 -5,-104 M5,-104 Q11,-106 17,-103") + eyes() + cheeks(".22") +
             '<path d="M-7,-71 Q0,-66 7,-71" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % LIP,
        "w": brow("M-17,-101 Q-11,-103 -5,-107 M5,-107 Q11,-103 17,-101") + eyes() +
             '<path d="M-6,-69 Q0,-73 6,-69" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % LIP,
        "t": brow("M-17,-102 L-5,-103 M5,-103 L17,-102") +
             '<path d="M-16,-93.5 Q-11,-90.5 -6,-93.5 M6,-93.5 Q11,-90.5 16,-93.5" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % D +
             '<path d="M-15,-87.5 Q-11,-85.5 -7,-87.5 M7,-87.5 Q11,-85.5 15,-87.5" fill="none" stroke="%s" stroke-width="1.3" stroke-linecap="round"/>' % SHADE +
             '<path d="M-6,-71 L6,-71" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % LIP,
        "d": brow("M-17,-104 Q-11,-104.5 -5,-102 M5,-102 Q11,-104.5 17,-104") + eyes() + cheeks(".25") +
             '<path d="M-8,-72 Q0,-65 8,-72" fill="none" stroke="%s" stroke-width="2.8" stroke-linecap="round"/>' % LIP,
        "h": brow("M-17,-105 Q-11,-109 -5,-106 M5,-106 Q11,-109 17,-105") +
             '<path d="M-16,-92 Q-11,-98 -6,-92 M6,-92 Q11,-98 16,-92" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % D + cheeks(".5") +
             '<path d="M-9,-73.5 Q0,-60 9,-73.5Z" fill="#7E2F38"/><path d="M-7.6,-73 Q0,-71 7.6,-73 L6.6,-70.4 Q0,-68.8 -6.6,-70.4Z" fill="#FFFFFF"/>',
        "s": brow("M-17,-101 Q-11,-103 -5,-106 M5,-106 Q11,-103 17,-101") +
             "".join('<ellipse cx="%g" cy="-91.5" rx="3.4" ry="3.6" fill="%s"/><path d="M%g,-95.5 Q%g,-97.5 %g,-95.5" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % (x, D, x - 5, x, x + 5, D) for x in (-11, 11)) +
             '<path d="M-7,-69 Q0,-74 7,-69" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % LIP,
        "c": brow("M-17,-100 Q-11,-102 -5,-107 M5,-107 Q11,-102 17,-100") +
             "".join('<ellipse cx="%g" cy="-91.5" rx="3.4" ry="3.6" fill="%s"/><circle cx="%g" cy="-92.6" r="1.1" fill="#FFFFFF"/>' % (x, D, x + 1, ) for x in (-11, 11)) +
             '<path class="tear" d="M-14,-86 q-3.2,6 0,9 q3.2,-3 0,-9Z" fill="#8EC5FF"/><path class="tear" style="animation-delay:.8s" d="M14,-86 q-3.2,6 0,9 q3.2,-3 0,-9Z" fill="#8EC5FF"/>' +
             '<path d="M-7,-69 Q-3.5,-72.5 0,-70.5 Q3.5,-72.5 7,-69" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % LIP,
        "g": brow("M-17,-104 Q-11,-106 -5,-105 M5,-106 Q11,-110 17,-107") +
             "".join('<ellipse cx="%g" cy="-93" rx="3.6" ry="4.3" fill="%s"/><circle cx="%g" cy="-94.6" r="1.2" fill="#FFFFFF"/>' % (x + 2.4, D, x + 3.4) for x in (-11, 11)) + cheeks(".5") +
             '<path d="M-6,-70.5 Q2,-67 8,-73" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % LIP,
        "x": brow("M-17,-107 Q-11,-111 -5,-108 M5,-108 Q11,-111 17,-107") +
             "".join('<ellipse cx="%g" cy="-93" rx="4" ry="5" fill="%s"/><circle cx="%g" cy="-95" r="1.4" fill="#FFFFFF"/>' % (x, D, x + 1.3) for x in (-11, 11)) +
             '<ellipse cx="0" cy="-70" rx="4.2" ry="5.2" fill="#7E2F38"/>',
        "j": brow("M-17,-106 Q-11,-110 -5,-107 M5,-107 Q11,-110 17,-106") +
             '<path d="M-16,-92 Q-11,-98 -6,-92 M6,-92 Q11,-98 16,-92" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % D + cheeks(".55") +
             '<path class="tear" d="M-19,-89 q-2.4,5 0,7.5 q2.4,-2.5 0,-7.5Z" fill="#8EC5FF"/><path class="tear" style="animation-delay:.6s" d="M19,-89 q-2.4,5 0,7.5 q2.4,-2.5 0,-7.5Z" fill="#8EC5FF"/>' +
             '<path d="M-10,-74 Q0,-58 10,-74Z" fill="#7E2F38"/><path d="M-8.4,-73.4 Q0,-71.2 8.4,-73.4 L7.4,-70.6 Q0,-68.8 -7.4,-70.6Z" fill="#FFFFFF"/>',
    }
    for k, c in faces.items():
        p.append('<g class="%s">%s</g>' % (("t " + c) if c else "", F[k]))
    def arm(d, hx, hy):
        return ('<path d="%s" fill="none" stroke="%s" stroke-width="17" stroke-linecap="round"/><circle cx="%g" cy="%g" r="8.5" fill="%s"/>' % (d, BLAZER, hx, hy, SKIN))
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
        "ear": arm("M-50,-26 C-64,-8 -66,10 -62,24", -62, 28) + '<rect x="26" y="-114" width="15" height="30" rx="4" fill="%s" transform="rotate(-14 33 -99)"/>' % INK
               + arm("M50,-26 C68,-42 56,-72 38,-86", 36, -88),
        "face": arm("M-50,-26 C-64,-42 -48,-64 -27,-74", -25, -76) + arm("M50,-26 C64,-42 48,-64 27,-74", 25, -76),
        "scroll": '<rect x="-13" y="-30" width="26" height="38" rx="5" fill="%s"/><rect x="-10" y="-26" width="20" height="28" rx="2" fill="#8FA6FF"/>' % INK
                  + arm("M-50,-26 C-62,-6 -40,8 -14,-2", -11, -3) + arm("M50,-26 C62,-6 40,8 14,-2", 11, -3),
        "chin": arm("M-50,-26 C-62,-6 -52,14 -30,20", -26, 20) + arm("M50,-26 C60,-10 40,-40 16,-60", 14, -62),
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
    notes = "".join('<g transform="rotate(%d %d %d)"><rect x="%d" y="%d" width="46" height="40" rx="4" fill="%s"/><text x="%d" y="%d" text-anchor="middle" font-size="9.5" font-weight="700" fill="#5B4A1C">%s</text></g>' % (
        r, x + 23, y + 20, x, y, c, x + 23, y + 24, t) for x, y, c, r, t in [(226, 52, "#FFE58A", -5, "Speak up!"), (280, 46, "#FFD1DC", 4, "Apply!!"), (310, 96, "#CDEBD9", 3, "Gym?")])
    cert = ('<rect x="64" y="186" width="92" height="66" rx="6" fill="#FFFFFF" stroke="#D9CBA8" stroke-width="3"/><circle cx="110" cy="206" r="8" fill="#F2C063"/>'
            '<rect x="80" y="222" width="60" height="5" rx="2.5" fill="#D8DAE0"/><rect x="88" y="233" width="44" height="5" rx="2.5" fill="#D8DAE0"/>')
    icons = ('<g class="pop" style="animation-delay:0s"><circle cx="404" cy="104" r="22" fill="#E3F2EA"/><text x="404" y="113" text-anchor="middle" font-size="24" font-weight="700" fill="#127A4F">?</text></g>'
             '<g class="pop" style="animation-delay:.6s"><circle cx="464" cy="104" r="22" fill="#E6EDF9"/><circle cx="464" cy="104" r="11" fill="none" stroke="#4A72C8" stroke-width="3"/><path d="M464,97 v7 l5,4" stroke="#4A72C8" stroke-width="3" fill="none" stroke-linecap="round"/></g>'
             '<g class="pop" style="animation-delay:1.2s"><circle cx="524" cy="104" r="22" fill="#F6EEDC"/><path d="M514,110 c0,-14 4,-19 10,-19 s10,5 10,19Z" fill="none" stroke="#A87A22" stroke-width="3" stroke-linejoin="round"/><circle cx="524" cy="114" r="2.5" fill="#A87A22"/></g>')
    tabs = "".join('<rect x="%d" y="252" width="14" height="5" rx="2" fill="%s"/>' % (356 + i * 16, c) for i, c in enumerate(["#FF6B6B", "#F4B942", "#7FD1AE", "#8FA6FF", "#C7C7CC"]))
    inner = ('<rect x="64" y="56" width="140" height="104" rx="14" fill="#1F2A55"/><circle cx="176" cy="82" r="14" fill="#F6E7B8"/><circle cx="182" cy="78" r="12" fill="#1F2A55"/>' + stars + notes + cert +
             FLOOR + riya(270, 308, 1, faces={"t": ""}, arms={"desk": ""}) + desk(120, 322, 380) +
             '<g><rect x="150" y="296" width="64" height="26" rx="4" fill="#E9E1D2"/><rect x="154" y="286" width="58" height="12" rx="3" fill="#6B7BD8"/><rect x="152" y="276" width="62" height="12" rx="3" fill="#F2A77E"/></g>'
             '<g><path d="M338,322 h118 l-10,-6 h-98Z" fill="#9AA0AE"/><rect x="350" y="248" width="94" height="66" rx="7" fill="#2B3350"/><rect class="glowlap" x="356" y="260" width="82" height="48" rx="3" fill="#8FA6FF" opacity=".55"/>' + tabs +
             '<rect x="362" y="270" width="52" height="5" rx="2.5" fill="#FFFFFF" opacity=".8"/><rect x="362" y="281" width="68" height="4" rx="2" fill="#FFFFFF" opacity=".5"/><rect x="362" y="291" width="40" height="4" rx="2" fill="#FFFFFF" opacity=".5"/></g>'
             '<g><rect x="468" y="298" width="22" height="24" rx="5" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/><path class="steam" d="M479,292 q-4,-6 0,-12 q4,-6 0,-12" fill="none" stroke="#C7C7CC" stroke-width="2.5" stroke-linecap="round"/></g>' +
             thought(376, 70, 176, 68, icons, hx=318, hy=184))
    return scene(inner, "Riya, 25, at her desk late at night: certificates on the wall, sticky notes, too many browser tabs, and three worries: what she's good at, where her days go, and her job search", "#F2F3F8")

def ch_test():
    q = lambda y, on=False, cls="": ('<g class="%s"><rect x="378" y="%g" width="150" height="26" rx="8" fill="%s" stroke="%s" stroke-width="1.5"/><circle cx="394" cy="%g" r="6" fill="%s" stroke="%s" stroke-width="1.5"/><rect x="408" y="%g" width="%d" height="6" rx="3" fill="%s"/></g>') % (
        cls, y, "#E3F2EA" if on else "#FFFFFF", "#127A4F" if on else "#E5E5EA", y + 13, "#127A4F" if on else "#FFFFFF", "#127A4F" if on else "#C7C7CC", y + 10, 96 if on else 80, "#127A4F" if on else "#D8DAE0")
    bars = "".join('<rect class="bar" style="transition-delay:%.2fs" x="%d" y="%d" width="10" height="%d" rx="3" fill="#127A4F" opacity="%.2f"/>' % (i * .06, 386 + i * 14, 340 - h, h, .55 + .045 * i)
                   for i, h in enumerate([44, 62, 38, 70, 52, 58, 34, 66, 48, 60]))
    phone = ('<g class="t v2 v3 v4"><rect x="360" y="64" width="186" height="334" rx="28" fill="%s"/><rect x="368" y="72" width="170" height="318" rx="22" fill="#FFFFFF"/>' % INK +
             logo_at("test", 380, 88, 24) + '<text x="412" y="106" font-size="14" font-weight="700" fill="%s">HV Test</text>' % INK +
             '<g class="t v2"><rect x="380" y="124" width="146" height="5" rx="3" fill="#E3F2EA"/><rect class="progress" x="380" y="124" width="146" height="5" rx="3" fill="#127A4F"/>'
             '<rect x="380" y="146" width="140" height="8" rx="4" fill="%s"/><rect x="380" y="162" width="104" height="8" rx="4" fill="%s"/>' % (INK, INK) +
             q(190) + q(224, True, "pick") + q(258) + q(292) + '</g>'
             '<g class="t v3"><text x="453" y="140" text-anchor="middle" font-size="12" font-weight="600" fill="#86868B">YOUR SCORE</text>'
             '<circle cx="453" cy="196" r="40" fill="none" stroke="#E3F2EA" stroke-width="10"/><circle class="ring" cx="453" cy="196" r="40" fill="none" stroke="#127A4F" stroke-width="10" stroke-linecap="round" stroke-dasharray="251" stroke-dashoffset="251" transform="rotate(-90 453 196)"/>'
             '<text x="453" y="205" text-anchor="middle" font-size="28" font-weight="700" fill="%s">78</text>' % INK + bars +
             '<text x="453" y="366" text-anchor="middle" font-size="12" font-weight="600" fill="#86868B">10 AREAS · 2 PDFs</text></g>'
             '<g class="t v4"><text x="380" y="140" font-size="11" font-weight="700" fill="#127A4F" letter-spacing=".6">YOUR 30-DAY PLAN</text>' +
             "".join('<rect x="380" y="%d" width="146" height="42" rx="10" fill="%s"/><rect x="390" y="%d" width="14" height="14" rx="4" fill="#FFFFFF" stroke="#127A4F" stroke-width="1.8"/><text x="412" y="%d" font-size="12" font-weight="600" fill="%s">%s</text><text x="412" y="%d" font-size="10" fill="#86868B">%s</text>' % (
                 y, "#F2F8F4" if i % 2 == 0 else "#FFFFFF", y + 10, y + 18, INK, t, y + 32, sub) for i, (y, t, sub) in enumerate([(152, "SQL, 45 min daily", "real problems, timed"), (200, "Speak 20 min daily", "record, listen back"), (248, "Write 3 real stories", "proof of strengths"), (296, "Show up daily", "consistency: 48")])) +
             '<text x="453" y="366" text-anchor="middle" font-size="12" font-weight="600" fill="#86868B">Built from your results</text></g></g>')
    inner = (FLOOR +
             '<g class="t v1"><clipPath id="mehta-cut"><rect x="330" y="0" width="270" height="344"/></clipPath><g clip-path="url(#mehta-cut)">' + people.figure(dict(people.CAST["mehta"], pose="clasp"), 470, 340, 1) + '</g>' + desk(360, 330, 220) +
             '<rect x="372" y="344" width="196" height="72" rx="4" fill="#CDB592"/></g>' +
             bubble(300, 34, 280, 70, "Your strengths? And a quick|SQL query, top 5 customers.", "right", "t v1", size=15, tailx=462) +
             chair(190, 396) + riya(190, 370, 1.05, faces={"w": "v1", "n": "v2", "h": "v3", "d": "v4"}, arms={"down": "v1", "phone": "v2 v3 v4"}, sweat="v1", bulb="v3") +
             thought(60, 60, 150, 58, '<text x="135" y="98" text-anchor="middle" font-size="26" font-weight="700" fill="#C7C7CC">? ? ?</text>', "t v1", hx=160, hy=150) +
             bubble(28, 40, 272, 66, "Strong: problem solving, teamwork.|To fix: speaking, SQL, consistency.", "right", "t v4", "#E3F2EA", 14, "#0B4F33", tailx=182) +
             phone)
    return scene(inner, "Riya freezing at an interview, then taking HV Test on her phone, seeing her strengths and gaps, and getting a 30-day plan")

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
             FLOOR + riya(180, 334, 1, faces={"g": "v1", "n": "v2", "d": "v3 v5", "h": "v4"}, arms={"desk": "v1 v2 v3 v5", "tea": "v4"}) + desk(40, 348, 290) +
             '<g class="t v1"><rect x="236" y="318" width="20" height="30" rx="5" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/><rect x="262" y="322" width="20" height="26" rx="5" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/><rect x="288" y="316" width="20" height="32" rx="5" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/></g>'
             '<g class="t v1">' + notifs + '<g transform="rotate(4 470 90)"><rect x="420" y="40" width="112" height="96" rx="8" fill="#FFF8E1" stroke="#EADCB0"/>' +
             "".join('<rect x="434" y="%d" width="12" height="12" rx="3" fill="#FFFFFF" stroke="#C9B98A"/><rect class="wiggle" x="454" y="%d" width="62" height="6" rx="3" fill="#C9B98A"/>' % (58 + i * 20, 61 + i * 20) for i in range(4)) + '</g></g>'
             '<g class="t v2 v3 v4 v5 panel"><rect x="336" y="56" width="236" height="330" rx="22" fill="#FFFFFF" stroke="#E5E5EA" stroke-width="1.5"/>' + logo_at("reset", 352, 72, 26) +
             '<text x="386" y="91" font-size="14" font-weight="700" fill="%s">HV Reset</text><text x="352" y="134" font-size="36" font-weight="300" fill="%s" class="mono">01:14:52</text>' % (INK, INK) +
             '<g class="t v2 v3 v4"><g class="shift">' + blk(0, 156, 204, "9:00  SQL practice", "#4A72C8") + blk(1, 204, 204, "11:00  Short break", "#EEF0F4", "#6E6E73") + blk(2, 252, 204, "2:00  Speaking practice", "#4A72C8") + blk(3, 300, 204, "6:00  Evening walk", "#F4B942", INK) + '</g></g>'
             '<g class="t v5">' + "".join('<g class="blk5" style="--d:%.2fs"><rect x="352" y="%d" width="204" height="40" rx="10" fill="%s"/><text x="366" y="%d" font-size="14" font-weight="600" fill="%s">%s</text></g>' % (
                 i * .12, 156 + i * 48, f, 181 + i * 48, tc, t) for i, (t, f, tc) in enumerate([("9:00  SQL practice", "#4A72C8", "#FFFFFF"), ("2:00  Speaking practice", "#4A72C8", "#FFFFFF"),
                                                                                              ("4:00  Interview prep", "#127A4F", "#FFFFFF"), ("6:00  Apply to 3 jobs", "#A87A22", "#FFFFFF")])) +
             '<rect x="352" y="350" width="204" height="26" rx="13" fill="#E6EDF9"/><text x="454" y="367" text-anchor="middle" font-size="12" font-weight="700" fill="#2E43A6">30-day plan · day 24 of 30</text></g>'
             '<g class="t v3 late"><rect x="478" y="72" width="80" height="26" rx="13" fill="#FBF1DF"/><text x="518" y="90" text-anchor="middle" font-size="12" font-weight="700" fill="#9A6512">Restart ↻</text></g>'
             '<g class="t v4"><rect x="352" y="350" width="204" height="26" rx="13" fill="#E3F2EA"/><text x="454" y="367" text-anchor="middle" font-size="12" font-weight="700" fill="#0B4F33">SQL 38 → 81% · Mock 4 → 8 ↑</text></g></g>'
             '<g class="t v4 dash"><rect x="22" y="28" width="300" height="136" rx="18" fill="#FFFFFF" stroke="#E5E5EA" stroke-width="1.5"/><text x="40" y="54" font-size="12" font-weight="700" fill="#86868B" letter-spacing=".5">HER DASHBOARD · WEEK 6</text>' + "".join('<text x="%d" y="92" font-size="24" font-weight="700" fill="%s">%s</text><text x="%d" y="110" font-size="11" font-weight="600" fill="#86868B">%s</text>' % (x, c, v, x, l) for x, v, l, c in [(40, "78%", "on time", "#127A4F"), (134, "42h", "focused", "#4A72C8"), (228, "12", "day streak", "#A87A22")]) + "".join('<rect x="%d" y="%d" width="14" height="%d" rx="3" fill="#4A72C8" opacity="%.2f"/>' % (40 + i * 20, 150 - h, h, .35 + .06 * i) for i, h in enumerate([8, 12, 10, 16, 18, 22]) ) + '<text x="170" y="148" font-size="11" font-weight="600" fill="#9A6512">Evenings slip → move them</text></g>' + '<g class="t v2"><rect x="24" y="136" width="292" height="44" rx="16" fill="#2E43A6"/><text x="40" y="156" font-size="11" font-weight="700" fill="#C9D3FF">To HV AI</text><text x="40" y="172" font-size="12.5" font-weight="600" fill="#FFFFFF">“Roz 9 baje SQL, 2 baje speaking”</text></g>')
    return scene(inner, "Riya's scattered days, then HV AI turning her 30-day plan into timed tasks in HV Reset, a restart after missed days, her progress going up, and interview prep and applying added to her day")

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
             chair(170, 393) + riya(170, 366, 1.05, faces={"w": "v1", "n": "v2", "x": "v3", "j": "v4"}, arms={"reach": "v1", "down": "v2", "face": "v3", "up": "v4"}) +
             '<g class="t v2 v3 v4 panel"><rect x="318" y="52" width="258" height="244" rx="20" fill="#FFFFFF" stroke="#E5E5EA" stroke-width="1.5"/>' + logo_at("vault", 332, 66, 24) +
             '<text x="364" y="84" font-size="14" font-weight="700" fill="%s">HV Vault</text>' % INK +
             '<text x="562" y="84" text-anchor="end" font-size="12" font-weight="700" fill="#A87A22">34 applied</text>' +
             "".join('<text x="%d" y="116" font-size="10" font-weight="700" fill="#86868B" letter-spacing="1">%s</text>' % (x, t) for x, t in [(334, "SAVED"), (416, "APPLIED"), (498, "INTERVIEW")]) +
             card(332, 126, "", "Razorpay", False, "v2 v3 v4", 0) + card(332, 178, "", "Meesho", False, "v2 v3 v4", .15) +
             card(414, 126, "", "Cred", True, "v2 v3 v4", .3) + card(496, 126, "", "Zomato", False, "v2 v3 v4", .45) + card(496, 178, "", "Tue 4 PM", False, "v3 v4", .1) + '</g>' +
             '<g class="t v3"><g class="ring-bell"><circle cx="560" cy="44" r="20" fill="#F6EEDC"/><path d="M551,50 c0,-12 3,-17 9,-17 s9,5 9,17Z" fill="none" stroke="#A87A22" stroke-width="2.6" stroke-linejoin="round"/><circle cx="560" cy="54" r="2.4" fill="#A87A22"/></g>'
             '<rect x="318" y="312" width="258" height="40" rx="14" fill="%s"/><text x="334" y="337" font-size="13.5" font-weight="600" fill="#FFFFFF">Kal 4 baje Zomato interview</text>' % "#2E43A6" +
             '<rect x="318" y="360" width="200" height="40" rx="14" fill="#FFFFFF" stroke="#E5E5EA"/><text x="334" y="385" font-size="13.5" font-weight="600" fill="%s">📅 Tue · 4:00 PM ✓</text></g>' % INK +
             '<g class="t v4"><g class="envelope"><rect x="360" y="316" width="150" height="92" rx="10" fill="#FFFFFF" stroke="#D2D2D7" stroke-width="2"/><path d="M360,322 l75,50 l75,-50" fill="none" stroke="#D2D2D7" stroke-width="2"/>'
             '<rect class="letter" x="378" y="300" width="114" height="60" rx="6" fill="#F6EEDC"/><text class="letter" x="435" y="336" text-anchor="middle" font-size="16" font-weight="800" fill="#A87A22">OFFER</text><text class="letter" x="435" y="352" text-anchor="middle" font-size="10.5" font-weight="600" fill="#7C5712">Product Analyst</text></g>' + confetti + '</g>')
    return scene(inner, "Riya's scattered job links, then HV Vault holding 34 applications on one board, a follow-up and an interview on the calendar, and finally an offer letter")

def finale():
    inner = ('<rect width="600" height="460" rx="28" fill="#F5F6FA"/>' +
             '<path class="loop" d="M125,350 C125,428 475,428 475,350" fill="none" stroke="#E3A23B" stroke-width="3" stroke-dasharray="4 10" stroke-linecap="round"/>'
             '<path d="M117,362 L125,346 L133,362" fill="none" stroke="#E3A23B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
             '<text x="300" y="446" text-anchor="middle" font-size="16" font-weight="700" fill="#9A6512">↻ Grow, and go again</text>' +
             "".join('<g class="link" style="animation-delay:%.1fs"><rect x="%d" y="232" width="70" height="26" rx="13" fill="none" stroke="%s" stroke-width="6"/><rect x="%d" y="232" width="70" height="26" rx="13" fill="none" stroke="%s" stroke-width="6"/></g>' % (
                 d, x, c1, x + 44, c2) for d, x, c1, c2 in [(.2, 172, "#127A4F", "#4A72C8"), (.5, 342, "#4A72C8", "#A87A22")]) +
             logo_at("test", 70, 190, 110) + logo_at("reset", 245, 190, 110) + logo_at("vault", 420, 190, 110) +
             "".join('<text x="%d" y="332" text-anchor="middle" font-size="18" font-weight="700" fill="%s">%s</text>' % (x, INK, t) for x, t in [(125, "Know"), (300, "Grow"), (475, "Act")]) +
             riya(300, 150, .62, faces={"h": ""}, arms={"up": ""}))
    return '<svg class="art" viewBox="0 0 600 460" role="img" aria-label="HV Test, HV Reset and HV Vault linked as a chain, looping back to grow, with Riya cheering">%s</svg>' % inner

# (icon letter, icon colour, app, title, body, meta, side)  side: "" notification, "me" her own message, "them" a reply
INTER = {
 "night": dict(face=("s", "scroll", "#26305E"), mood="another rejection, can't sleep", dark=True, time="Sunday · 11:48 PM", title="The night it all piles up.",
   text="Riya should be asleep. Two years since college, and she's still at home: comfortable, safe, and quietly stuck. Tonight she's reading the same email again. Another skill test failed, another interview gone wrong. She has the degree. She has the certificates. So why does every test feel like a language she only half knows, and why does she go blank the moment someone asks about her?",
   items=[("@mom", "", "WhatsApp", "Mom", "Beta, Sharma aunty ki beti ki job lag gayi 😊 Tera kab hoga?", "11:31 PM", ""),
          ("@ananya", "", "LinkedIn", "Ananya, your batchmate", "started a new position at a top startup. Say congrats!", "11:40 PM", ""),
          ("M", "#EA4335", "Mail", "Online skill test result", "You scored 41%. The cut-off was 65%. We won't be moving ahead.", "9:14 PM", ""),
          ("M", "#EA4335", "Mail", "Interview feedback", "Communication and clarity need work. Couldn't complete the SQL task.", "Fri", "")],
   voice="I have the degree and the certificates. Why does nobody pick me?",
   pains=["Failed skill tests", "Doesn't know her strengths", "Freezes in interviews", "Family pressure"],
   bridge="She doesn't need a fourth certificate. She needs to know where she actually stands."),
 "kalse": dict(face=("g", "scroll", "#2B2F5C"), mood="caught in the scroll, again", dark=True, time="Day 3 of her plan · 10:05 AM", title="Knowing isn't doing.",
   text="Her self-assessment told her exactly what to fix. For two days she's on fire. On day three the old Riya is back: one reel becomes forty, and the interview-practice video sits paused at 7:42. Again.",
   items=[("▶", "#FF0000", "YouTube", "How to answer &ldquo;Tell me about yourself&rdquo;", "Paused at 7:42 of 18:20", "yesterday", ""),
          ("◎", "#E1306C", "Instagram", "priya.codes and 12 others", "posted new reels", "10:02 AM", ""),
          ("✎", "#F4B942", "Notes", "My routine", "Monday: start fresh ✅  Tuesday: start fresh again", "", ""),
          ("31", "#4A72C8", "Calendar", "SQL practice, 10:00", "Missed", "10:00 AM", "")],
   voice="Kal se pakka. (From tomorrow. For sure.)",
   pains=["Procrastination", "Phone traps", "Restarting every Monday", "Guilt"],
   bridge="She doesn't need more motivation. She needs a simpler day."),
 "inbox": dict(face=("c", "face", "#2A2A52"), mood="two rejections before breakfast", dark=True, time="Week 7 · Monday morning", title="The inbox that hurts.",
   text="Her skills are real now, and so is the job hunt. So is the mess: job links buried in chats, three versions of her resume, and a tracker spreadsheet she stopped updating 19 days ago.",
   items=[("M", "#EA4335", "Mail", "Finlo Careers", "Unfortunately, we have decided to move forward with other candidates.", "9:02 AM", ""),
          ("M", "#EA4335", "Mail", "Brightpath Analytics", "Thank you for your interest. The position has been filled.", "Sat", ""),
          ("@rohit", "", "WhatsApp", "Rohit (recruiter)", "Will get back to you by Friday 👍", "12 days ago", ""),
          ("▦", "#0F9D58", "Sheets", "jobs_tracker_FINAL_v2.xlsx", "Last edited 19 days ago", "", "")],
   voice="Did I already apply to that role? Did I ever follow up with Cred?",
   pains=["Rejections", "Ghosting", "Lost links", "Missed follow-ups"],
   bridge="Rejections are part of the game. Losing track of good chances doesn't have to be."),
 "call": dict(face=("j", "ear", "#FFE3C4"), mood="happy tears", dark=False, time="Week 11 · Thursday, 4:12 PM", title="The call.",
   text="Two weeks after the rejection that almost broke her streak, her phone rings. Unknown number. She almost lets it go. Then she picks up.",
   items=[("@kavya", "", "Phone", "Incoming call", "Kavya, Talent team", "4:12 PM", ""),
          ("M", "#EA4335", "Mail", "Offer letter: Product Analyst", "We're delighted to offer you the role. Please find the details attached.", "4:31 PM", ""),
          ("", "", "", "", "Maa, job lag gayi!! 🎉🎉", "4:33 PM", "me"),
          ("@mom", "", "", "Mom", "Mujhe pata tha ❤️ Sharma aunty ko main bataungi 😄", "4:34 PM", "them")],
   voice="Not luck. Consistency: eleven weeks of small, honest, slightly boring days.",
   pains=["Knew her strengths", "Showed up daily", "Never lost a lead", "Got the job"]),
}
def portrait(face, pose, bg):
    top = -146 if pose == "scroll" else -160   # show the phone in her hands
    return ('<svg viewBox="-68 %d 136 136" aria-hidden="true" focusable="false"><rect x="-68" y="%d" width="136" height="136" fill="%s"/>%s</svg>' % (
        top, top, bg, riya(0, 0, 1, faces={face: ""}, arms={pose: ""})))

def interlude(key):
    d = INTER[key]
    def item(ic, col, app, t, body, meta, side):
        if side:
            av = ('<span class="bav">%s</span>' % people.head(people.CAST[ic[1:]], 26)) if ic.startswith("@") else ""
            return '<div class="nt %s">%s%s<p>%s</p><small>%s</small></div>' % (side, av, ('<b>%s</b>' % t) if t else "", body, meta)
        if ic.startswith("@"):
            return ('<div class="nt"><span class="ico av">%s</span><div><div class="top"><em>%s</em><small>%s</small></div><b>%s</b><p>%s</p></div></div>' % (people.head(people.CAST[ic[1:]], 34), app, meta, t, body))
        return ('<div class="nt"><span class="ico" style="background:%s">%s</span><div><div class="top"><em>%s</em><small>%s</small></div><b>%s</b><p>%s</p></div></div>' % (col, ic, app, meta, t, body))
    return ('<section class="inter%s" id="%s"><div class="wrap grid">'
            '<div class="txt rv"><div class="who">%s<div><b>Riya</b><span>%s</span></div></div><p class="when">%s</p><h2>%s</h2><p class="story">%s</p><blockquote>&ldquo;%s&rdquo;</blockquote>'
            '<div class="pains">%s</div>%s</div>'
            '<div class="ph rv" role="group" aria-label="Riya\'s phone"><div class="notch"></div>%s</div></div></section>') % (
        "" if d["dark"] else " win", key, portrait(*d["face"]), d["mood"], d["time"], d["title"], d["text"], d["voice"],
        "".join('<span>%s</span>' % x for x in d["pains"]), ('<p class="bridge">%s</p>' % d["bridge"]) if d.get("bridge") else "",
        "".join(item(*i) for i in d["items"]))

LESSONS = [("Know your strengths and your gaps.", "She had strengths she'd never noticed and gaps her certificates had hidden. Two honest tests showed her both."),
           ("Give every task a time.", "Her comfort zone had no clock. A fixed start time for 45 minutes of SQL and 20 of speaking, every day, did what three certificates couldn't."),
           ("A missed day isn't a lost week.", "She shifted the day and kept going, instead of waiting for Monday to start over."),
           ("Track every chance. Follow up.", "34 applications, one list, reminders on time. The interview that changed everything came from a follow-up.")]
def cast():
    return "".join('<figure class="pc rv"><svg viewBox="-86 -166 172 520" role="img" aria-label="%s">%s</svg><figcaption><b>%s</b><em>%s</em><span>%s</span></figcaption></figure>' % (
        c["name"], people.figure(c), c["name"], c["role"], c["line"]) for c in people.CAST.values())

def next_art():
    riya = dict(people.CAST["riya"], expr="h")
    you = dict(people.CAST["riya"], hairstyle="short", extras=[], pose="down", expr="n")
    return ('<svg viewBox="-200 -190 400 580" role="img" aria-label="Riya standing next to an outline of you, with a question mark: you could be next">'
            '<circle cx="0" cy="70" r="190" fill="#E8ECFB"/>' + people.figure(riya, -86, 0, 1) +
            '<g class="ghost">' + people.figure(you, 92, 0, 1) + '</g>'
            '<text x="92" y="-78" text-anchor="middle" font-size="46" font-weight="700" fill="#FFFFFF">?</text>'
            '<text x="-86" y="372" text-anchor="middle" font-size="20" font-weight="700" fill="#1D1D1F">Riya</text>'
            '<text x="92" y="372" text-anchor="middle" font-size="20" font-weight="700" fill="#2E43A6">You</text></svg>')

def lessons():
    return "".join('<div class="ls rv"><span>%d</span><b>%s</b><p>%s</p></div>' % (i + 1, h, t) for i, (h, t) in enumerate(LESSONS))

# ---------------------------------------------------------------- chapters (scrollytelling)
def chapter(key, num, step, title, why, art, steps, tools):
    st = "".join('<div class="step" data-step="%d"><div class="cap"><p class="k">%s</p><h3>%s</h3><p>%s</p>%s</div></div>' % (
        i + 1, k, h, p, ('<p class="tools"><b>What Riya used</b>%s</p>' % tools) if i == len(steps) - 1 else "") for i, (k, h, p) in enumerate(steps))
    return interlude({"test": "night", "reset": "kalse", "vault": "inbox"}[key]) + ('<section class="chapter" id="%s"><div class="wrap"><div class="chead rv"><span class="num">Step %d · %s</span>'
            '<h2>%s</h2><p class="why"><b>Why this step matters.</b> %s</p></div>'
            '<div class="scrolly"><div class="stage-wrap"><div class="stage" data-step="1">%s</div></div><div class="steps">%s</div></div></div></section>') % (
        key, num, step, title, why, art, st)

CH = [
    chapter("test", 1, "Know where you stand", "What am I actually good at?",
        "Without an honest picture of yourself, you practise the wrong things and apply for the wrong roles. Everything after this depends on it.", ch_test(), [
        ("Week 0 · The problem", "Two questions. Two blanks.", "&ldquo;Tell me about your strengths.&rdquo; Riya says &ldquo;hard-working&rdquo; three times and gives no example. &ldquo;Now write a quick SQL query for our top five customers.&rdquo; Her certificate says SQL. Her hands don't. She freezes on both."),
        ("Week 1 · What she did", "She stops collecting certificates and measures.", "Two honest tests: one for her strengths and how she works, one for her actual skills. She used HV Test, which has both, free. What mattered was being honest with herself."),
        ("The result", "Strengths she never noticed. Gaps she never faced.", "Problem solving 82 and teamwork 86: all those college projects she quietly held together. But communication 46, and SQL 38: she knew the words from her courses, not the work. And consistency 48. It stings, and it's the first honest picture she's had."),
        ("The plan", "Less watching. More doing.", "No new course. 45 minutes of real, timed SQL problems and 20 minutes of speaking practice every day: answer one question, record it, listen back. Three real stories that prove her strengths. And the hard one: show up every day.")],
        '<a href="https://harshvittori.github.io/hv-tests/">HV Test</a>, free: a strengths assessment and a skills test.'),
    chapter("reset", 2, "Show up daily", "Why can't I stay consistent?",
        "Skills and confidence aren't things you finish, like a certificate. You practise them until the test and the hard question stop scaring you. And a comfort zone has no clock: without a time for each task, &ldquo;later&rdquo; always wins. This is the step where most people stop.", ch_reset(), [
        ("The problem", "Big plans. Lost days.", "Two years of no college, no office, no routine. Her comfort zone is very comfortable. She wakes at 10, gets stuck on SQL question 3 at 11, records one answer, hates how she sounds, checks her phone at 11:05, and suddenly it's evening. Again."),
        ("What she did", "Every task gets a time. No more &ldquo;later&rdquo;.", "Her comfort zone had no clock, so &ldquo;baad mein karungi&rdquo; always won. Now her 30-day plan runs on the clock: every task has a fixed start time. She used HV Reset: she typed &ldquo;Roz 9 baje SQL, 2 baje speaking practice&rdquo; to HV AI, and at 9:00 the task is on screen with a clock counting down. One task at a time, and the day pulls her out of bed."),
        ("Week 2 · A setback", "The comfort zone pulls back. She doesn't quit.", "A cold, a family function, and the old comfort of &ldquo;aaj rehne do&rdquo;. Two days gone. Instead of starting over on Monday, she shifts today's plan, keeps the one core task, and goes again. The streak resets. The progress doesn't."),
        ("Week 6 · The change", "Now it's just what she does.", "300 SQL problems and 42 recordings. Her timed SQL test: 38% five weeks ago, 81% today. Her answers: three minutes of rambling then, 60 seconds with a real example now. Neha ma'am, her old college teacher, does a mock interview with her: &ldquo;Now I believe you.&rdquo; Her HV Reset dashboard shows the rest: 78% of tasks started on time (it was 20% in week 1), 42 focused hours, a 12-day streak. It also shows her evening tasks slip the most, so she moves speaking practice to 2 PM. Out of the comfort zone, and she can see it."),
        ("Week 6 · Next", "Interview prep and applying go on the clock too.", "Day 24 of her 30-day plan. The same timed day now holds two more tasks: 4:00 interview prep with her three real stories, and 6:00 apply to three good roles. Applying stops being a midnight panic and becomes something she starts on time.")],
        '<a href="https://harshvittori.github.io/hv-reset/">HV Reset</a> with HV AI, free: a start time for every task, a clock that keeps the day moving, and a dashboard that shows how she&rsquo;s really doing.'),
    chapter("vault", 3, "Apply with a system", "Where did all my applications go?",
        "Real skills and confidence get you through the tests and interviews. A system gets you in front of enough of them. Without tracking and follow-ups, good chances quietly slip away, and the work from steps 1 and 2 goes to waste.", ch_vault(), [
        ("The problem", "Skills ready. Offers still missing.", "Her technical and communication skills are finally where they should be, and she clears most tests now. But offers don't come. She applies on five job sites, links sit in WhatsApp, she applied to one company twice, and she can't remember whom to follow up with."),
        ("Week 7 · What she did", "Every job in one place.", "Saved, applied, interview: every job in one place, updated the same day. She used HV Vault, a free job tracker. No more applying twice or losing a link: 34 applications over four weeks, each with its status, and three final interviews."),
        ("Follow-ups", "The follow-ups actually happen.", "After every application she sets a reminder to follow up. One quiet application turns into an interview because of it. She adds the interview to her calendar the moment it's fixed: &ldquo;Kal 4 baje&rdquo;, done."),
        ("Week 11 · The outcome", "A no. Then the yes.", "A final round says no, and it hurts. She notes what went wrong, preps with her real stories, and two weeks later signs the offer she wanted: Product Analyst.")],
        '<a href="https://harshvittori.github.io/hv-vault-web/">HV Vault</a>, free: one board for her applications and follow-ups.'),
]

TIMELINE = [("Week 1", "Takes a strengths test and a skills test. Communication 46, SQL 38, consistency 48. Ouch.", "#127A4F"),
            ("Week 2", "Plans each day the night before. Misses two days, then restarts instead of quitting.", "#4A72C8"),
            ("Week 5", "SQL test 81%, up from 38%. Mock interview 8 out of 10, up from 4. Her dashboard: 78% of tasks started on time, up from 20%.", "#4A72C8"),
            ("Week 6", "Adds interview prep and &ldquo;apply to 3 jobs&rdquo; to her timed daily plan.", "#4A72C8"),
            ("Week 7", "Starts applying, a few good roles a day, every one tracked in one place.", "#A87A22"),
            ("Week 8", "Ananya, the batchmate she used to envy, sends an opening at a friend's startup. Riya adds it to her list and applies that evening.", "#A87A22"),
            ("Week 9", "34 applications, 4 of 5 skill tests cleared, 3 final interviews. A follow-up revives a quiet lead.", "#A87A22"),
            ("Week 10", "Rejected after a final round. Writes down why, and preps again.", "#86868B"),
            ("Week 11", "Offer: Product Analyst. The role she was aiming for.", "#2E43A6")]
def timeline():
    return "".join('<li class="rv"><span class="dot" style="background:%s"></span><b>%s</b><p>%s</p></li>' % (c, w, t) for w, t, c in TIMELINE)

TOGGLE_CSS = ".stage[data-step=\"5\"] .blk5{animation:slidein .7s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d);animation-play-state:running}\n.blk5{transform-box:fill-box}\n" + "".join('.stage[data-step="%d"] .v%d{opacity:1;translate:0 0}\n.stage[data-step="%d"] .v%d,.stage[data-step="%d"] .v%d *{animation-play-state:running}\n' % (n, n, n, n, n, n) for n in range(1, 6))

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
.nav nav{display:flex;align-items:center;gap:4px;margin-left:auto;font-size:14px}
.nav nav a{position:relative;display:inline-block;white-space:nowrap;line-height:32px;height:32px;padding:0 13px;border-radius:999px;text-decoration:none;color:var(--soft);font-weight:500;transition:color .2s ease,background-color .2s ease,box-shadow .2s ease}
.nav nav a:hover{color:var(--accent);background:rgba(46,67,166,.07);text-decoration:none}
.nav nav a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.nav nav a[aria-current]{color:var(--accent);font-weight:600;background:#E8ECFB;box-shadow:inset 0 0 0 1px rgba(46,67,166,.14)}
.nav nav a[aria-current]:hover{background:#E1E6FA}
.pacts{display:flex;align-items:center;flex-wrap:wrap;gap:8px 18px;margin-top:18px}.pacts .btn{margin:0}.pcard .lm{color:var(--accent);font-weight:500;font-size:15px}
.more{margin-top:32px;font-size:17px}.more a{color:var(--accent);font-weight:600;text-decoration:none}.more a:hover{text-decoration:underline}
.brand{white-space:nowrap}
.ni{display:none;width:20px;height:20px;vertical-align:middle}
@media (max-width:720px){.nav nav a.ic{padding:0 8px}.nav nav a.ic .nt{display:none}.nav nav a.ic .ni{display:inline-block;margin-top:-3px}}
@media (max-width:720px){.nav nav a.opt,.nav .d{display:none}.nav nav{gap:2px}.nav nav a{height:30px;line-height:30px;padding:0 10px}}
@media (max-width:470px){.brand{font-size:0;gap:0}.nav nav a{padding:0 9px}}
@media (max-width:360px){.nav nav a{padding:0 7px;font-size:13.5px}}

/* no branding at the start: the menu bar slides in when Chapter 1 (the first tool) begins */
header{position:fixed;left:0;right:0;top:0;transition:transform .35s cubic-bezier(.2,.8,.2,1)}
header.hid{transform:translateY(-110%)}
header.hid:focus-within{transform:none}
/* hero */
.hero{display:grid;grid-template-columns:.9fr 1.1fr;gap:48px;align-items:center;padding:72px 0 84px}
.hero .eyebrow{font-size:15px;font-weight:600;color:var(--soft)}
.hero h1{font-size:clamp(46px,7vw,84px);font-weight:700;letter-spacing:-.045em;line-height:1.02;margin:12px 0 18px}
.hero .lead{font-size:clamp(19px,2.2vw,24px);color:var(--soft);line-height:1.35}
.hero .lead b{color:var(--ink);font-weight:600}
.worries{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.worries span{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:980px;background:var(--gray);font-size:15px;font-weight:500}
.worries i{width:10px;height:10px;border-radius:50%;display:inline-block}
.scroll-hint{display:inline-flex;align-items:center;gap:8px;margin-top:28px;font-size:16px;color:var(--faint)}
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
.why{font-size:18px;color:var(--soft);margin:14px auto 0;max-width:620px;line-height:1.45}.why b{color:var(--ink)}
.tools{margin-top:18px;padding:12px 14px;border-radius:14px;background:var(--gray);font-size:15px;color:var(--soft);line-height:1.45}
.tools b{display:block;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--faint);margin-bottom:2px}
.key .order{font-size:17px;color:rgba(255,255,255,.8);max-width:640px;margin:34px auto 0;line-height:1.5}
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
.aoff,.aoff *{animation-play-state:paused!important}   /* animations only run while their section is on screen */
@supports (content-visibility:auto){main>section:not(:first-child){content-visibility:auto;contain-intrinsic-size:auto 900px}}
@keyframes bob{50%{transform:translateY(4px)}}
.art .link,.art .pop{transform-box:fill-box;transform-origin:center}
@media (prefers-reduced-motion:reduce){.art *,.art .t{animation:none!important;transition:none!important}.art .ring{stroke-dashoffset:55}.art .bar{transform:none}}

/* before + journey */
.label{font-size:15px;font-weight:600;color:var(--accent);text-align:center}
.before{padding:72px 0 30px;background:var(--gray)}
.before .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;max-width:980px;margin:18px auto 0}
.before .stats div{background:#fff;border:1px solid #E4E5EA;border-radius:20px;padding:22px 20px;text-align:left}
.before .stats b{display:block;font-size:44px;font-weight:700;letter-spacing:-.04em;line-height:1}
.before .stats span{display:block;color:var(--soft);font-size:15px;margin-top:8px;line-height:1.35}
.before .note{text-align:center;color:var(--soft);font-size:19px;margin:26px 0 30px}
@media (max-width:820px){.before .stats{grid-template-columns:1fr 1fr}.before .stats b{font-size:36px}}
.journey{padding:100px 0 90px;border-top:1px solid #EEF0F4}
.journey h2{text-align:center;font-size:clamp(34px,5vw,58px);font-weight:700;letter-spacing:-.04em;line-height:1.05;margin-top:8px}
.journey .sub{text-align:center;color:var(--soft);font-size:20px;margin-top:10px}
.tl{list-style:none;margin:48px auto 0;padding:0 0 0 30px;max-width:680px;position:relative}
.tl::before{content:"";position:absolute;left:8px;top:8px;bottom:8px;width:2px;background:#E4E5EA}
.tl li{position:relative;padding:0 0 26px}
.tl .dot{position:absolute;left:-28px;top:5px;width:14px;height:14px;border-radius:50%;box-shadow:0 0 0 4px #fff}
.tl b{font-size:15px;font-weight:700;color:var(--soft)}
.tl p{font-size:19px;line-height:1.4;margin-top:2px}
.tl li:last-child p{font-weight:700}

/* interludes: her phone, between chapters */
.inter{padding:96px 0;background:#0E1430;color:#fff;position:relative;overflow:hidden}
.inter::before{content:"";position:absolute;inset:-30% -10% auto auto;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(91,111,224,.35),transparent 70%);pointer-events:none}
.inter.win{background:linear-gradient(135deg,#FFF6E6,#FDE7EF 55%,#E8EEFF);color:var(--ink)}
.inter.win::before{background:radial-gradient(circle,rgba(242,192,99,.45),transparent 70%)}
.inter .grid{display:grid;grid-template-columns:1fr 380px;gap:64px;align-items:center;position:relative}
.inter .when{font-size:14px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#9FB0FF}
.inter.win .when{color:#B5561E}
.inter h2{font-size:clamp(34px,5vw,58px);font-weight:700;letter-spacing:-.04em;line-height:1.04;margin-top:10px}
.inter .story{font-size:19px;line-height:1.5;color:rgba(255,255,255,.78);margin-top:16px;max-width:560px}
.inter.win .story{color:var(--soft)}
.inter blockquote{margin:26px 0 0;font-size:clamp(22px,2.6vw,30px);font-weight:600;font-style:italic;letter-spacing:-.02em;line-height:1.25;border-left:4px solid #FF8A8A;padding-left:18px;max-width:560px}
.inter.win blockquote{border-color:#34C759}
.pains{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px}
.pains span{font-size:14px;font-weight:600;padding:7px 13px;border-radius:999px;background:rgba(255,120,120,.14);color:#FFB3B3;border:1px solid rgba(255,138,138,.3)}
.inter.win .pains span{background:#E3F4EA;color:#0B6B3F;border-color:#BFE3CD}
.inter.win .pains span::before{content:"✓ "}
.cast{padding:96px 0 90px}
.cast h2{text-align:center;font-size:clamp(34px,5vw,58px);font-weight:700;letter-spacing:-.04em;line-height:1.05;margin-top:8px}
.cast .sub{text-align:center;color:var(--soft);font-size:20px;margin-top:10px}
.crow{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:40px max(20px,calc((100vw - 1120px)/2)) 20px;scrollbar-width:thin;-webkit-overflow-scrolling:touch}
.pc{flex:none;width:230px;margin:0;scroll-snap-align:center;background:linear-gradient(#F6F3EE,#EFEBE4);border-radius:26px;padding:18px 16px 20px;text-align:left}
.pc svg{display:block;width:100%;height:300px}
.pc b{display:block;font-size:19px;letter-spacing:-.02em;margin-top:10px}
.pc em{display:block;font-style:normal;font-size:14px;font-weight:600;color:var(--accent);margin-top:2px}
.pc span{display:block;font-size:14.5px;color:var(--soft);line-height:1.4;margin-top:8px}
.nt .ico.av{background:none;overflow:hidden;border-radius:50%}.nt .ico.av svg{display:block;width:34px;height:34px}
.nt .bav{float:left;margin:0 8px 0 -2px;border-radius:50%;overflow:hidden;width:26px;height:26px}.nt .bav svg{display:block}
.next{padding:100px 0 110px;background:var(--gray);border-top:1px solid #EEF0F4}
.ngrid{display:grid;grid-template-columns:.9fr 1.1fr;gap:56px;align-items:center}
.nart svg{display:block;width:100%;max-width:440px;height:auto;margin:0 auto}
.ghost *{fill:#AEBBEF!important;stroke:#AEBBEF!important;opacity:1!important}
.ghost ellipse:first-child{stroke:none!important;fill:#000!important;opacity:.06!important}
.next .label{text-align:left}
.next h2{font-size:clamp(36px,5.4vw,62px);font-weight:700;letter-spacing:-.045em;line-height:1.03;margin-top:8px}
.next .sub{font-size:20px;color:var(--soft);margin-top:14px;line-height:1.45}
.nsteps{list-style:none;padding:0;margin:28px 0 0;display:grid;gap:12px}
.nsteps li{display:flex;gap:14px;align-items:flex-start;background:#fff;border:1px solid #E4E5EA;border-radius:18px;padding:16px 18px}
.nsteps span{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;color:#fff;font-weight:700;font-size:15px}
.nsteps b{display:block;font-size:17.5px}.nsteps em{display:block;font-style:normal;color:var(--soft);font-size:15.5px;margin-top:2px}
.ncta{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}.ncta .btn{margin:0}
.nfor{color:var(--faint);font-size:15px;margin-top:18px}
@media (max-width:880px){.ngrid{grid-template-columns:1fr;gap:28px}.nart svg{max-width:340px}}
.who{display:flex;align-items:center;gap:16px;margin-bottom:26px}
.who svg{width:128px;height:128px;border-radius:32px;flex:none;box-shadow:0 18px 36px -18px rgba(0,0,0,.55)}
.who b{display:block;font-size:19px}.who span{display:block;font-size:15px;opacity:.72;margin-top:2px}
.tear{animation:tear 1.8s ease-in infinite}
@keyframes tear{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(12px);opacity:0}}
.bridge{margin-top:26px;font-size:18px;font-weight:600;color:#C9D3FF}
.ph{background:#151B38;border-radius:40px;padding:34px 14px 18px;box-shadow:0 40px 80px -30px rgba(0,0,0,.6),inset 0 0 0 2px rgba(255,255,255,.08);position:relative}
.inter.win .ph{background:#FFFFFF;box-shadow:0 40px 80px -36px rgba(120,60,20,.35),inset 0 0 0 1px #F0E4D8}
.ph .notch{position:absolute;top:12px;left:50%;width:90px;height:8px;margin-left:-45px;border-radius:8px;background:rgba(255,255,255,.14)}
.inter.win .ph .notch{background:#EEE6DD}
.nt{display:flex;gap:11px;background:rgba(255,255,255,.08);border-radius:20px;padding:12px 14px;margin-top:10px;text-align:left}
.inter.win .nt{background:#F6F4F1}
.nt .ico{flex:none;width:34px;height:34px;border-radius:9px;display:grid;place-items:center;font-size:13px;font-weight:800;color:#fff}
.nt>div{min-width:0;flex:1}
.nt .top{display:flex;justify-content:space-between;gap:8px;font-size:12px;opacity:.65}
.nt .top em{font-style:normal;font-weight:600;text-transform:uppercase;letter-spacing:.03em}
.nt b{display:block;font-size:14.5px;margin-top:1px}
.nt p{font-size:14.5px;line-height:1.35;opacity:.86;margin-top:1px}
.nt.me,.nt.them{display:block;max-width:82%;border-radius:18px;padding:9px 13px}
.nt.me{margin-left:auto;background:#DCF8C6!important;color:#10331A;border-bottom-right-radius:6px}
.nt.them{background:#FFFFFF!important;color:var(--ink);border:1px solid #EEE;border-bottom-left-radius:6px}
.nt.me small,.nt.them small{display:block;text-align:right;font-size:11px;opacity:.55;margin-top:2px}
.nt.them b{font-size:12px;color:#B5561E}
@media (prefers-reduced-motion:no-preference){.ph .nt{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .6s cubic-bezier(.2,.8,.2,1)}
  .ph.in .nt{opacity:1;transform:none}.ph.in .nt:nth-of-type(2){transition-delay:.35s}.ph.in .nt:nth-of-type(3){transition-delay:.7s}.ph.in .nt:nth-of-type(4){transition-delay:1.05s}}
@media (max-width:880px){.inter{padding:64px 0}.inter .grid{grid-template-columns:1fr;gap:34px}.ph{max-width:380px;width:100%;margin:0 auto}.inter .story{font-size:17px}}
.lessons{padding:90px 0 100px;background:var(--gray)}
.lessons h2{text-align:center;font-size:clamp(32px,4.8vw,54px);font-weight:700;letter-spacing:-.04em;margin-top:8px}
.lgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:40px}
.ls{background:#fff;border:1px solid #E4E5EA;border-radius:22px;padding:24px}
.ls span{display:inline-grid;place-items:center;width:32px;height:32px;border-radius:50%;background:#E8ECFB;color:var(--accent);font-weight:700;font-size:15px}
.ls b{display:block;font-size:19px;letter-spacing:-.02em;margin-top:14px;line-height:1.2}
.ls p{color:var(--soft);font-size:15.5px;margin-top:8px;line-height:1.45}
@media (max-width:980px){.lgrid{grid-template-columns:1fr 1fr}}@media (max-width:520px){.lgrid{grid-template-columns:1fr}}
.yourturn{text-align:center;font-size:20px;font-weight:600;margin-top:40px}.yourturn .btn{margin:0 0 0 10px;vertical-align:middle}
@media (max-width:520px){.yourturn .btn{display:flex;margin:14px auto 0;width:max-content}}

/* finale + people + builder */
.finale{padding:100px 0 110px;text-align:center;background:#FFFFFF;border-top:1px solid #EEF0F4}
.finale h2{font-size:clamp(34px,5vw,58px);font-weight:700;letter-spacing:-.04em;line-height:1.05}
.finale .sub{font-size:clamp(19px,2.2vw,24px);color:var(--soft);margin:12px auto 0;max-width:760px}
.key{padding:110px 0 120px;text-align:center;color:#fff;background:linear-gradient(135deg,#17225A,#2E43A6 58%,#4A46C9);position:relative;overflow:hidden}
.key::before{content:"";position:absolute;left:50%;top:-240px;width:760px;height:480px;margin-left:-380px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.14),transparent 70%);pointer-events:none}
.key .wrap{position:relative}
.key .label{color:#C9D3FF;margin-bottom:8px}
.key h2{font-size:clamp(44px,7vw,84px);font-weight:700;letter-spacing:-.045em;line-height:1.02}
.key .sub{font-size:clamp(19px,2.2vw,24px);color:rgba(255,255,255,.82);margin:14px auto 0;max-width:760px}
.key .eq i{color:rgba(255,255,255,.6)}
.key .term{color:var(--ink);border:0;border-top:4px solid var(--c);box-shadow:0 24px 50px -28px rgba(0,0,0,.5)}
.key .term.goal{--c:#F2C063;background:#F2C063;color:#1D1D1F}.key .term.goal em{color:#6B4A0E}.key .term.goal span{color:#4A3A1A}
.finale .label{margin-bottom:8px}
.eq{display:flex;align-items:stretch;justify-content:center;gap:10px;flex-wrap:wrap;margin:44px auto 0;max-width:1060px}
.eq i{align-self:center;font-style:normal;font-size:30px;font-weight:300;color:var(--faint)}
.term{flex:1 1 200px;max-width:230px;background:#fff;border:1px solid #E4E5EA;border-top:4px solid var(--c);border-radius:20px;padding:18px 18px 20px;text-align:left}
.term em{display:block;font-style:normal;font-size:13px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;color:var(--c)}
.term b{display:block;font-size:20px;letter-spacing:-.02em;margin-top:6px}
.term span{display:block;color:var(--soft);font-size:15px;margin-top:6px;line-height:1.4}
.term.goal{--c:#2E43A6;background:#2E43A6;border-color:#2E43A6;color:#fff}.term.goal em{color:#C9D3FF}.term.goal span{color:rgba(255,255,255,.8)}
@media (max-width:760px){.eq{flex-direction:column;align-items:center}.term{max-width:420px;width:100%;flex:none}.eq i{font-size:24px}}
.finale .art-box{max-width:720px;margin:40px auto 0;box-shadow:none;border:1px solid #EEF0F4}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:56px auto 0;max-width:960px;text-align:left}
.pcard{background:#fff;border:1px solid #E4E5EA;border-radius:22px;padding:26px;display:flex;flex-direction:column}
.pcard .h{display:flex;align-items:center;gap:12px}.pcard .h svg{border-radius:12px}
.pcard b{font-size:21px;font-weight:600;letter-spacing:-.02em}
.pcard p{color:var(--soft);margin-top:10px;flex:1}
.pcard .btn{align-self:flex-start}
@media (max-width:820px){.cards{grid-template-columns:1fr}}
.people{padding:100px 0;text-align:center;background:var(--gray)}
.people h2{font-size:clamp(32px,4.6vw,52px);font-weight:700;letter-spacing:-.035em;line-height:1.08}
.people .sub{font-size:20px;color:var(--soft);margin-top:10px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:900px;margin:44px auto 0;text-align:left}
.tile{background:#fff;border:1px solid #E4E5EA;border-radius:18px;padding:22px}
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
  var hd = document.querySelector("header"), first = document.getElementById("test");
  function bar() { hd.classList.toggle("hid", first.getBoundingClientRect().top > innerHeight * .55); }
  addEventListener("scroll", bar, { passive: true }); addEventListener("resize", bar); bar();
  // smooth scrolling: a section's animations run only while it's on screen
  if ("IntersectionObserver" in window) {
    var ao = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle("aoff", !e.isIntersecting); }); }, { rootMargin: "150px 0px" });
    document.querySelectorAll("main > section, main article").forEach(function (s) { ao.observe(s); });
  }
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
<title>From stuck to hired in 11 weeks: Riya's story</title>
<meta name="description" content="Riya is 25, skilled but stuck. Follow her 11 weeks from unsure and inconsistent to skilled, organised and hired.">
<link rel="canonical" href="https://harshvittori.github.io/story/">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:type" content="article">
<meta property="og:title" content="Everyone's moving ahead except you? Meet Riya.">
<meta property="og:description" content="Riya felt stuck too. A 3-minute story of how she turned it around.">
<meta property="og:url" content="https://harshvittori.github.io/story/"><meta property="og:image" content="https://harshvittori.github.io/story/og.jpg?v=4">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Everyone's moving ahead. Except you? Riya looks worried; messages from Mom (Tera kab hoga?) and a friend (Got the job!).">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Everyone's moving ahead except you? Meet Riya.">
<meta name="twitter:description" content="Riya felt stuck too. A 3-minute story of how she turned it around.">
<meta name="twitter:image" content="https://harshvittori.github.io/story/og.jpg?v=4">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"HV World","url":"https://harshvittori.github.io/"}</script>
<style>__CSS__</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hid"><div class="wrap nav"><a class="brand" href="/">__LOGO_NAV__HV World</a>
<nav aria-label="Main"><a class="opt" href="/">Home</a><a href="/test/"><span class="d">HV </span>Test</a><a href="/reset/"><span class="d">HV </span>Reset</a><a href="/vault/"><span class="d">HV </span>Vault</a><a class="ic" aria-label="Watch" href="/watch/"><svg class="ni" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 8.3v7.4l6-3.7z" fill="currentColor"/></svg><span class="nt">Watch</span></a><a class="ic" aria-current="page" aria-label="Riya's story" href="/story/"><svg class="ni" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.5C10 5 7 4.5 3.5 5v13c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5z"/><path d="M12 6.5v13"/></svg><span class="nt"><span class="d">Riya's </span>Story</span></a></nav></div></header>
<main id="main">
  <section id="top"><div class="wrap hero">
    <div class="rv">
      <p class="eyebrow">An 11-week story</p>
      <h1>This is Riya. She's 25.</h1>
      <p class="lead">Jaipur. B.Tech. Two years since graduation, and still no job. Three certificates on her resume, but she fails the companies' skill tests and goes blank when they ask about her strengths. <b>Comfortable at home, and quietly stuck. What now?</b></p>
      <div class="worries"><span><i style="background:#127A4F"></i>What am I actually good at?</span><span><i style="background:#4A72C8"></i>Why can't I stay consistent?</span><span><i style="background:#A87A22"></i>Where did my applications go?</span></div>
      <p class="scroll-hint" aria-hidden="true">Scroll to read __ARROW__</p>
    </div>
    <div class="art-box rv">__PROLOGUE__</div>
  </div></section>
  <section class="before"><div class="wrap">
    <p class="label rv">Riya, before</p>
    <div class="stats rv"><div><b>2</b><span>years since graduation, still no job</span></div><div><b>3</b><span>certificates on her resume</span></div><div><b>5</b><span>company skill tests failed</span></div><div><b>0</b><span>idea what her real strengths are</span></div></div>
    <p class="note rv">Sound familiar? This is her story: the bad nights, the restarts, and what finally changed.</p>
  </div></section>
  <section class="cast"><div class="wrap">
    <p class="label rv">The people in her story</p>
    <h2 class="rv">Nobody's journey is solo.</h2>
    <p class="sub rv">The ones who worry, push, ignore, test and finally say yes.</p>
  </div><div class="crow">__CAST__</div></section>
  __CHAPTERS__
  __CALL__
  <section class="journey"><div class="wrap">
    <p class="label rv">Her 11 weeks</p>
    <h2 class="rv">Not overnight. Not magic.</h2>
    <p class="sub rv">Good weeks, bad weeks, and one simple system she kept coming back to.</p>
    <ol class="tl">__TIMELINE__</ol>
  </div></section>
  <section class="lessons"><div class="wrap">
    <p class="label rv">What Riya would tell you</p>
    <h2 class="rv">Four things that actually worked.</h2>
    <div class="lgrid">__LESSONS__</div>
    <p class="yourturn rv">Your turn. Start where she did, with step 1: an honest look at where you stand.</p>
  </div></section>
  <section class="key" id="key"><div class="wrap">
    <p class="label rv">The whole point</p>
    <h2 class="rv">Consistency is the key.</h2>
    <p class="sub rv">Riya didn't get lucky. She followed three steps, in order, and kept going through the bad weeks. That's what made the difference. Just don't skip a step.</p>
    <div class="eq rv">
      <div class="term" style="--c:#127A4F"><em>Right direction</em><b>Know where you stand</b><span>An honest self-assessment and a clear 30-day plan.</span></div><i>+</i>
      <div class="term" style="--c:#4A72C8"><em>Consistency</em><b>Show up daily</b><span>One or two important tasks every day, even after a bad week.</span></div><i>+</i>
      <div class="term" style="--c:#A87A22"><em>A system</em><b>Track every chance</b><span>One place for every application, and follow-ups on time.</span></div><i>=</i>
      <div class="term goal"><em>The result</em><b>Your goal</b><span>Not overnight. But it comes.</span></div>
    </div>
    <p class="order rv">Each step builds on the one before. Skills without direction go nowhere. Applications without skills go unanswered. Skip one, and the next one gets harder.</p>
  </div></section>
  <section class="finale" id="products"><div class="wrap">
    <p class="label rv">What Riya used</p>
    <h2 class="rv">The free tools behind her three steps.</h2>
    <p class="sub rv">One for each step. The steps are what changed her story: know where you stand, show up daily, apply with a system. Then go again for the next goal.</p>
    <div class="art-box rv">__FINALE__</div>
    <div class="cards">
      <div class="pcard rv"><div class="h">__L_TEST__<b>HV Test</b></div><p>For step 1. Free tests for your traits, thinking and skills, with a report and a 30-day plan.</p><div class="pacts"><a class="btn" href="https://harshvittori.github.io/hv-tests/">Open HV Test</a><a class="lm" href="/test/">Learn more</a></div></div>
      <div class="pcard rv"><div class="h">__L_RESET__<b>HV Reset</b></div><p>For step 2. Tell HV AI your day, do one task at a time, and see your progress.</p><div class="pacts"><a class="btn" href="https://harshvittori.github.io/hv-reset/">Open HV Reset</a><a class="lm" href="/reset/">Learn more</a></div></div>
      <div class="pcard rv"><div class="h">__L_VAULT__<b>HV Vault</b></div><p>For step 3. One board for every application, with follow-up reminders.</p><div class="pacts"><a class="btn" href="https://harshvittori.github.io/hv-vault-web/">Open HV Vault</a><a class="lm" href="/vault/">Learn more</a></div></div>
    </div>
    <p class="more rv"><a href="/">See every feature, HV AI, privacy and FAQ →</a></p>
  </div></section>
  <section class="next" id="you"><div class="wrap ngrid">
    <div class="nart rv">__NEXT_ART__</div>
    <div class="ntxt">
      <p class="label rv">Your turn</p>
      <h2 class="rv">You could be the next Riya.</h2>
      <p class="sub rv">Different city, different dream, same feeling of being stuck. Her 11 weeks started with one small step. Yours can start today.</p>
      <ol class="nsteps rv">
        <li><span style="background:#127A4F">1</span><div><b>Know where you stand</b><em>Test your strengths and your skills honestly, and write down what to fix. Riya used HV Test, free.</em></div></li>
        <li><span style="background:#4A72C8">2</span><div><b>Plan just today</b><em>Give one or two important tasks a fixed start time, and start when the time comes. Riya used HV Reset, free.</em></div></li>
        <li><span style="background:#A87A22">3</span><div><b>Track every chance</b><em>Keep every application in one place and follow up on time. Riya used HV Vault, free.</em></div></li>
      </ol>
      <div class="ncta rv"><a class="btn" href="#test">Go through the steps again</a><a class="btn ghost" href="#products">See the tools Riya used</a></div>
      <p class="nfor rv">Every step matters. For students, job seekers, professionals, freelancers, career switchers, and anyone starting again.</p>
    </div>
  </div></section>
</main>
<footer><div class="wrap row"><span>© <span id="yr">2026</span> HV World · Built by Harsh Goyal</span>
<nav aria-label="Footer"><a href="/">All features</a><a href="/watch/">Watch</a><a href="/test/">About HV Test</a><a href="/reset/">About HV Reset</a><a href="/vault/">About HV Vault</a><a href="https://harshvittori.github.io/hv-tests/">HV Test</a><a href="https://harshvittori.github.io/hv-reset/">HV Reset</a><a href="https://harshvittori.github.io/hv-vault-web/">HV Vault</a><a href="https://www.linkedin.com/in/harshvittori" target="_blank" rel="noopener">LinkedIn</a><a href="https://github.com/harshvittori" target="_blank" rel="noopener">GitHub</a></nav></div></footer>
<script>__JS__</script>
</body>
</html>
"""

def build():
    html = (PAGE.replace("__CSS__", CSS).replace("__JS__", JS).replace("__ARROW__", ARROW)
            .replace("__LOGO_NAV__", logo("world")).replace("__PROLOGUE__", prologue()).replace("__CHAPTERS__", "\n".join(CH))
            .replace("__FINALE__", finale()).replace("__NEXT_ART__", next_art()).replace("__CAST__", cast()).replace("__TIMELINE__", timeline()).replace("__CALL__", interlude("call")).replace("__LESSONS__", lessons()).replace("__L_TEST__", logo("test", size=44)).replace("__L_RESET__", logo("reset", size=44)).replace("__L_VAULT__", logo("vault", size=44)))
    assert "__" not in re.sub(r"<script>.*?</script>", "", html, flags=re.S).replace("__proto__", ""), "unfilled placeholder"
    os.makedirs(os.path.join(OUT, "story"), exist_ok=True)
    html = html.replace("</style>", transitions.CSS + "</style>", 1).replace("</head>", transitions.HEAD + "\n</head>", 1)
    open(os.path.join(OUT, "story", "index.html"), "w").write(app_links_new_tab(html))
    open(os.path.join(OUT, "favicon.svg"), "w").write(read("world.svg") + "\n")
    print("ok", len(html), "bytes")

if __name__ == "__main__":
    build()
