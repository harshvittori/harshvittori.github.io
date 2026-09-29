"""HV World: the people in Riya's story, drawn full length as inline SVG.

One figure() builds anyone from a small description (skin, hair, clothes, pose, extras). Proportions are
about seven heads tall, with soft shading and no outlines, so they read as calm editorial illustrations.
Local frame: head centre (0,-94), shoulders y≈-44, hips y≈92, feet y≈342. head() gives an avatar crop."""

INK = "#1D1D1F"
DARK = "#2A1C18"


def _shade(c, k):
    """Darken (k<0) or lighten (k>0) a #RRGGBB colour."""
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    f = (lambda v: int(v + (255 - v) * k)) if k > 0 else (lambda v: int(v * (1 + k)))
    return "#%02X%02X%02X" % tuple(max(0, min(255, f(v))) for v in (r, g, b))


# ---------------------------------------------------------------- hair
def _hair_back(st, col):
    return {
        "long": '<path d="M-35,-112 C-48,-158 48,-158 35,-112 C42,-92 46,-64 44,-40 C46,-30 40,-24 34,-26 C20,-30 -20,-30 -34,-26 C-40,-24 -46,-30 -44,-40 C-46,-64 -42,-92 -35,-112Z" fill="%s"/>' % col,
        "bun": '<circle cx="0" cy="-134" r="15" fill="%s"/><path d="M-32,-104 C-34,-146 34,-146 32,-104 L30,-82 C20,-76 -20,-76 -30,-82Z" fill="%s"/>' % (col, col),
        "curly": "".join('<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (x, y, r, col) for x, y, r in
                         [(-30, -128, 18), (0, -140, 20), (30, -128, 18), (-40, -104, 16), (40, -104, 16), (-42, -80, 15), (42, -80, 15), (-38, -58, 13), (38, -58, 13)]),
        "short": '<path d="M-31,-104 C-33,-142 33,-142 31,-104 L30,-92 C22,-96 -22,-96 -30,-92Z" fill="%s"/>' % col,
        "pony": '<path d="M-32,-104 C-34,-146 34,-146 32,-104 L30,-90 C20,-86 -20,-86 -30,-90Z" fill="%s"/><path d="M22,-126 C46,-118 50,-86 44,-52 C42,-40 34,-36 30,-44 C38,-70 36,-98 20,-114Z" fill="%s"/>' % (col, col),
        "bob": '<path d="M-36,-110 C-46,-152 46,-152 36,-110 C40,-92 42,-76 40,-64 C30,-58 -30,-58 -40,-64 C-42,-76 -40,-92 -36,-110Z" fill="%s"/>' % col,
    }[st]


