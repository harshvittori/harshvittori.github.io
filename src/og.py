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

RESET_ART = ('<div class="bleed">' +
    window("r-intro-0", (320, 175, 800, 470), 565, "harshvittori.github.io/harsh-reset", "left:8px;top:50%;transform:translateY(-50%) rotate(-2deg)") +
    '<div class="fchip amber" style="left:10px;top:78px;transform:rotate(-4deg)">⏰&nbsp; Running 30 min late</div>'
    '<div class="plan" style="left:-24px;bottom:58px;transform:rotate(2deg)">'
    '<div class="row now"><b>3:00 PM</b><span>Send applications</span><em>+30m</em></div>'
    '<div class="row"><b>4:30 PM</b><span>Outreach</span><em>+30m</em></div>'
    '<div class="row meal"><b>5:30 PM</b><span>Lunch break</span><em>kept</em></div></div>'
    '<div class="fchip green" style="right:40px;bottom:150px;transform:rotate(3deg)">✓&nbsp; Whole day shifted</div></div>')

def kcard(t, co, col, tag, style="", cls=""):
    return ('<div class="kc %s" style="%s"><div class="kh"><i style="background:%s">%s</i><div><b>%s</b><small>%s</small></div></div>'
            '<span class="tg">%s</span></div>') % (cls, style, col, co[0], t, co, tag)
VAULT_ART = ('<div class="bleed">'
    '<div class="board" style="left:14px;top:50%;transform:translateY(-50%) rotate(-2deg)">'
    '<div class="bh"><span>SAVED</span><span>APPLIED</span><span>INTERVIEW</span></div>'
    '<div class="cols"><div class="kcol">' + kcard("GTM Associate", "Razorpay", "#3395FF", "Medium") + kcard("Growth Analyst", "Meesho", "#E0457B", "High") + '</div>'
    '<div class="kcol">' + kcard("Founder's Office", "Cred", "#1D1D1F", "Follow-up in 5d") + '<div class="slot"></div></div>'
    '<div class="kcol">' + kcard("Partnerships Lead", "Zomato", "#E23744", "Tue · 4:00 PM") + '</div></div></div>'
    + kcard("Growth Associate", "Swiggy", "#FC8019", "High", "left:215px;top:300px;transform:rotate(6deg);width:236px", "drag") +
    '<div class="toast" style="left:48px;bottom:44px">✓&nbsp; Applied, follow-up reminder set</div>'
    '<div class="fchip gold" style="right:64px;top:62px;transform:rotate(4deg)">🔔&nbsp; Follow up with Cred today</div></div>')

def bar(name, v):
    return '<div class="br"><div class="bt"><span>%s</span><b>%d</b></div><div class="bb"><i style="width:%d%%"></i></div></div>' % (name, v, v)
TEST_ART = ('<div class="bleed">'
    '<div class="score" style="left:40px;top:50%;transform:translateY(-50%) rotate(-2deg)">'
    '<div class="sc-top"><svg viewBox="0 0 120 120" class="ringsv"><circle cx="60" cy="60" r="50" fill="none" stroke="#E1F0E7" stroke-width="12"/>'
    '<circle cx="60" cy="60" r="50" fill="none" stroke="#127A4F" stroke-width="12" stroke-linecap="round" stroke-dasharray="314" stroke-dashoffset="104" transform="rotate(-90 60 60)"/></svg>'
    '<div class="sc-num"><small>YOUR SCORE</small><b>67<span>/100</span></b><em>Grounded</em></div></div>'
    + bar("Accountability", 89) + bar("Emotional control", 81) + bar("Handling conflict", 70) + '</div>'
    '<div class="fchip green" style="right:44px;top:66px;transform:rotate(4deg)">📄&nbsp; 2 PDFs ready</div>'
    '<div class="fchip amber" style="right:30px;bottom:70px;transform:rotate(-3deg)">🎯&nbsp; 30-day plan</div></div>')

