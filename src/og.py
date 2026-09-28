"""Link-preview (Open Graph) cards for every page of harshvittori.github.io.
A curiosity headline, a real app screen (Riya for the story), and one clear call to action,
in the HV Test card style (logo + name, label, amber rule). Writes src/og-cards.html;
render the five 1200x630 JPEGs with src/og-render.js (Playwright):
  python3 src/og.py && node src/og-render.js
"""
import os, re, sys, base64
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import story                                   # Riya's illustration comes from the story page itself

_k = [0]
def svg(name, size, rot=0, shadow=True):
    _k[0] += 1
    s = open(os.path.join(HERE, name + ".svg")).read().strip()
    for i in re.findall(r'id="([^"]+)"', s):
        s = s.replace('id="%s"' % i, 'id="%s-og%d"' % (i, _k[0])).replace("url(#%s)" % i, "url(#%s-og%d)" % (i, _k[0]))
    st = "width:%dpx;height:%dpx;border-radius:%dpx;transform:rotate(%sdeg);flex:none;%s" % (size, size, size * .24, rot, "box-shadow:0 24px 50px -20px rgba(20,30,60,.5)" if shadow else "")
    return s.replace("<svg ", '<svg style="%s" ' % st, 1)

def font(w):
    b = base64.b64encode(open(os.path.join(HERE, "fonts", "outfit-latin-%d-normal.woff2" % w), "rb").read()).decode()
    return "@font-face{font-family:Outfit;font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2')}" % (w, b)

def window(img, crop, width, url, style=""):
    """A browser window showing a crop (x, y, w, h in 1440-wide screenshot px) of a real app screen."""
    x, y, w, h = crop; k = width / w
    return ('<div class="win" style="width:%dpx;%s"><div class="bar"><i></i><i></i><i></i><span>%s</span></div>'
            '<div class="scr" style="height:%dpx;background-image:url(og-assets/%s.jpg);background-size:%.1fpx auto;background-position:-%.1fpx -%.1fpx"></div></div>') % (
        width, style, url, h * k, img, 1440 * k, x * k, y * k)

HOME_ART = ('<div class="fan">' +
            window("t-result", (380, 40, 700, 460), 330, "hv-tests", "left:0;top:150px;transform:rotate(-8deg)") +
            window("r-intro-0", (220, 60, 1000, 640), 360, "harsh-reset", "left:170px;top:40px;transform:rotate(3deg);z-index:2") +
            window("v-dash-a", (0, 0, 1440, 900), 380, "hv-vault-web", "left:250px;top:250px;transform:rotate(-2deg);z-index:3") + '</div>')
RIYA = '<div class="riya">%s</div>' % story.prologue()

CARDS = [  # out, brand logo, brand word, accent, dark, tint, circle, eyebrow, headline, sub, cta, art
    ("og.jpg", "world-orbit", "WORLD", "#2E43A6", "#233489", "#F4F5FB", "#E2E7F8", "3 free apps · by Harsh Vittori",
     "Stop guessing.<br>Start growing.", "Know your strengths. Run a calm day.<br>Never miss a follow-up.", "▶&nbsp; Watch the 45s film", HOME_ART),
    ("story/og.jpg", "world", "WORLD", "#2E43A6", "#233489", "#F4F5FB", "#E2E7F8", "A 1-minute illustrated story",
     "Hard work. Zero progress. Sound familiar?", "Meet Riya. A 1-minute story about the 3 things quietly holding her back.", "Read her story &nbsp;→", RIYA),
    ("test/og.jpg", "logo-test", "TEST", "#127A4F", "#0D5E3C", "#F4F8F5", "#DDEFE4", "10 minutes · Free · No login",
     "You think you know yourself. Prove it.", "Real-life situations. An honest score out of 100, and a 30-day plan to grow.", "Take the test &nbsp;→",
     window("t-result", (380, 40, 700, 460), 560, "harshvittori.github.io/hv-tests", "right:-40px;top:120px;transform:perspective(1400px) rotateY(-12deg) rotateX(3deg)")),
    ("reset/og.jpg", "logo-reset", "RESET", "#3F66BE", "#2C4E99", "#F3F6FC", "#DCE6F8", "Plan your day",
     "Late start?<br>Fix your whole day<br>in one tap.", "One block, one task, zero guilt. Meals and breaks stay protected.", "Plan my day &nbsp;→",
     window("r-late", (330, 40, 780, 470), 560, "harshvittori.github.io/harsh-reset", "right:-40px;top:120px;transform:perspective(1400px) rotateY(-12deg) rotateX(3deg)")),
    ("vault/og.jpg", "logo-vault", "VAULT", "#A0721C", "#7C5712", "#FAF7F0", "#F1E6CF", "For your job hunt",
     "Stop losing job leads in WhatsApp chats.", "Every job, recruiter and interview on one board, with follow-ups that set themselves.", "Organise my job hunt &nbsp;→",
     window("v-pipe-b", (575, 225, 865, 420), 560, "harshvittori.github.io/hv-vault-web", "right:-40px;top:120px;transform:perspective(1400px) rotateY(-12deg) rotateX(3deg)")),
]

