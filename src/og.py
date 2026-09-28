"""Link-preview (Open Graph) cards for every page, in the HV Test card style.
Writes src/og-cards.html (five 1200x630 cards). Render them to PNG with src/og-render.js (Playwright):
  python3 src/og.py && node src/og-render.js
"""
import os, re, base64
HERE = os.path.dirname(os.path.abspath(__file__))

def svg(name, size, rot=0, shadow=True):
    s = open(os.path.join(HERE, name + ".svg")).read().strip()
    tag = name.replace("-", "")
    for i in re.findall(r'id="([^"]+)"', s):
        s = s.replace('id="%s"' % i, 'id="%s-%s%d"' % (i, tag, size)).replace("url(#%s)" % i, "url(#%s-%s%d)" % (i, tag, size))
    st = "width:%dpx;height:%dpx;border-radius:%dpx;transform:rotate(%sdeg);%s" % (size, size, size * .24, rot, "box-shadow:0 30px 60px -24px rgba(20,30,60,.45)" if shadow else "")
    return s.replace("<svg ", '<svg style="%s" ' % st, 1)

def font(w):
    b = base64.b64encode(open(os.path.join(HERE, "fonts", "outfit-latin-%d-normal.woff2" % w), "rb").read()).decode()
    return "@font-face{font-family:Outfit;font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2')}" % (w, b)

# out path, brand logo, brand word (accent part), accent, dark accent, tint, circle, eyebrow, headline, sub, chips, right-side art
WORLD_ART = ('<div class="cluster">' + svg("world-orbit", 230, -6) +
             '<span class="a1">' + svg("logo-test", 92, 8) + '</span><span class="a2">' + svg("logo-reset", 92, -8) + '</span><span class="a3">' + svg("logo-vault", 92, 6) + '</span></div>')
CARDS = [
    ("og.png", "world-orbit", "WORLD", "#2E43A6", "#233489", "#F4F5FB", "#E4E8F8", "By Harsh Vittori",
     "Your work, your day, your growth.", "Three simple apps that work together. One calm world.", ["HV Test", "HV Reset", "HV Vault"], WORLD_ART),
    ("story/og.png", "world", "WORLD", "#2E43A6", "#233489", "#F4F5FB", "#E4E8F8", "An illustrated story",
     "This is Riya.", "She works hard, but feels stuck. Follow her story, and see what changes.", ["Know", "Plan", "Act"], '<div class="big">' + svg("world", 250, -6) + '</div>'),
    ("test/og.png", "logo-test", "TEST", "#127A4F", "#0D5E3C", "#F4F8F5", "#E1F0E7", "Know yourself",
     "See how you really think.", "Real-life situations, a score out of 100, a full report and a 30-day plan.", ["About 10 min", "No login", "2 PDFs"], '<div class="big">' + svg("logo-test", 250, -6) + '</div>'),
    ("reset/og.png", "logo-reset", "RESET", "#3F66BE", "#2C4E99", "#F3F6FC", "#E1E9F8", "Plan your day",
     "A calm day, one block at a time.", "Running late? One tap and the whole plan shifts. Meals never skipped.", ["One block, one task", "Shift a late day", "HV AI"], '<div class="big">' + svg("logo-reset", 250, -6) + '</div>'),
    ("vault/og.png", "logo-vault", "VAULT", "#A0721C", "#7C5712", "#FAF7F0", "#F2E9D6", "Act on every opportunity",
     "Nothing slips anymore.", "Every job, follow-up and interview in one calm place.", ["One board", "Auto follow-ups", "AI auto-fill"], '<div class="big">' + svg("logo-vault", 250, -6) + '</div>'),
]

CSS = font(500) + font(600) + font(700) + """
*{box-sizing:border-box;margin:0}body{background:#888}
.card{position:relative;width:1200px;height:630px;overflow:hidden;font-family:Outfit,sans-serif;color:#16212B;background:var(--tint);margin-bottom:20px}
.c1{position:absolute;width:640px;height:640px;border-radius:50%;background:var(--circle);right:-120px;top:-190px}
.c2{position:absolute;width:300px;height:300px;border-radius:50%;background:var(--circle);opacity:.55;left:520px;bottom:-190px}
.left{position:absolute;left:66px;top:56px;width:640px}
.brand{display:flex;align-items:center;gap:14px;font-weight:700;font-size:34px;letter-spacing:.02em}
.brand svg{box-shadow:none!important}.brand b{color:var(--accent);font-weight:700}
.eye{margin-top:52px;font-weight:600;font-size:18px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent)}
h1{margin-top:12px;font-weight:700;font-size:68px;line-height:1.02;letter-spacing:-.01em;max-width:620px}
.rule{width:56px;height:6px;border-radius:4px;background:#F2A33A;margin:26px 0 22px}
.sub{font-weight:500;font-size:25px;line-height:1.35;color:#3D4A55;max-width:600px}
.chips{display:flex;gap:12px;margin-top:26px}
.chips span{font-weight:600;font-size:19px;color:var(--dark);background:color-mix(in srgb,var(--accent) 12%,#fff);border:1px solid color-mix(in srgb,var(--accent) 22%,#fff);padding:9px 18px;border-radius:999px;white-space:nowrap}
.big{position:absolute;right:80px;top:100px}
.cluster{position:absolute;right:70px;top:110px;width:360px;height:360px}
.cluster>svg{position:absolute;left:65px;top:65px}
.cluster span{position:absolute}.a1{left:0;top:10px}.a2{right:-10px;top:40px}.a3{left:150px;bottom:-40px}
"""
html = "<!DOCTYPE html><html><head><meta charset='utf-8'><style>%s</style></head><body>" % CSS
for out, lg, word, acc, dark, tint, circ, eye, h1, sub, chips, art in CARDS:
    html += ('<div class="card" data-out="%s" style="--accent:%s;--dark:%s;--tint:%s;--circle:%s"><div class="c1"></div><div class="c2"></div>'
             '<div class="left"><div class="brand">%sHV <b>%s</b></div><p class="eye">%s</p><h1>%s</h1><div class="rule"></div><p class="sub">%s</p>'
             '<div class="chips">%s</div></div>%s</div>') % (out, acc, dark, tint, circ, svg(lg, 50, 0, False), word, eye, h1, sub, "".join("<span>%s</span>" % c for c in chips), art)
open(os.path.join(HERE, "og-cards.html"), "w").write(html + "</body></html>")
print("ok", len(CARDS), "cards")