HOME_ART2 = ('<div class="bleed">'
    '<div class="score mini" style="left:30px;top:44px;transform:rotate(-4deg)"><div class="tag-app">%s<span>HV Test</span></div>'
    '<div class="sc-top" style="margin:0"><svg viewBox="0 0 120 120" class="ringsv" style="width:96px;height:96px"><circle cx="60" cy="60" r="50" fill="none" stroke="#E1F0E7" stroke-width="13"/>'
    '<circle cx="60" cy="60" r="50" fill="none" stroke="#127A4F" stroke-width="13" stroke-linecap="round" stroke-dasharray="314" stroke-dashoffset="104" transform="rotate(-90 60 60)"/></svg>'
    '<div class="sc-num"><b style="font-size:60px">67<span style="font-size:22px">/100</span></b><em style="font-size:16px">Grounded</em></div></div></div>'
    '<div class="plan" style="left:214px;top:215px;width:350px;transform:rotate(3deg);z-index:4"><div class="tag-app">%s<span>HV Reset</span></div>'
    '<div class="row now"><b>3:00 PM</b><span>Send applications</span><em>+30m</em></div>'
    '<div class="row"><b>4:30 PM</b><span>Outreach</span><em>+30m</em></div></div>'
    '<div class="vmini" style="left:40px;top:392px;transform:rotate(-2deg)"><div class="tag-app">%s<span>HV Vault</span></div>'
    + kcard("Growth Associate", "Swiggy", "#FC8019", "Applied ✓", "position:relative;box-shadow:none;border:1px solid #EEF0F5") +
    '</div><div class="toast" style="left:250px;bottom:40px;z-index:5">✓&nbsp; Follow-up reminder set</div></div>') % (
    svg("logo-test", 26, 0, False), svg("logo-reset", 26, 0, False), svg("logo-vault", 26, 0, False))
RIYA = '<div class="riya">%s</div>' % story.prologue()

CARDS = [  # out, brand logo, brand word, accent, dark, tint, circle, eyebrow, headline, sub, cta, art
    ("og.jpg", "world-orbit", "WORLD", "#2E43A6", "#233489", "#F4F5FB", "#E2E7F8", "3 free apps · by Harsh Vittori",
     "Stop guessing.<br>Start growing.", "Know your strengths. Run a calm day.<br>Never miss a follow-up.", "▶&nbsp; Watch the 45s film", HOME_ART2),
    ("story/og.jpg", "world", "WORLD", "#2E43A6", "#233489", "#F4F5FB", "#E2E7F8", "A 1-minute illustrated story",
     "Hard work. Zero progress. Sound familiar?", "Meet Riya. A 1-minute story about the 3 things quietly holding her back.", "Read her story &nbsp;→", RIYA),
    ("test/og.jpg", "logo-test", "TEST", "#127A4F", "#0D5E3C", "#F4F8F5", "#DDEFE4", "10 minutes · Free · No login",
     "You think you know yourself. Prove it.", "Real-life situations. An honest score out of 100, and a 30-day plan to grow.", "Take the test &nbsp;→",
     TEST_ART),
    ("reset/og.jpg", "logo-reset", "RESET", "#3F66BE", "#2C4E99", "#F3F6FC", "#DCE6F8", "Plan your day",
     "Late start?<br>Fix your whole day<br>in one tap.", "One block, one task, zero guilt. Meals and breaks stay protected.", "Plan my day &nbsp;→",
     RESET_ART),
    ("vault/og.jpg", "logo-vault", "VAULT", "#A0721C", "#7C5712", "#FAF7F0", "#F1E6CF", "For your job hunt",
     "Stop losing job leads in WhatsApp chats.", "Every job, recruiter and interview on one board, with follow-ups that set themselves.", "Organise my job hunt &nbsp;→",
     VAULT_ART),
]