def _hair_front(st, col, shine):
    sh = '<path d="M-14,-136 C-4,-141 10,-141 18,-136" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round" opacity=".7"/>' % shine
    return {
        "long": '<path d="M-31,-100 C-36,-136 -4,-146 18,-139 C35,-132 38,-113 31,-95 C27,-111 17,-121 1,-123 C-11,-117 -22,-110 -31,-100Z" fill="%s"/>'
                '<path d="M-30,-106 C-37,-86 -36,-66 -41,-44 L-33,-44 C-30,-64 -28,-86 -26,-102Z" fill="%s"/><path d="M31,-100 C36,-84 36,-66 41,-46 L33,-46 C30,-64 29,-84 28,-98Z" fill="%s"/>' % (col, col, col) + sh,
        "bun": '<path d="M-30,-102 C-31,-134 31,-134 30,-102 C26,-116 8,-122 0,-122 C-8,-122 -26,-116 -30,-102Z" fill="%s"/><path d="M0,-129 V-121" stroke="%s" stroke-width="1.6" opacity=".6"/>'
               '<path d="M-22,-114 C-14,-120 -6,-122 0,-122" fill="none" stroke="#B9B2AE" stroke-width="2" stroke-linecap="round" opacity=".85"/>' % (col, _shade(col, .25)),
        "curly": "".join('<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (x, y, r, col) for x, y, r in [(-24, -122, 11), (-10, -128, 11), (6, -128, 11), (20, -122, 11), (-30, -108, 8), (30, -108, 8)]),
        "short": '<path d="M-31,-100 C-34,-138 30,-146 32,-104 C30,-114 18,-122 4,-121 C-8,-120 -22,-114 -31,-100Z" fill="%s"/><rect x="-32" y="-104" width="4" height="12" rx="2" fill="%s"/><rect x="28" y="-104" width="4" height="12" rx="2" fill="%s"/>' % (col, col, col),
        "pony": '<path d="M-31,-102 C-33,-136 -2,-142 20,-136 C33,-130 34,-114 31,-102 C24,-116 10,-122 -8,-120 C-18,-116 -26,-110 -31,-102Z" fill="%s"/>' % col,
        "bob": '<path d="M-33,-98 C-38,-138 6,-148 26,-134 C36,-126 37,-110 34,-96 C28,-112 12,-120 -6,-118 C-18,-114 -28,-106 -33,-98Z" fill="%s"/>'
               '<path d="M-33,-104 C-37,-86 -36,-72 -38,-64 L-31,-64 C-30,-76 -29,-90 -28,-100Z" fill="%s"/><path d="M33,-100 C37,-84 37,-72 38,-64 L31,-64 C30,-76 30,-88 29,-98Z" fill="%s"/>' % (col, col, col) + sh,
    }[st]


# ---------------------------------------------------------------- face
def _face(p):
    sk, sd, g, ex, x = p["skin"], _shade(p["skin"], -.14), p.get("gender", "f"), p.get("expr", "n"), set(p.get("extras", []))
    hair = p["hair"]
    o = ['<circle cx="-30" cy="-92" r="5.5" fill="%s"/><circle cx="30" cy="-92" r="5.5" fill="%s"/>' % (sk, sk)]
    if g == "m":
        o.append('<path d="M-30,-106 C-30,-130 30,-130 30,-106 C30,-80 20,-60 0,-58 C-20,-60 -30,-80 -30,-106Z" fill="%s"/>' % sk)
    else:
        o.append('<path d="M-29,-104 C-29,-129 29,-129 29,-104 C29,-80 17,-60 0,-58 C-17,-60 -29,-80 -29,-104Z" fill="%s"/>' % sk)
    if "stubble" in x:
        o.append('<path d="M-26,-84 C-22,-64 -10,-58 0,-58 C10,-58 22,-64 26,-84 C20,-72 12,-66 0,-66 C-12,-66 -20,-72 -26,-84Z" fill="%s" opacity=".35"/>' % hair)
    if "beard" in x:
        o.append('<path d="M-27,-88 C-24,-62 -12,-54 0,-54 C12,-54 24,-62 27,-88 C22,-76 14,-68 0,-68 C-14,-68 -22,-76 -27,-88Z" fill="%s"/>' % hair)
        o.append('<path d="M-9,-76 Q0,-80 9,-76 Q0,-73 -9,-76Z" fill="%s"/>' % hair)
    o.append('<path d="M-1,-88 Q2.6,-80 -1.6,-77.5" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % sd)
    bw = 3.4 if g == "m" else 2.6
    o.append('<path d="M-17,-103 Q-11,-106 -5,-104 M5,-104 Q11,-106 17,-103" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round"/>' % (hair if hair not in ("#D9D4CF", "#BDB6B0") else "#8B8580", bw))
    if ex == "h":
        o.append('<path d="M-16,-92 Q-11,-97 -6,-92 M6,-92 Q11,-97 16,-92" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % DARK)
    else:
        for ex_ in (-11, 11):
            o.append('<ellipse cx="%g" cy="-93" rx="3.4" ry="4" fill="%s"/><circle cx="%g" cy="-94.5" r="1.1" fill="#FFFFFF"/>' % (ex_, DARK, ex_ + 1.1))
            if g == "f":
                o.append('<path d="M%g,-97.3 Q%g,-100 %g,-97.3" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % (ex_ - 5, ex_, ex_ + 5, DARK))
    if "age" in x:
        o.append('<path d="M-19,-84 Q-17,-80 -15,-78 M19,-84 Q17,-80 15,-78" fill="none" stroke="%s" stroke-width="1.3" stroke-linecap="round"/>' % sd)
    lip = "#A24F57" if g == "f" else _shade(sk, -.3)
    if ex == "h":
        o.append('<path d="M-9,-73 Q0,-61 9,-73Z" fill="#7E2F38"/><path d="M-7.6,-72.5 Q0,-70.6 7.6,-72.5 L6.6,-70.2 Q0,-68.6 -6.6,-70.2Z" fill="#FFFFFF"/>')
    else:
        o.append('<path d="M-7,-71 Q0,-66 7,-71" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % lip)
    if g == "f":
        o.append('<circle cx="-19" cy="-80" r="5" fill="#E8826F" opacity=".22"/><circle cx="19" cy="-80" r="5" fill="#E8826F" opacity=".22"/>')
    if "bindi" in x:
        o.append('<circle cx="0" cy="-109" r="2.2" fill="#C0303C"/>')
    if "earrings" in x:
        o.append('<circle cx="-30" cy="-84" r="2.6" fill="#E3AE45"/><circle cx="30" cy="-84" r="2.6" fill="#E3AE45"/>')
    if "jhumka" in x:
        o.append('<path d="M-33,-86 h6 l-1,6 h-4Z M27,-86 h6 l-1,6 h-4Z" fill="#E3AE45"/>')
    return "".join(o)


def _glasses():
    return ('<g fill="none" stroke="#3A3330" stroke-width="2"><rect x="-19" y="-99" width="15" height="12" rx="4"/><rect x="4" y="-99" width="15" height="12" rx="4"/>'
            '<path d="M-4,-94 Q0,-96 4,-94 M-19,-94 L-28,-96 M19,-94 L28,-96"/></g>')


# ---------------------------------------------------------------- body
def _legs(p):
    b, col, shoe = p["bottom"], p["bottom_col"], p.get("shoes", "#2B2B30")
    dk = _shade(col, -.12)
    o = []
    if b in ("trousers", "jeans"):
        o.append('<path d="M-38,88 L-34,334 H-12 L-4,120 L4,120 L12,334 H34 L38,88Z" fill="%s"/>' % col)
        o.append('<path d="M4,120 L12,334 H34 L38,88 L20,88 Z" fill="%s" opacity=".55"/>' % dk)
        if b == "jeans":
            o.append('<path d="M-30,96 Q-20,104 -14,98 M30,96 Q20,104 14,98" fill="none" stroke="%s" stroke-width="1.6" opacity=".6"/>' % _shade(col, .3))
        o.append('<path d="M-6,120 L-4,120 L4,120" fill="none"/>')
    elif b == "churidar":
        o.append('<path d="M-30,190 L-26,334 H-10 L-4,200 L4,200 L10,334 H26 L30,190Z" fill="%s"/>' % col)
        o.append(''.join('<path d="M%d,%d q8,3 16,0" fill="none" stroke="%s" stroke-width="1.4" opacity=".5"/>' % (x, y, dk) for x in (-26, 10) for y in (300, 310, 320)))
    elif b == "skirt":
        o.append('<path d="M-40,88 L-52,260 H52 L40,88Z" fill="%s"/><path d="M8,88 L14,260 H52 L40,88Z" fill="%s" opacity=".5"/>' % (col, dk))
        o.append('<rect x="-24" y="258" width="14" height="76" rx="6" fill="%s"/><rect x="10" y="258" width="14" height="76" rx="6" fill="%s"/>' % (p["skin"], _shade(p["skin"], -.08)))
    o.append('<path d="M-36,332 H-8 C-6,340 -10,344 -16,344 H-38 C-42,344 -42,336 -36,332Z" fill="%s"/><path d="M8,332 H36 C42,336 42,344 38,344 H16 C10,344 6,340 8,332Z" fill="%s"/>' % (shoe, shoe))
    return "".join(o)


def _top(p):
    t, col, acc = p["top"], p["top_col"], p.get("accent", "#F6EFE6")
    dk = _shade(col, -.14)
    body = 'M-44,-40 C-52,-30 -52,0 -46,40 L-42,96 H42 L46,40 C52,0 52,-30 44,-40 C30,-50 -30,-50 -44,-40Z'
    o = []
    if t == "blazer":
        o.append('<path d="M-17,-47 Q0,-40 17,-47 L12,96 H-12Z" fill="%s"/>' % acc)
        for m in (1, -1):
            o.append('<path d="M%g,-40 C%g,-30 %g,0 %g,40 L%g,98 L%g,98 L%g,-4 L%g,-47 C%g,-48 %g,-44 %g,-40Z" fill="%s"/>' % (
                -44 * m, -52 * m, -52 * m, -46 * m, -42 * m, -4 * m, -5 * m, -17 * m, -30 * m, -40 * m, -44 * m, col))
            o.append('<path d="M%g,-47 L%g,-30 L%g,-24 L%g,-4" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (-17 * m, -27 * m, -15 * m, -5 * m, _shade(col, .18)))
        o.append('<path d="M4,-4 L4,98 L42,98 L46,40 C52,0 52,-30 44,-40 C36,-44 26,-46 17,-47Z" fill="#000" opacity=".08"/>')
        o.append('<circle cx="-7" cy="22" r="2.2" fill="%s"/><circle cx="-7" cy="48" r="2.2" fill="%s"/>' % (dk, dk))
    elif t == "shirt":
        o.append('<path d="%s" fill="%s"/><path d="M0,-44 V96" stroke="%s" stroke-width="1.6"/>' % (body, col, dk))
        o.append("".join('<circle cx="3" cy="%d" r="1.6" fill="%s"/>' % (y, dk) for y in (-20, 10, 40, 70)))
        o.append('<path d="M-18,-48 L-2,-36 L-8,-26Z M18,-48 L2,-36 L8,-26Z" fill="%s"/>' % _shade(col, .25))
        o.append('<path d="M6,-44 L42,96 L46,40 C52,0 52,-30 44,-40Z" fill="#000" opacity=".07"/>')
        o.append('<rect x="-44" y="88" width="88" height="10" rx="3" fill="#3A3330"/><rect x="-5" y="87" width="10" height="12" rx="2" fill="#C9B27A"/>')
    elif t == "hoodie":
        o.append('<path d="M-30,-52 C-30,-30 30,-30 30,-52 C22,-40 -22,-40 -30,-52Z" fill="%s"/>' % dk)
        o.append('<path d="%s" fill="%s"/>' % (body.replace("L-42,96 H42", "L-44,100 H44"), col))
        o.append('<path d="M-6,-40 V-4 M6,-40 V-4" stroke="#F4F4F4" stroke-width="2" stroke-linecap="round"/>')
        o.append('<path d="M-26,50 H26 L22,80 H-22Z" fill="%s" opacity=".7"/>' % dk)
        o.append('<path d="M6,-44 L44,100 L46,40 C52,0 52,-30 44,-40Z" fill="#000" opacity=".07"/>')
    elif t == "kurta":
        o.append('<path d="M-44,-40 C-52,-30 -52,0 -48,40 L-54,196 H54 L48,40 C52,0 52,-30 44,-40 C30,-50 -30,-50 -44,-40Z" fill="%s"/>' % col)
        o.append('<path d="M-14,-46 Q0,-30 14,-46" fill="none" stroke="%s" stroke-width="3"/>' % acc)
        o.append("".join('<circle cx="%g" cy="%g" r="1.8" fill="%s"/>' % (x, y, acc) for x, y in [(-10, -34), (10, -34), (0, -24), (-5, -12), (5, -12), (0, 0)]))
        o.append('<path d="M-54,188 H54" stroke="%s" stroke-width="4"/>' % acc)
        o.append('<path d="M8,-44 L54,196 L48,40 C52,0 52,-30 44,-40Z" fill="#000" opacity=".08"/>')
    elif t == "cardigan":
        o.append('<path d="M-17,-47 Q0,-36 17,-47 L14,96 H-14Z" fill="%s"/>' % acc)
        for m in (1, -1):
            o.append('<path d="M%g,-40 C%g,-30 %g,0 %g,40 L%g,98 L%g,98 L%g,-47 C%g,-48 %g,-44 %g,-40Z" fill="%s"/>' % (
                -44 * m, -52 * m, -52 * m, -46 * m, -42 * m, -12 * m, -17 * m, -30 * m, -40 * m, -44 * m, col))
        o.append('<path d="M12,98 L42,98 L46,40 C52,0 52,-30 44,-40 C36,-44 26,-46 17,-47Z" fill="#000" opacity=".08"/>')
    if "lanyard" in p.get("extras", []):
        o.append('<path d="M-14,-46 L-4,20 M14,-46 L4,20" stroke="%s" stroke-width="3"/><rect x="-10" y="18" width="20" height="26" rx="3" fill="#FFFFFF"/><rect x="-6" y="24" width="12" height="4" rx="2" fill="%s"/>' % (p.get("lanyard", "#2E43A6"), p.get("lanyard", "#2E43A6")))
    if "chain" in p.get("extras", []):
        o.append('<path d="M-8,-44 Q0,-35 8,-44" fill="none" stroke="#E3AE45" stroke-width="1.6"/><circle cx="0" cy="-36.5" r="2" fill="#E3AE45"/>')
    if "dupatta" in p.get("extras", []):
        o.append('<path d="M20,-46 C8,-10 -20,30 -46,70 L-40,86 C-14,48 14,10 34,-40Z" fill="%s" opacity=".92"/>' % p.get("dupatta_col", "#E8B04A"))
        o.append('<path d="M34,-40 C44,20 46,90 44,150 L34,150 C36,90 34,30 26,-42Z" fill="%s" opacity=".92"/>' % p.get("dupatta_col", "#E8B04A"))
    return "".join(o)


def _arm(x0, y0, pts, sleeve, skin, w=17, fore=None, hand=True):
    """A two-part arm: shoulder → elbow in the sleeve colour, elbow → wrist in `fore` (sleeve or skin)."""
    (ex, ey), (wx, wy) = pts
    fore = fore or sleeve
    s = '<path d="M%g,%g L%g,%g" stroke="%s" stroke-width="%g" stroke-linecap="round"/>' % (x0, y0, ex, ey, sleeve, w)
    s += '<path d="M%g,%g L%g,%g" stroke="%s" stroke-width="%g" stroke-linecap="round"/>' % (ex, ey, wx, wy, fore, w - 3)
    if hand:
        s += '<ellipse cx="%g" cy="%g" rx="7.5" ry="8.5" fill="%s"/>' % (wx, wy + 5, skin)
    return s


def _arms(p):
    sl, sk, pose = p.get("sleeve", p["top_col"]), p["skin"], p.get("pose", "down")
    fore = sk if p.get("rolled") else None
    o = []
    L = lambda pts, hand=True: _arm(-44, -34, pts, sl, sk, fore=fore, hand=hand)
    R = lambda pts, hand=True: _arm(44, -34, pts, sl, sk, fore=fore, hand=hand)
    held = p.get("held", "")
    if pose == "down":
        o += [L([(-52, 40), (-50, 104)]), R([(52, 40), (50, 104)])]
    elif pose == "clasp":
        o += [L([(-52, 36), (-8, 62)]), R([(52, 36), (8, 62)])]
    elif pose == "hold":          # right forearm up, something held at chest
        o += [L([(-52, 40), (-50, 104)]), R([(54, 34), (22, 2)], hand=False)]
        o.append(held)
        o.append('<ellipse cx="22" cy="6" rx="7.5" ry="8.5" fill="%s"/>' % sk)
    elif pose == "hug":           # both forearms across the chest, holding a book or tablet
        o.append(R([(54, 36), (18, 20)], hand=False))
        o.append(held)
        o.append(L([(-54, 36), (-14, 24)]) + '<ellipse cx="18" cy="24" rx="7.5" ry="8.5" fill="%s"/>' % sk)
    return "".join(o)


def figure(p, x=0, y=0, s=1.0, cls=""):
    o = ['<ellipse cx="0" cy="346" rx="58" ry="8" fill="#000" opacity=".08"/>']
    o.append(_hair_back(p["hairstyle"], p["hair"]))
    o.append(_legs(p))
    o.append('<rect x="-9" y="-66" width="18" height="26" rx="7" fill="%s"/><path d="M-9,-60 Q0,-53 9,-60 V-50 Q0,-45 -9,-50Z" fill="%s" opacity=".55"/>' % (p["skin"], _shade(p["skin"], -.14)))
    o.append(_top(p))
    o.append(_face(p))
    o.append(_hair_front(p["hairstyle"], p["hair"], p.get("shine", _shade(p["hair"], .2))))
    if "glasses" in p.get("extras", []):
        o.append(_glasses())
    if "bag" in p.get("extras", []):
        o.append('<path d="M-30,-44 L-56,70" stroke="#8A5A3C" stroke-width="4"/><path d="M-72,60 H-40 L-38,110 H-74Z" fill="#A86E4A"/><path d="M-72,60 H-40 L-40,70 H-72Z" fill="#8A5A3C"/>')
    o.append(_arms(p))
    if "watch" in p.get("extras", []):
        o.append('<rect x="-56" y="92" width="12" height="7" rx="2" fill="#3A3330"/>')
    return '<g class="%s" transform="translate(%g %g) scale(%g)">%s</g>' % (cls, x, y, s, "".join(o))


def head(p, size=34, bg=None):
    """An avatar: the figure cropped to head and shoulders."""
    q = dict(p, pose="down", extras=[e for e in p.get("extras", []) if e not in ("bag", "lanyard", "dupatta")])
    return ('<svg viewBox="-54 -150 108 108" width="%d" height="%d" aria-hidden="true" focusable="false"><rect x="-54" y="-150" width="108" height="108" fill="%s"/>%s</svg>' % (
        size, size, bg or _shade(p["top_col"], .75), figure(q)))


# ---------------------------------------------------------------- the cast
PHONE = '<rect x="10" y="-26" width="22" height="36" rx="4" fill="%s"/><rect x="13" y="-22" width="16" height="26" rx="2" fill="#8FA6FF"/>' % INK
CUP = '<path d="M8,-18 h26 l-3,30 h-20Z" fill="#FFFFFF"/><rect x="7" y="-22" width="28" height="6" rx="3" fill="#6B4A3A"/><rect x="11" y="-6" width="20" height="8" fill="#C9A27E"/>'
BOOK = '<rect x="-24" y="-8" width="56" height="42" rx="4" fill="#7C4D8C"/><rect x="-20" y="-4" width="48" height="34" rx="2" fill="#9A67AA"/><rect x="-12" y="6" width="30" height="4" rx="2" fill="#F1E6F4"/>'
TABLET = '<rect x="-24" y="-10" width="54" height="40" rx="6" fill="#2B2B30"/><rect x="-20" y="-6" width="46" height="32" rx="3" fill="#DDE6FF"/>'
FOLDER = '<rect x="4" y="-16" width="36" height="46" rx="3" fill="#E8C98A"/><rect x="8" y="-10" width="28" height="3" rx="1.5" fill="#B99A5C"/>'

CAST = {
    "riya": dict(name="Riya", role="25 · a fresher, 2025 batch", line="B.Com, MBA, three certificates. Keeps failing tests and interviews.",
                 skin="#D9A07A", hair="#231715", hairstyle="long", top="blazer", top_col="#2F3B6E", accent="#F6EFE6", bottom="trousers", bottom_col="#3B3F4A",
                 shoes="#E8DCCB", extras=["earrings", "chain", "bag"], pose="down"),
    "mom": dict(name="Mom", role="her biggest fan, and her biggest worry", line="Asks &ldquo;tera kab hoga?&rdquo; every week. Means it with love.",
                skin="#C98E68", hair="#3A2A26", hairstyle="bun", top="kurta", top_col="#8E2F45", accent="#E8B04A", bottom="churidar", bottom_col="#F1E4CF",
                shoes="#8A5A3C", extras=["bindi", "jhumka", "age", "glasses", "dupatta"], dupatta_col="#E8B04A", pose="clasp"),
    "ananya": dict(name="Ananya", role="her batchmate, already at a startup", line="Posts her new job on LinkedIn. Weeks later, she sends Riya the opening that changes everything.",
                   skin="#E2B08D", hair="#3B2518", hairstyle="curly", top="hoodie", top_col="#E27D60", bottom="jeans", bottom_col="#46628F", shoes="#F4F4F4",
                   extras=["lanyard", "earrings"], lanyard="#1F8A70", pose="hold", held=CUP),
    "neha": dict(name="Neha ma'am", role="her old college teacher", line="Runs a mock interview with Riya: &ldquo;Now I believe you.&rdquo;",
                 skin="#C4876A", hair="#2E2522", hairstyle="bob", top="cardigan", top_col="#5E7F6E", accent="#F3EDE3", bottom="skirt", bottom_col="#3F4756", shoes="#5A3E30",
                 extras=["glasses", "age", "earrings"], pose="hug", held=BOOK),
    "rohit": dict(name="Rohit", role="a recruiter who goes quiet", line="&ldquo;Will get back to you by Friday 👍&rdquo; Twelve days later: nothing.",
                  skin="#B97D58", hair="#1E1716", hairstyle="short", gender="m", top="shirt", top_col="#BFD4EA", bottom="trousers", bottom_col="#2F3440", shoes="#3A2A22",
                  extras=["stubble", "lanyard", "watch"], lanyard="#C0392B", rolled=True, pose="hold", held=PHONE),
    "mehta": dict(name="Mr. Mehta", role="the interviewer", line="Asks about her strengths, then for one quick SQL query. She freezes on both.",
                  skin="#C28A66", hair="#6E6661", hairstyle="short", gender="m", top="blazer", top_col="#3A4150", accent="#DCE3F0", bottom="trousers", bottom_col="#2C3038",
                  shoes="#1F1B1A", extras=["glasses", "beard", "age"], pose="hold", held=FOLDER),
    "kavya": dict(name="Kavya", role="HR at the company that hires her", line="Makes the call on a Thursday at 4:12 PM. Riya almost doesn't pick up.",
                  skin="#D8A27E", hair="#2A1B17", hairstyle="pony", top="blazer", top_col="#7A4E8E", accent="#FFFFFF", bottom="trousers", bottom_col="#2F2A36", shoes="#2F2A36",
                  extras=["earrings", "chain"], pose="hug", held=TABLET),
}