CSS = font(500) + font(600) + font(700) + """
*{box-sizing:border-box;margin:0}body{background:#888}
.card{position:relative;width:1200px;height:630px;overflow:hidden;font-family:Outfit,sans-serif;color:#16212B;background:var(--tint);margin-bottom:20px}
.c1{position:absolute;width:720px;height:720px;border-radius:50%;background:var(--circle);right:-170px;top:-120px}
.c2{position:absolute;width:280px;height:280px;border-radius:50%;background:var(--circle);opacity:.6;left:430px;bottom:-200px}
.left{position:absolute;left:64px;top:52px;width:560px;z-index:5}
.brand{display:flex;align-items:center;gap:14px;font-weight:700;font-size:32px;letter-spacing:.02em}
.brand svg{box-shadow:none!important}.brand b{color:var(--accent);font-weight:700}
.eye{margin-top:44px;font-weight:600;font-size:18px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
h1{margin-top:12px;font-weight:700;font-size:64px;line-height:1.02;letter-spacing:-.015em}
.rule{width:56px;height:6px;border-radius:4px;background:#F2A33A;margin:24px 0 20px}
.sub{font-weight:500;font-size:24px;line-height:1.35;color:#3D4A55;max-width:540px}
.cta{display:inline-flex;align-items:center;margin-top:28px;font-weight:600;font-size:23px;color:#fff;background:var(--accent);padding:14px 28px;border-radius:999px;box-shadow:0 14px 30px -12px var(--accent)}
.win{position:absolute;border-radius:16px;overflow:hidden;background:#fff;border:1px solid rgba(20,30,60,.12);box-shadow:0 40px 80px -30px rgba(20,30,60,.55)}
.bar{height:28px;background:#EEF0F5;display:flex;align-items:center;gap:7px;padding:0 12px;border-bottom:1px solid rgba(20,30,60,.08)}
.bar i{width:10px;height:10px;border-radius:50%;background:#FF5F57}.bar i:nth-child(2){background:#FEBC2E}.bar i:nth-child(3){background:#28C840}
.bar span{margin-left:14px;font-size:13px;color:#6B7390;background:#fff;padding:3px 14px;border-radius:6px;white-space:nowrap;overflow:hidden}
.scr{background-repeat:no-repeat}
.fan{position:absolute;left:600px;top:40px;width:640px;height:560px}
.riya{position:absolute;right:48px;top:96px;width:520px;transform:rotate(2deg);border-radius:26px;overflow:hidden;box-shadow:0 40px 80px -30px rgba(20,30,60,.55)}
.riya svg{display:block;width:100%;height:auto}
"""
html = "<!DOCTYPE html><html><head><meta charset='utf-8'><style>%s</style></head><body>" % CSS
for out, lg, word, acc, dark, tint, circ, eye, h1, sub, cta, art in CARDS:
    html += ('<div class="card" data-out="%s" style="--accent:%s;--dark:%s;--tint:%s;--circle:%s"><div class="c1"></div><div class="c2"></div>'
             '<div class="left"><div class="brand">%sHV <b>%s</b></div><p class="eye">%s</p><h1>%s</h1><div class="rule"></div><p class="sub">%s</p>'
             '<div class="cta">%s</div></div>%s</div>') % (out, acc, dark, tint, circ, svg(lg, 48, 0, False), word, eye, h1, sub, cta, art)
open(os.path.join(HERE, "og-cards.html"), "w").write(html + "</body></html>")
print("ok", len(CARDS), "cards")