CSS = font(500) + font(600) + font(700) + """
*{box-sizing:border-box;margin:0}body{background:#888}
.card{position:relative;width:1200px;height:630px;overflow:hidden;font-family:Outfit,sans-serif;color:#16212B;background:var(--tint);margin-bottom:20px}
.c1{position:absolute;width:720px;height:720px;border-radius:50%;background:var(--circle);right:-170px;top:-120px}
.c2{position:absolute;width:280px;height:280px;border-radius:50%;background:var(--circle);opacity:.6;left:430px;bottom:-200px}
.left{position:absolute;left:64px;top:0;bottom:0;width:560px;z-index:5;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}
.brand{display:flex;align-items:center;gap:14px;font-weight:700;font-size:32px;letter-spacing:.02em}
.brand svg{box-shadow:none!important}.brand b{color:var(--accent);font-weight:700}
.eye{margin-top:38px;font-weight:600;font-size:18px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
h1{margin-top:12px;font-weight:700;font-size:64px;line-height:1.02;letter-spacing:-.015em}
.rule{width:56px;height:6px;border-radius:4px;background:#F2A33A;margin:24px 0 20px}
.sub{font-weight:500;font-size:24px;line-height:1.35;color:#3D4A55;max-width:540px}
.cta{display:inline-flex;align-items:center;margin-top:28px;font-weight:600;font-size:23px;color:#fff;background:var(--accent);padding:14px 28px;border-radius:999px;box-shadow:0 14px 30px -12px var(--accent)}
.win{position:absolute;border-radius:16px;overflow:hidden;background:#fff;border:1px solid rgba(20,30,60,.12);box-shadow:0 40px 80px -30px rgba(20,30,60,.55)}
.bar{height:28px;background:#EEF0F5;display:flex;align-items:center;gap:7px;padding:0 12px;border-bottom:1px solid rgba(20,30,60,.08)}
.bar i{width:10px;height:10px;border-radius:50%;background:#FF5F57}.bar i:nth-child(2){background:#FEBC2E}.bar i:nth-child(3){background:#28C840}
.bar span{margin-left:14px;font-size:13px;color:#6B7390;background:#fff;padding:3px 14px;border-radius:6px;white-space:nowrap;overflow:hidden}
.scr{background-repeat:no-repeat}
.fan{position:absolute;left:600px;top:50%;transform:translateY(-50%);width:640px;height:560px}
.bleed{position:absolute;left:620px;top:0;width:620px;height:630px}
.fchip{position:absolute;z-index:4;font-weight:600;font-size:22px;padding:13px 22px;border-radius:999px;background:#fff;box-shadow:0 18px 40px -16px rgba(20,30,60,.45);white-space:nowrap}
.fchip.amber{color:#9A5B07;background:#FFF4E2;border:1.5px solid #F6D6A4}.fchip.green{color:#0F6B45;background:#E9F7EF;border:1.5px solid #BFE5CF}.fchip.gold{color:#7C5712;background:#FFF8EA;border:1.5px solid #EBD7AE}
.plan{position:absolute;z-index:3;width:372px;background:#fff;border-radius:20px;padding:12px;box-shadow:0 30px 60px -24px rgba(20,30,60,.5)}
.plan .row{display:flex;align-items:center;gap:12px;padding:11px 12px;border-radius:12px;background:#F2F4F8;margin-bottom:8px;font-size:18px;font-weight:600}.plan .row:last-child{margin-bottom:0}
.plan .row b{font-size:15px;color:#6B7390;width:66px}.plan .row span{flex:1}.plan .row em{font-style:normal;font-size:14px;color:#9A5B07;background:#FFF1DB;padding:3px 9px;border-radius:999px}
.plan .row.now{background:#1D2230;color:#fff}.plan .row.now b{color:#AEB6CC}.plan .row.meal{background:#FBF4E4}.plan .row.meal em{color:#0F6B45;background:#E3F4EA}
.board{position:absolute;width:690px;background:rgba(255,255,255,.96);border-radius:26px;padding:22px 20px;box-shadow:0 40px 80px -30px rgba(20,30,60,.5);border:1px solid rgba(20,30,60,.06)}
.bh{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px}.bh span{font-size:15px;font-weight:600;letter-spacing:.14em;color:#8A91AB}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;height:318px}
.kcol{background:#F3F4F8;border-radius:16px;padding:10px;display:flex;flex-direction:column;gap:10px}
.kc{background:#fff;border-radius:14px;padding:12px;box-shadow:0 4px 12px -6px rgba(20,30,60,.25)}
.kh{display:flex;gap:10px;align-items:center}.kh i{width:38px;height:38px;border-radius:11px;color:#fff;font-style:normal;font-weight:700;font-size:17px;display:grid;place-items:center;flex:none}
.kh b{display:block;font-size:18px;font-weight:600;line-height:1.15}.kh small{font-size:14.5px;color:#6B7390}
.tg{display:inline-block;margin-top:10px;font-size:14px;font-weight:600;color:#7C5712;background:#FBF1DC;padding:3px 9px;border-radius:999px}
.slot{height:96px;border-radius:14px;border:2px dashed #D6C7A6;background:rgba(251,244,228,.6)}
.kc.drag{position:absolute;z-index:4;box-shadow:0 30px 50px -16px rgba(20,30,60,.55)}
.toast{position:absolute;z-index:5;font-weight:600;font-size:19px;color:#fff;background:#1D2230;padding:14px 22px;border-radius:14px;box-shadow:0 20px 40px -16px rgba(0,0,0,.5);white-space:nowrap}
.score{position:absolute;width:470px;background:#fff;border-radius:28px;padding:30px 32px 26px;box-shadow:0 40px 80px -30px rgba(20,30,60,.5)}
.sc-top{display:flex;align-items:center;gap:26px;margin-bottom:22px}.ringsv{width:150px;height:150px;flex:none}
.sc-num small{display:block;font-size:15px;font-weight:600;letter-spacing:.14em;color:#6B7390}
.sc-num b{display:block;font-size:84px;font-weight:700;line-height:1;color:#16212B}.sc-num b span{font-size:30px;color:#8A91AB;font-weight:600}
.sc-num em{font-style:normal;display:inline-block;margin-top:8px;font-size:20px;font-weight:600;color:#0F6B45;background:#E3F4EA;padding:5px 14px;border-radius:999px}
.br{margin-top:14px}.bt{display:flex;justify-content:space-between;font-size:18px;font-weight:600;color:#3D4A55;margin-bottom:6px}.bt b{color:#127A4F}
.bb{height:10px;border-radius:9px;background:#E7F1EB;overflow:hidden}.bb i{display:block;height:100%;background:#127A4F;border-radius:9px}
.score.mini{width:300px;padding:18px 22px}
.vmini{position:absolute;width:300px;background:#fff;border-radius:22px;padding:16px;box-shadow:0 30px 60px -24px rgba(20,30,60,.5);z-index:3}
.tag-app{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600;color:#6B7390;margin-bottom:10px}
.riya{position:absolute;right:48px;top:50%;width:520px;transform:translateY(-50%) rotate(2deg);border-radius:26px;overflow:hidden;box-shadow:0 40px 80px -30px rgba(20,30,60,.55)}
.riya svg{display:block;width:100%;height:auto}
"""
html = "<!DOCTYPE html><html><head><meta charset='utf-8'><style>%s</style></head><body>" % CSS
for out, lg, word, acc, dark, tint, circ, eye, h1, sub, cta, art in CARDS:
    html += ('<div class="card" data-out="%s" style="--accent:%s;--dark:%s;--tint:%s;--circle:%s"><div class="c1"></div><div class="c2"></div>'
             '<div class="left"><div class="brand">%sHV <b>%s</b></div><p class="eye">%s</p><h1>%s</h1><div class="rule"></div><p class="sub">%s</p>'
             '<div class="cta">%s</div></div>%s</div>') % (out, acc, dark, tint, circ, svg(lg, 48, 0, False), word, eye, h1, sub, cta, art)
open(os.path.join(HERE, "og-cards.html"), "w").write(html + "</body></html>")
print("ok", len(CARDS), "cards")
