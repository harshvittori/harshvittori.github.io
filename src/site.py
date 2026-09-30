"""HV World: the home page (all three apps, HV AI, privacy, access, FAQ)
and one page per app: /test/, /reset/, /vault/. Logos come from src/.

Run from the repo root:  python3 src/site.py
The story page (index.html) comes from src/story.py."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import transitions
import legal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Links into the apps (HV Test, HV Reset, HV Vault) open in a new tab, so HV World stays open behind them.
def app_links_new_tab(html):
    return re.sub(r'<a\b([^>]*\bhref="https://harshvittori\.github\.io/(?:hv-reset|hv-vault-web|hv-tests)/[^"]*"[^>]*)>',
                  lambda m: m.group(0) if "target=" in m.group(1) else '<a' + m.group(1) + ' target="_blank" rel="noopener">', html)

def read(n):
    return open(os.path.join(HERE, n)).read().strip().replace('xmlns="http://www.w3.org/2000/svg" ', '')

LOGOS = {"ai": read("logo-ai.svg"), "world": read("world.svg"), "test": read("logo-test.svg"), "reset": read("logo-reset.svg"), "vault": read("logo-vault.svg")}
_n = [0]
def logo(name, cls=""):
    _n[0] += 1
    s = LOGOS[name]
    for i in re.findall(r'id="([^"]+)"', s):
        s = s.replace('id="%s"' % i, 'id="%s-%d"' % (i, _n[0])).replace("url(#%s)" % i, "url(#%s-%d)" % (i, _n[0]))
    return s.replace("<svg ", '<svg aria-hidden="true" focusable="false"%s ' % (' class="%s"' % cls if cls else ""), 1)

def I(d):
    return ('<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>' % d)
CHECK = I('<path d="M5 12.5l4.2 4.2L19 7"/>')
ARROW = I('<path d="M5 12h14M13 6l6 6-6 6"/>')
CHAIN = I('<rect x="2.5" y="8" width="11" height="8" rx="4"/><rect x="10.5" y="8" width="11" height="8" rx="4"/>')
SYNC = I('<path d="M21 12a9 9 0 0 1-15.5 6.2M3 12A9 9 0 0 1 18.5 5.8"/><path d="M18.5 2v4h-4M5.5 22v-4h4"/>')
USER = I('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>')
SPARK = I('<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>')
LOCK = I('<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>')

URL = {"test": "https://harshvittori.github.io/hv-tests/", "reset": "https://harshvittori.github.io/hv-reset/", "vault": "https://harshvittori.github.io/hv-vault-web/"}

# ---------------------------------------------------------------- product previews (plain HTML, no screenshots)
MOCK_TEST = '''<div class="mock q">
  <div class="qh"><span class="qlogo">''' + LOGOS["test"] + '''</span><div><b>Maturity Assessment</b><small>Personal Growth</small></div><span class="qn">18 / 29</span></div>
  <div class="prog"><i></i></div>
  <h5>A teammate takes credit for your idea in a meeting. What do you do?</h5>
  <div class="opt"><span class="k">A</span>Correct them right there</div>
  <div class="opt on"><span class="k">B</span>Talk to them privately after<span class="tk">&#10003;</span></div>
  <div class="opt"><span class="k">C</span>Let it go this time</div>
  <div class="opt"><span class="k">D</span>Tell your manager later</div>
  <div class="qf"><span>About 10 min</span><span class="nx">Next &rarr;</span></div>
</div>'''

MOCK_RESET = '''<div class="mock day">
  <p class="meta">Now · until 12:30 PM</p>
  <div class="now">01:14:52</div>
  <p class="meta">Deep work: project report</p>
  <div class="blk cur"><span>11:00 AM</span>Deep work: project report</div>
  <div class="blk"><span>12:30 PM</span>Short break</div>
  <div class="blk meal"><span>1:15 PM</span>Lunch</div>
  <div class="stats"><div><b>4/5</b><small>done today</small></div><div><b>2h 40m</b><small>focused</small></div><div><b>6 days</b><small>streak</small></div></div>
</div>'''

MOCK_VAULT = '''<div class="mock vt">
  <div class="qh"><span class="qlogo">''' + LOGOS["vault"] + '''</span><div><b>Your job search</b><small>This week</small></div><span class="qn">3 due today</span></div>
  <div class="vs"><div><b>12</b><small>Applied</small></div><div><b>3</b><small>Interviews</small></div><div><b>25%</b><small>Reply rate</small></div></div>
  <div class="kan">
    <div><h4>Saved</h4><div><b>GTM Associate</b><small>Razorpay</small></div><div><b>Growth Analyst</b><small>Meesho</small></div></div>
    <div><h4>Applied</h4><div class="hot"><b>Founder's Office</b><small>Cred &middot; follow-up today</small></div><div><b>Product Analyst</b><small>Swiggy</small></div></div>
    <div><h4>Interview</h4><div class="int"><b>Partnerships Lead</b><small>Zomato &middot; Tue 4 PM</small></div></div>
  </div>
  <div class="vfu"><span class="vb">&#128276;</span><div><b>Follow up with Cred</b><small>Founder's Office &middot; message ready</small></div><span class="nx">Send</span></div>
  <div class="vai"><span class="sp">&#10022;</span><span class="tx">&ldquo;Kal 4 baje Zomato ka interview hai&rdquo;</span><em>HV AI</em></div>
</div>'''

MOCK_AI = '''<div class="mock chat">
  <p class="ai">Bolo, kya karna hai?</p>
  <p class="me">Kal 4 baje Zomato ka interview hai</p>
  <div class="card"><b>Interview</b>Zomato · Tue, 29 Sep · 4:00 PM<em>Confirm</em></div>
  <p class="me">Cred wale ko applied mark karo aur 5 din baad follow-up laga do</p>
  <div class="card"><b>2 changes</b>Founder's Office at Cred → Applied, follow-up on 4 Oct<em>Confirm all</em></div>
</div>'''

PRODUCTS = [
    ("test", "HV Test", "Know yourself", "Tests that show how you think, learn, act and grow, so you know where you stand and what to work on next.", [
        ("A growing library of tests.", "Traits, thinking, skills and personal growth. The Maturity Assessment is live now."),
        ("An honest score.", "See where you're strong and where to grow, not just a number."),
        ("A checkable scorecard.", "Your score and skill marks with a unique ID and QR, plus a full report and a 30-day plan."),
        ("Private by design.", "No login. Your answers never leave your browser."),
    ], MOCK_TEST, "Take a test"),
    ("reset", "HV Reset", "Plan your day. See your progress.", "Plan your day, do one task at a time, and see what you really did. Your own dashboard shows where your time goes and whether you're getting better.", [
        ("One task at a time.", "A big clock shows what's on now, what's next and how long is left. Pause when you step away."),
        ("Your own dashboard.", "Time spent, real focus, what started on time, streaks and a score that shows if you're improving."),
        ("Running late? Shift the day.", "One tap moves the rest of the plan. Nothing is lost."),
        ("Plans from one sentence.", "Tell HV AI “Aaj 9 se 1 padhai, 6 baje gym” and your day is ready."),
    ], MOCK_RESET, "Open HV Reset"),
    ("vault", "HV Vault", "Act on every opportunity", "Every job, company, follow-up and interview in one calm place, so nothing slips.", [
        ("One board.", "Move jobs from Saved to Applied, Interview and Offer."),
        ("Follow-ups that set themselves.", "Mark a job Applied and the first reminder is ready."),
        ("Profile from your resume.", "Upload it once and your profile fills itself in."),
        ("Calendar, templates, numbers.", "Interviews, ready-to-send messages and your weekly progress."),
    ], MOCK_VAULT, "Open HV Vault"),
]

# small "live" badges that float around each product picture (home cards and product page heroes)
CHIPS = {
    "test": [("&#10003; Score 72 of 100", "good"), ("&#127941; Scorecard with ID", ""), ("&#127793; Your 30-day plan", "")],
    "reset": [("&#9200; Running 30 min late", "warn"), ("&#10003; Whole day shifted", "good"), ("&#128293; 6-day streak", "")],
    "vault": [("&#10003; Moved to Applied", "good"), ("&#128197; Interview Tue, 4 PM", ""), ("&#10024; Auto follow-up set", "warn")],
}
def stage(key, mock):
    chips = "".join('<span class="chip c%d %s" aria-hidden="true">%s</span>' % (i, cls, t) for i, (t, cls) in enumerate(CHIPS.get(key, [])))
    return '<div class="stage">%s%s</div>' % (mock, chips)

def product(key, name, tag, pitch, feats, mock, cta, flip):
    lis = "".join('<li>%s<span><b>%s</b> %s</span></li>' % (CHECK, a, b) for a, b in feats)
    return ('''<article class="product p-%s%s rv" id="%s">
  <div class="left">
    <div class="top">%s<div><h3>%s</h3><p class="tag">%s</p></div></div>
    <p class="pitch">%s</p>
    <ul>%s</ul>
    <div class="acts"><a class="btn" href="%s">%s %s</a><a class="btn ghost" href="/%s/">Learn more</a></div>
  </div>
  <div class="right">%s</div>
</article>''' % (key, " flip" if flip else "", key, logo(key), name, tag, pitch, lis, URL[key], cta, ARROW, key, stage(key, mock)))

FAQ = [
    ("Who can use HV World?", "Everyone. HV Test, HV Reset and HV Vault are free for everyone, and so is HV AI. Open them in any browser, on your phone or laptop."),
    ("Do I need to install anything?", "No. Everything runs in the browser on your phone or laptop. On a phone you can add any app to your home screen from the browser's share menu."),
    ("Do I need an account?", "HV Vault uses Google sign-in, so your data follows you across devices. HV Test needs no account at all."),
    ("What languages does HV AI understand?", "Hindi, English and Hinglish, typed or spoken. It replies in the language you use."),
    ("Can HV AI change things without asking?", "No. Every change is shown first as a card you confirm, edit or cancel. Deletes always ask again, and you can undo the last change."),
    ("Are HV Test results a diagnosis?", "No. HV Test is a self-assessment for personal growth, not a clinical or psychological diagnosis."),
]

CSS = r"""
:root{--ink:#1D1D1F;--soft:#6E6E73;--faint:#86868B;--line:#E4E5EA;--gray:#F2F3F6;--bg:#F9F9FB;--accent:#2E43A6;--accent-hover:#1D2B72;
  --test:#127A4F;--reset:#4A72C8;--vault:#A87A22;--font:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue",Helvetica,Arial,sans-serif;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 var(--font);letter-spacing:-.018em;-webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3,h4,h5,p{margin:0}a{color:inherit}
.wrap{width:min(1120px,100% - 32px);margin:0 auto}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:#fff;padding:8px 14px;border-radius:8px;z-index:99}.skip:focus{left:8px}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:8px}
/* header */
header{position:sticky;top:0;z-index:50;background:rgba(249,249,251,.85);-webkit-backdrop-filter:saturate(180%) blur(18px);backdrop-filter:saturate(180%) blur(18px);border-bottom:1px solid rgba(0,0,0,.07)}
.nav{height:52px;display:flex;align-items:center;gap:20px}
.brand{display:flex;align-items:center;gap:9px;text-decoration:none;font-weight:600;font-size:17px}
.brand svg{width:26px;height:26px;border-radius:7px}
.nav nav{display:flex;align-items:center;gap:4px;margin-left:auto;font-size:14px}
.nav nav a{position:relative;display:inline-block;white-space:nowrap;line-height:32px;height:32px;padding:0 13px;border-radius:999px;text-decoration:none;color:var(--soft);font-weight:500;transition:color .2s ease,background-color .2s ease,box-shadow .2s ease}
.nav nav a:hover{color:var(--accent);background:rgba(46,67,166,.07);text-decoration:none}
.nav nav a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.nav nav a[aria-current]{color:var(--accent);font-weight:600;background:#E8ECFB;box-shadow:inset 0 0 0 1px rgba(46,67,166,.14)}
.nav nav a[aria-current]:hover{background:#E1E6FA}
.brand{white-space:nowrap}
.ni{display:none;width:20px;height:20px;vertical-align:middle}
@media (max-width:720px){.nav nav a.ic{padding:0 8px}.nav nav a.ic .nt{display:none}.nav nav a.ic .ni{display:inline-block;margin-top:-3px}}
@media (max-width:720px){.nav nav a.opt,.nav .d{display:none}.nav nav{gap:2px}.nav nav a{height:30px;line-height:30px;padding:0 10px}}
@media (max-width:470px){.brand{font-size:0;gap:0}.nav nav a{padding:0 9px}}
@media (max-width:360px){.nav nav a{padding:0 7px;font-size:13.5px}}
/* buttons */
.btn{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:11px 22px;border-radius:999px;background:var(--accent);color:#fff;text-decoration:none;font-weight:500;font-size:16px;transition:background .2s}
.btn:hover{background:var(--accent-hover)}
.btn svg{width:17px;height:17px}
.btn.ghost{background:transparent;color:var(--accent);padding-left:6px;padding-right:6px}.btn.ghost:hover{background:transparent;text-decoration:underline}
/* hero */
.hero{padding:88px 0 56px;display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.eyebrow{font-size:15px;font-weight:600;color:var(--soft);margin-bottom:14px}
.hero h1{font-size:clamp(42px,6vw,72px);font-weight:700;letter-spacing:-.045em;line-height:1.03}
.hero h1 span{color:var(--accent)}
.lead{font-size:clamp(18px,2vw,21px);color:var(--soft);margin:22px 0 30px;max-width:540px;line-height:1.45}
.ctas{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center}
.note{margin-top:18px;font-size:14px;color:var(--faint)}
.orbit{position:relative;aspect-ratio:1;max-width:440px;margin:0 auto;width:100%}
.orbit::before{content:"";position:absolute;inset:-4%;border-radius:50%;background:radial-gradient(circle,rgba(91,99,214,.16) 0%,rgba(91,99,214,.06) 45%,transparent 70%);pointer-events:none}
.orbit .ring{position:absolute;inset:8%;border-radius:50%;border:1.5px dashed #D2D2D7}
.orbit .ring.r2{inset:25%}
.orbit .core{position:absolute;inset:37%}
.orbit .core svg{width:100%;height:100%;border-radius:26%;box-shadow:0 24px 50px -22px rgba(30,40,110,.55)}
.planet{position:absolute;width:23%;text-decoration:none;display:flex;flex-direction:column;align-items:center;gap:10px;transition:transform .35s cubic-bezier(.22,1,.36,1)}
.planet svg{width:100%;aspect-ratio:1;border-radius:24%;box-shadow:0 16px 34px -18px rgba(20,30,70,.5)}
.planet span{font-weight:600;font-size:13.5px;white-space:nowrap;background:#fff;padding:5px 12px;border-radius:999px;border:1px solid var(--line);box-shadow:0 8px 18px -12px rgba(20,30,70,.45)}
.planet:hover{transform:translateY(-5px)}
.planet.p1{left:38.5%;top:-3%}.planet.p2{left:-1%;top:56%}.planet.p3{right:-1%;top:56%}
@media (prefers-reduced-motion:no-preference){.orbit .ring{animation:spin 90s linear infinite}.orbit .ring.r2{animation-duration:60s;animation-direction:reverse}.planet{animation:float 7s ease-in-out infinite}.planet.p2{animation-delay:-2.3s}.planet.p3{animation-delay:-4.6s}}
@keyframes spin{to{transform:rotate(360deg)}}@keyframes float{50%{translate:0 -8px}}
@media (max-width:880px){.hero{grid-template-columns:1fr;padding:48px 0 40px;gap:36px}.orbit{max-width:320px}}
/* strip */
.strip{--pc:var(--accent);--pline:#DADDF2;margin-bottom:72px}
/* section heads */
section{scroll-margin-top:72px}
.head{max-width:680px;margin:0 auto 44px;text-align:center}
.label{font-size:15px;font-weight:600;color:var(--accent);margin-bottom:10px}
.head h2,.sec-h{font-size:clamp(32px,4.4vw,52px);font-weight:700;letter-spacing:-.04em;line-height:1.06}
.head p:not(.label){font-size:19px;color:var(--soft);margin-top:14px}
/* products */
.products{display:grid;gap:20px;margin-bottom:112px}
.product{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--pline,var(--line));border-radius:28px;overflow:hidden;background:#fff;scroll-margin-top:72px}
.product .left{padding:44px;display:flex;flex-direction:column;gap:18px}
.product .top{display:flex;align-items:center;gap:16px}
.product .top svg{width:60px;height:60px;border-radius:16px;flex:none}
.product h3{font-size:30px;font-weight:700;letter-spacing:-.035em;line-height:1.1}
.product .tag{font-size:15px;font-weight:600;margin-top:3px}
.p-test .tag,.p-test li svg{color:var(--test)}.p-reset .tag,.p-reset li svg{color:var(--reset)}.p-vault .tag,.p-vault li svg{color:var(--vault)}
.product .pitch{font-size:18.5px;color:var(--soft);line-height:1.45}
.product ul{list-style:none;padding:0;margin:0;display:grid;gap:12px}
.product li{display:flex;gap:12px;align-items:flex-start;font-size:16px;line-height:1.45}
.product li svg{width:20px;height:20px;flex:none;margin-top:2px}
.product li span{color:var(--soft)}.product li b{color:var(--ink);font-weight:600}
.product .btn{align-self:flex-start;margin-top:6px}
.product .right{background:var(--tint,var(--gray));border-left:1px solid var(--pline,var(--line));padding:56px 48px;display:flex;align-items:center;justify-content:center;min-height:460px;overflow:hidden}
.product.flip .left{order:2}.product.flip .right{border-left:0;border-right:1px solid var(--pline)}
.p-test{--tint:#EEF6F1;--pline:#D3E7DA;--pc:#127A4F}.p-reset{--tint:#EEF2FB;--pline:#D6E0F4;--pc:#4A72C8}.p-vault{--tint:#F8F3E8;--pline:#EADDC2;--pc:#A87A22}
.acts{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin-top:6px}.product .acts .btn{margin-top:0}
@media (max-width:880px){.product{grid-template-columns:1fr}.product.flip .left{order:0}.product .right,.product.flip .right{border-left:0;border-right:0;border-top:1px solid var(--pline)}.product .left{padding:28px 22px}.product .right{min-height:0;padding:44px 18px 30px}}
/* mock screens: white cards on gray */
@font-face{font-family:HVSora;src:url(/media/fonts/Sora-Regular.ttf) format("truetype");font-weight:400;font-display:swap}
@font-face{font-family:HVSora;src:url(/media/fonts/Sora-SemiBold.ttf) format("truetype");font-weight:600 700;font-display:swap}
.mock{width:100%;max-width:450px;background:#fff;border:1px solid var(--line);border-radius:22px;padding:20px;font-size:14.5px;font-family:HVSora,var(--font);letter-spacing:-.01em;box-shadow:0 24px 50px -32px rgba(20,30,60,.35)}
.mock h5,.mock b{font-family:HVSora,var(--font)}
.meta{font-size:12.5px;color:var(--faint)}
.mock .qh{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.mock .qlogo svg{width:34px;height:34px;border-radius:10px;display:block;box-shadow:0 6px 14px -6px rgba(18,122,79,.6)}
.mock .qh b{display:block;font-size:14px;font-weight:600;line-height:1.2}.mock .qh small{display:block;font-size:12px;color:var(--faint)}
.mock .qn{margin-left:auto;font-size:12px;font-weight:600;color:var(--test);background:#EAF6EF;border:1px solid #CFE9DA;padding:4px 10px;border-radius:999px}
.q .prog{height:6px;border-radius:9px;background:#E3F2EA;margin-bottom:14px;overflow:hidden}.q .prog i{display:block;height:100%;width:62%;border-radius:9px;background:linear-gradient(90deg,#3FB27F,#127A4F)}
.q h5{font-size:17px;font-weight:600;line-height:1.35;margin:4px 0 14px;letter-spacing:-.025em}
.q .opt{display:flex;gap:10px;align-items:center;padding:9px 12px 9px 9px;border-radius:13px;border:1px solid var(--line);margin-bottom:7px;background:#fff}
.q .opt .k{width:24px;height:24px;border-radius:8px;display:grid;place-items:center;font-size:12px;font-weight:600;color:var(--soft);background:#F2F4F3;flex:none}
.q .opt .tk{margin-left:auto;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-size:12px;color:#fff;background:var(--test)}
.q .opt.on{border-color:var(--test);background:#EEF7F2;font-weight:600;box-shadow:0 0 0 3px rgba(18,122,79,.12)}.q .opt.on .k{background:var(--test);color:#fff}
.q .qf{display:flex;align-items:center;justify-content:space-between;margin-top:12px;font-size:12.5px;color:var(--faint)}.q .qf .nx{font-weight:600;color:#fff;background:var(--test);padding:7px 14px;border-radius:999px;font-size:13px}
.day .now{font-size:40px;font-weight:300;letter-spacing:-.02em;line-height:1.1;margin:4px 0 2px;font-variant-numeric:tabular-nums}
.day .meta:nth-of-type(2){margin-bottom:14px}
.day .blk{display:flex;gap:12px;align-items:center;padding:10px 12px;border-radius:12px;margin-bottom:6px;background:var(--gray)}
.day .blk span{font-size:12px;font-weight:600;width:62px;color:var(--faint)}
.day .blk.cur{background:var(--ink);color:#fff}.day .blk.cur span{color:#C7C7CC}
.day .blk.meal{background:#FBF4E4}
.day .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:10px;padding-top:10px;border-top:1px solid var(--gray)}
.day .stats div{background:#EEF2FB;border-radius:12px;padding:8px 10px}.day .stats b{display:block;font-size:17px;font-weight:600;color:var(--reset)}.day .stats small{font-size:11.5px;color:var(--faint)}
.kan{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.kan>div{min-width:0}
.kan h4{font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);margin:0 0 8px}
.kan div div{background:var(--gray);border-radius:10px;padding:9px 10px;margin-bottom:7px;line-height:1.3}
.kan div div.hot{background:#FBF4E4;box-shadow:inset 3px 0 0 var(--vault)}.kan div div.int{background:#EEF2FB}
.vt .qlogo svg{box-shadow:0 6px 14px -6px rgba(20,30,60,.6)}.vt .qn{color:#8A5A00;background:#FFF4DE;border-color:#F3DFB4}
.vs{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
.vs div{background:#FBF7EE;border:1px solid #F1E6CF;border-radius:12px;padding:10px 12px}
.vs b{display:block;font-size:20px;font-weight:600;letter-spacing:-.03em;color:var(--vault);line-height:1.1}.vs small{font-size:11.5px;color:var(--soft)}
.vt .kan{margin-bottom:6px}
.vfu{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:13px;border:1px solid #F3DFB4;background:#FFFBF2;margin-bottom:10px}
.vfu .vb{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;background:#FFF1D3;flex:none}
.vfu b{display:block;font-size:13px;font-weight:600}.vfu small{display:block;font-size:11.5px;color:var(--soft)}
.vfu .nx{margin-left:auto;font-weight:600;font-size:12.5px;color:#fff;background:var(--vault);padding:6px 13px;border-radius:999px}
.vai{display:flex;align-items:center;gap:9px;padding:10px 12px;border-radius:999px;background:#F4F5F8;border:1px solid var(--line);font-size:13px;color:var(--ink)}
.vai .sp{color:#6B5BD6;font-size:14px}.vai .tx{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.vai em{font-style:normal;font-size:11px;font-weight:600;color:#6B5BD6;background:#EEEBFF;padding:3px 8px;border-radius:999px}
.kan b{display:block;font-size:12.5px;font-weight:600}.kan small{color:var(--soft);font-size:11px}
.chat{display:grid;gap:8px}
.chat p{padding:9px 12px;border-radius:16px;max-width:86%;line-height:1.35;font-size:13px}
.chat .ai{background:var(--gray)}
.chat .me{justify-self:end;background:var(--accent);color:#fff}
.chat .card{border:1px solid var(--line);border-radius:14px;padding:10px 12px;font-size:12.5px;line-height:1.4}
.chat .card b{display:block;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);margin-bottom:2px}
.chat .card em{font-style:normal;display:table;margin-top:8px;background:var(--accent);color:#fff;border-radius:999px;padding:4px 12px;font-weight:600;font-size:12px}
/* together */
.together{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:112px}
.feat{background:#fff;border:1px solid var(--line);border-radius:24px;padding:30px}
.feat .ic{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;background:#EEF0FA;color:var(--accent);margin-bottom:18px}
.feat .ic svg{width:22px;height:22px}
.feat h3{font-size:20px;font-weight:700;letter-spacing:-.025em;margin-bottom:8px}
.feat p{color:var(--soft);font-size:16px}
@media (max-width:880px){.together{grid-template-columns:1fr}}
/* ai */
.ai-sec{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--line);border-radius:28px;overflow:hidden;background:#fff;margin-bottom:112px}
.ai-sec .l{padding:48px;display:flex;flex-direction:column;justify-content:center}
.ailab{display:inline-flex;align-items:center;gap:10px}.aiic svg{width:36px;height:36px;border-radius:10px;display:block;box-shadow:0 10px 20px -10px rgba(60,50,180,.6)}
.ai-sec .l p:not(.label){font-size:18.5px;color:var(--soft);margin-top:14px}
.ai-sec ul{list-style:none;padding:0;margin:22px 0 0;display:grid;gap:10px}
.ai-sec li{display:flex;gap:10px;font-size:16px;color:var(--soft)}.ai-sec li svg{width:20px;height:20px;flex:none;color:var(--accent);margin-top:2px}
.ai-sec .r{background:#EEF0FA;border-left:1px solid #DCE0F2;padding:40px;display:flex;align-items:center;justify-content:center}
@media (max-width:880px){.ai-sec{grid-template-columns:1fr}.ai-sec .l{padding:28px 22px}.ai-sec .r{padding:28px 18px}}
/* privacy + access */
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:112px}
.two>div{background:#fff;border:1px solid var(--line);border-radius:28px;padding:40px}
.two h3{font-size:26px;font-weight:700;letter-spacing:-.03em;margin-bottom:10px}
.two p:not(.label){color:var(--soft);font-size:17px}
@media (max-width:720px){.two{grid-template-columns:1fr}.two>div{padding:28px 22px}}
/* faq */
.faq{max-width:780px;margin:0 auto 112px;border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;padding:22px 4px;font-size:18px;font-weight:600;letter-spacing:-.02em;display:flex;justify-content:space-between;gap:16px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:26px;font-weight:300;color:var(--accent);transition:transform .25s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details p{padding:0 4px 22px;color:var(--soft)}
/* final + footer */
.final{text-align:center;padding:88px 16px;background:var(--gray);border-top:1px solid var(--line)}
.final .sec-h{margin-bottom:14px}
.final p{font-size:19px;color:var(--soft)}
.picks{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:30px}
.pick{display:inline-flex;align-items:center;gap:10px;padding:10px 18px 10px 10px;border-radius:999px;background:#fff;border:1px solid var(--line);text-decoration:none;font-weight:600;transition:border-color .2s}
.pick:hover{border-color:var(--accent)}
.pick svg{width:30px;height:30px;border-radius:8px}
.builder{margin-top:44px;font-size:15px;color:var(--soft)}.builder a{color:var(--accent);font-weight:600;text-decoration:none}.builder a:hover{text-decoration:underline}
footer{padding:26px 0 40px;color:var(--faint);font-size:14px;border-top:1px solid var(--line);background:var(--gray)}
footer .row{display:flex;flex-wrap:wrap;gap:12px 26px;align-items:center;justify-content:space-between}
footer nav{display:flex;flex-wrap:wrap;gap:6px 18px}footer a{text-decoration:none}footer a:hover{color:var(--ink)}
.film{margin-bottom:112px}
.filmbox{display:block;position:relative;width:100%;max-width:1040px;margin:0 auto;padding:0;border:1px solid var(--line);border-radius:28px;overflow:hidden;background:#0A0F24;cursor:pointer;aspect-ratio:16/9;box-shadow:0 40px 80px -40px rgba(20,30,60,.45);font:inherit}
.filmbox video{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}
.play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:grid;place-items:center;width:92px;height:92px;border-radius:50%;background:rgba(255,255,255,.95);box-shadow:0 0 0 10px rgba(255,255,255,.18),0 20px 44px -12px rgba(0,0,0,.6);transition:transform .25s}
.play i{display:grid;place-items:center}.play svg{width:34px;height:34px;fill:var(--accent);margin-left:5px}
.filmbox:hover .play{transform:translate(-50%,-50%) scale(1.06)}
.filmdlg{padding:0;border:0;background:transparent;width:min(1200px,94vw);max-width:none;overflow:visible}
.filmdlg::backdrop{background:rgba(6,9,19,.9)}
.filmdlg video{width:100%;display:block;border-radius:18px;background:#000;aspect-ratio:16/9}
.fdv{position:relative}
.again{position:absolute;left:0;right:0;bottom:5%;margin:0 auto;width:max-content;z-index:3;display:inline-flex;align-items:center;gap:8px;border:0;cursor:pointer;font:600 15px/1 inherit;color:#1D1D1F;background:rgba(255,255,255,.94);padding:8px 16px 8px 8px;border-radius:999px;box-shadow:0 14px 30px -12px rgba(0,0,0,.7)}
.again svg{width:24px;height:24px;padding:5px;border-radius:50%;background:#2E43A6;color:#fff}.again[hidden]{display:none}
@media (max-width:560px){.again{bottom:3%;font-size:13px;padding:6px 12px 6px 6px}.again svg{width:20px;height:20px;padding:4px}}
.filmdlg .x{position:absolute;top:-54px;right:0;width:44px;height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.16);color:#fff;font-size:28px;line-height:1;cursor:pointer}
@media (max-width:880px){.film{margin-bottom:72px}.filmbox{border-radius:18px}.play{width:68px;height:68px}.play svg{width:26px;height:26px}}
.sep{border:0;height:1px;background:var(--line);width:min(1120px,100% - 32px);margin:0 auto 96px}
.faq details p{max-width:none}
/* app pages */
.pp .label.pc,.pp .head .label{color:var(--pc)}
.pf .label:not(.pc){color:var(--faint)}
.phero{background:var(--tint)}
.phero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center;padding:72px 0 56px}
.crumb{font-size:14px;color:var(--soft);margin-bottom:26px}.crumb a{text-decoration:none;color:var(--soft)}.crumb a:hover{color:var(--ink)}.crumb span{margin:0 6px;color:var(--faint)}
.pname{display:flex;align-items:center;gap:18px}
.pname svg{width:76px;height:76px;border-radius:20px;flex:none;box-shadow:0 18px 36px -20px rgba(20,30,70,.5)}
.pname h1{font-size:clamp(40px,5.4vw,64px);font-weight:700;letter-spacing:-.045em;line-height:1}
.verb{font-size:clamp(18px,2vw,22px);font-weight:600;color:var(--pc);margin-top:6px}
.pp .lead{margin:24px 0 28px}
.aoff,.aoff *{animation-play-state:paused!important}   /* animations only run while their section is on screen */
.phero{overflow:clip}
.showcase .head{max-width:760px}
.sc-grid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:40px;align-items:center;margin-top:28px}
.sc-shot{margin:0;border-radius:18px;overflow:hidden;border:1px solid var(--pline);background:#fff;box-shadow:0 40px 80px -40px rgba(20,30,60,.45)}
.sc-bar{display:flex;align-items:center;gap:6px;padding:10px 14px;background:#F3F4F7;border-bottom:1px solid var(--line)}
.sc-bar i{width:10px;height:10px;border-radius:50%;background:#E0E1E6}.sc-bar i:nth-child(1){background:#FF6159}.sc-bar i:nth-child(2){background:#FFBD2E}.sc-bar i:nth-child(3){background:#28C941}
.sc-bar span{margin-left:10px;font-size:12px;color:var(--faint);background:#fff;border-radius:6px;padding:3px 10px}
.sc-img{position:relative}.sc-img img{display:block;width:100%;height:auto}
.mk{position:absolute;transform:translate(-50%,-50%);width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-size:13px;font-weight:700;color:#fff;background:var(--pc);box-shadow:0 0 0 3px #fff,0 6px 14px -4px rgba(20,30,60,.5);transition:transform .25s cubic-bezier(.22,1,.36,1)}
.mk.on{transform:translate(-50%,-50%) scale(1.35)}
.sc-pts{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.sc-pts li{display:flex;gap:12px;align-items:flex-start;padding:10px 12px;border-radius:14px;cursor:default;transition:background .2s}
.sc-pts li:hover,.sc-pts li:focus,.sc-pts li.on{background:var(--tint);outline:none}
.sc-pts .pn{flex:none;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-size:13px;font-weight:700;color:#fff;background:var(--pc)}
.sc-pts b{display:block;font-size:16px;margin-bottom:2px}.sc-pts li>span:last-child{color:var(--muted);font-size:14.5px;line-height:1.45}
.sc-more{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:26px}
.sc-more b{font-size:14px;margin-right:4px}.sc-more span{font-size:13.5px;padding:6px 12px;border-radius:999px;background:var(--tint);border:1px solid var(--pline);color:var(--ink)}
@media (max-width:880px){.sc-grid{grid-template-columns:1fr;gap:22px}.mk{width:20px;height:20px;font-size:11px;box-shadow:0 0 0 2px #fff}}
/* HV Test: verify + share, partnerships */
.showcase.tall .sc-grid{grid-template-columns:minmax(0,.9fr) minmax(0,1fr);gap:48px}
.showcase.tall .sc-shot{max-width:500px;justify-self:center;width:100%}
.vf{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.vf h2{font-size:clamp(28px,3.4vw,42px);font-weight:700;letter-spacing:-.035em;line-height:1.1;margin-bottom:14px}
.vf .btn{background:var(--pc)}.vf .btn:hover{filter:brightness(.92)}.vf .btn.ghost{background:none;color:var(--pc)}
.vf-steps{list-style:none;margin:26px 0 28px;padding:0;display:grid;gap:14px}
.vf-steps li{display:flex;gap:14px;align-items:flex-start}
.vf-steps li>span{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-weight:700;font-size:14px;color:#fff;background:var(--pc)}
.vf-steps b{display:block;font-size:17px;margin-bottom:2px}.vf-steps div{color:var(--muted);font-size:15.5px;line-height:1.5}
.vf-steps code{font:600 14px/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--ink);background:var(--tint);border:1px solid var(--pline);padding:3px 7px;border-radius:6px;white-space:nowrap}
.vf-card{background:#fff;border:1px solid var(--line);border-radius:24px;padding:30px;box-shadow:0 30px 60px -40px rgba(20,30,60,.35)}
.vf-k{font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-bottom:16px}
.vf-share{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.vf-share span{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:14px;background:var(--tint);border:1px solid var(--pline);font-weight:600;font-size:15px;color:var(--ink)}
.vf-share svg{width:20px;height:20px;flex:none;color:var(--pc)}
.vf-note{margin-top:20px;padding-top:18px;border-top:1px solid var(--line);display:grid;gap:8px}
.vf-note p{font-size:14.5px;color:var(--muted);line-height:1.5;margin:0}.vf-note b{color:var(--ink)}
.pt-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.pt-c{background:#fff;border:1px solid var(--line);border-radius:20px;padding:24px 22px;display:flex;flex-direction:column;gap:10px}
.pt-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:4px}
.pt-ic{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;background:var(--tint);color:var(--pc)}.pt-ic svg{width:22px;height:22px}
.pt-tag{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--pc);background:var(--tint);border:1px dashed var(--pline);padding:4px 10px;border-radius:999px}
.pt-c h3{font-size:18px;font-weight:600;letter-spacing:-.01em}.pt-c p{font-size:15px;color:var(--muted);line-height:1.5}
.pt-small{text-align:center;font-size:14.5px;color:var(--faint);margin-top:24px}
@media (max-width:880px){.showcase.tall .sc-grid{grid-template-columns:1fr;gap:22px}.vf{grid-template-columns:1fr;gap:32px}.vf-card{padding:22px}.pt-grid{grid-template-columns:1fr 1fr}}
@media (max-width:340px){.vf-share{grid-template-columns:1fr}}
@media (max-width:560px){.pt-grid{grid-template-columns:1fr;gap:10px}.pt-c{display:grid;grid-template-columns:44px 1fr;column-gap:14px;row-gap:4px;padding:16px 18px;border-radius:16px}.pt-top{display:contents}.pt-ic{grid-row:1/3}.pt-tag{grid-column:2;grid-row:1;justify-self:start;font-size:10.5px;padding:2px 8px;margin-bottom:2px}.pt-c h3{grid-column:2;font-size:17px}.pt-c p{grid-column:2;font-size:14.5px}}
@media (max-width:420px){.vf-share span{padding:11px 12px;font-size:14px;gap:8px}}

.stage{position:relative;display:flex;justify-content:center;width:100%;max-width:470px;--px:0;--py:0;transform-style:preserve-3d;
  transform:perspective(1600px) rotateX(calc(6deg + var(--py) * -5deg)) rotateY(calc(-12deg + var(--px) * 8deg));transition:transform .6s cubic-bezier(.22,1,.36,1)}
.stage::before,.stage::after{content:"";position:absolute;border-radius:24px;pointer-events:none}
.stage::before{inset:20px -16px -20px 16px;background:linear-gradient(135deg,var(--pc,var(--accent)),transparent 80%);opacity:.18;transform:translateZ(-50px)}
.stage::after{inset:40px -30px -40px 30px;background:linear-gradient(135deg,var(--pc,var(--accent)),transparent 75%);opacity:.08;transform:translateZ(-100px)}
.stage .mock{position:relative;z-index:1;transform:translateZ(0);box-shadow:0 60px 90px -45px rgba(20,30,60,.55),0 18px 36px -24px rgba(20,30,60,.35)}
.chip{position:absolute;z-index:2;display:inline-flex;align-items:center;gap:6px;white-space:nowrap;font-size:13px;font-weight:600;padding:8px 13px;border-radius:999px;background:#fff;color:var(--ink);border:1px solid var(--pline,var(--line));box-shadow:0 14px 30px -14px rgba(20,30,60,.35);transform:translateZ(70px);box-shadow:0 22px 40px -16px rgba(20,30,60,.45)}
.chip.good{background:#EAF7EF;color:#0F6B3A;border-color:#CFE9DA}.chip.warn{background:#FFF4DE;color:#8A5A00;border-color:#F3DFB4}
.chip.c0{top:-16px;left:-22px}.chip.c1{top:42%;right:-30px}.chip.c2{bottom:-16px;left:14%}.vt~.chip.c1{top:31%;right:-30px}
@media (prefers-reduced-motion:no-preference){.stage .mock{animation:bob 8s ease-in-out infinite}.chip{animation:bob 6s ease-in-out infinite}.chip.c1{animation-duration:7s;animation-delay:-2.4s}.chip.c2{animation-duration:6.6s;animation-delay:-4.2s}}
@keyframes bob{50%{translate:0 -9px}}
@media (max-width:880px){.stage{transform:perspective(1400px) rotateX(4deg) rotateY(-7deg)}.stage::before{inset:14px -10px -14px 10px}.stage::after{inset:28px -18px -28px 18px}}
.pmock{display:flex;justify-content:center}.pmock .mock{border-color:var(--pline);box-shadow:0 30px 60px -36px rgba(20,30,60,.4)}
.facts{position:relative;overflow:hidden;display:grid;grid-template-columns:repeat(4,1fr);padding:28px 8px;border-radius:26px;background:#fff;
  background:linear-gradient(120deg,#fff 0%,#fff 35%,color-mix(in srgb,var(--pc) 12%,#fff) 100%);border:1px solid var(--pline);
  box-shadow:0 30px 60px -38px color-mix(in srgb,var(--pc) 60%,transparent)}
.facts::before{content:"";position:absolute;right:-70px;top:-90px;width:300px;height:300px;border-radius:50%;background:color-mix(in srgb,var(--pc) 6%,transparent);pointer-events:none}
.facts::after{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:linear-gradient(var(--pc),color-mix(in srgb,var(--pc) 40%,#fff))}
.facts div{position:relative;padding:0 26px;border-left:1px solid var(--pline)}.facts div:first-child{border-left:0}
.facts b{display:block;font:600 30px/1.15 HVSora,var(--font);letter-spacing:-.04em;color:var(--pc)}.facts span{display:block;font-size:15px;color:var(--soft);margin-top:4px;line-height:1.4}
.pp-sec{padding:96px 0;border-bottom:1px solid var(--line)}
.pp-sec .head{margin-bottom:40px}
.pf{display:grid;grid-template-columns:1fr 1fr;gap:0}
.pf>div{padding:8px 48px 8px 0}.pf>div+div{padding:8px 0 8px 48px;border-left:1px solid var(--line)}
.pf h2{font-size:clamp(28px,3.4vw,40px);font-weight:700;letter-spacing:-.035em;line-height:1.1;margin-bottom:14px}
.pf p:not(.label){font-size:18px;color:var(--soft)}
.more{display:inline-flex;align-items:center;gap:6px;margin-top:18px;color:var(--accent);font-weight:600;text-decoration:none}.more svg{width:16px;height:16px}.more:hover{text-decoration:underline}
.steps3{display:grid;grid-template-columns:repeat(3,1fr);background:#fff;border:1px solid var(--line);border-radius:24px;overflow:hidden}
.st{padding:32px 30px;border-right:1px solid var(--line)}.st:last-child{border-right:0}
.st .n{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--tint);border:1px solid var(--pline);color:var(--pc);font-weight:700;font-size:15px;margin-bottom:18px}
.st h3{font-size:20px;font-weight:700;letter-spacing:-.025em;margin-bottom:6px}.st p{color:var(--soft);font-size:16px}
.fgrid{display:grid;grid-template-columns:repeat(3,1fr);background:#fff;border:1px solid var(--line);border-radius:24px;overflow:hidden}
.ft{padding:28px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);margin:0 -1px -1px 0}
.fic{width:40px;height:40px;border-radius:11px;display:grid;place-items:center;background:var(--tint);border:1px solid var(--pline);color:var(--pc);margin-bottom:16px}.fic svg{width:20px;height:20px}
.ft h3{font-size:17.5px;font-weight:700;letter-spacing:-.02em;margin-bottom:6px}.ft p{color:var(--soft);font-size:15.5px;line-height:1.45}
.who{max-width:880px;margin:0 auto;border-top:1px solid var(--line)}
.wt{display:grid;grid-template-columns:240px 1fr;gap:24px;align-items:baseline;padding:22px 4px;border-bottom:1px solid var(--line)}
.wt b{font-size:22px;font-weight:700;letter-spacing:-.03em}.wt span{color:var(--soft);font-size:18px;line-height:1.45}
.pp .faq{margin-bottom:0}
.pcta{text-align:center;margin-top:40px}
.next{border-bottom:0}.next .label{text-align:center;margin-bottom:22px}
.nxs{display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:820px;margin:0 auto}
.nx{display:flex;align-items:center;gap:16px;padding:18px 20px;background:var(--tint);border:1px solid var(--pline);border-radius:20px;text-decoration:none;transition:transform .25s}
.nx:hover{transform:translateY(-3px)}
.nx>svg:first-child{width:52px;height:52px;border-radius:14px;flex:none}
.nx span{flex:1}.nx b{display:block;font-size:19px;font-weight:700;letter-spacing:-.02em}.nx small{color:var(--pc);font-weight:600;font-size:14.5px}
.nx>svg:last-child{width:20px;height:20px;color:var(--pc)}
.back{text-align:center;margin-top:28px}.back a{display:inline-flex;align-items:center;gap:6px;color:var(--accent);font-weight:600;text-decoration:none}.back svg{width:16px;height:16px}.back a:hover{text-decoration:underline}
@media (max-width:880px){.phero .wrap{grid-template-columns:1fr;padding:44px 0 60px;gap:36px}
  .phero .pmock{padding:40px 0 40px}.phero .pmock .stage{width:calc(100% - 24px)}
  .facts{grid-template-columns:1fr 1fr;padding:6px 4px;border-radius:22px}.facts div{padding:16px 18px}.facts div:nth-child(3){border-left:0}.facts div:nth-child(-n+2){border-bottom:1px solid var(--pline)}
  .pp-sec{padding:64px 0}.pf{grid-template-columns:1fr}.pf>div,.pf>div+div{padding:0}.pf>div+div{border-left:0;border-top:1px solid var(--line);margin-top:32px;padding-top:32px}
  .steps3{grid-template-columns:1fr}.st{border-right:0;border-bottom:1px solid var(--line)}.st:last-child{border-bottom:0}
  .fgrid{grid-template-columns:1fr 1fr}.nxs{grid-template-columns:1fr}}
@media (max-width:560px){.fgrid{grid-template-columns:1fr}.wt{grid-template-columns:1fr;gap:4px;padding:18px 2px}.wt b{font-size:19px}.wt span{font-size:16px}.ft{padding:22px 20px}}
/* phones: pictures first and smaller, compact rows */
@media (max-width:880px){
  .hero{padding:36px 0 28px;gap:44px}.orbit{max-width:290px}.planet span{font-size:12px;padding:4px 10px}
  .strip{margin-bottom:64px}
  .head{margin-bottom:28px}.head h2,.sec-h{font-size:32px}.head p:not(.label){font-size:17px}
  .products{gap:28px;margin-bottom:72px}
  .product .right{padding:52px 18px 46px}
  .product .left{padding:22px 20px 24px;gap:14px}
  .product .top svg{width:48px;height:48px;border-radius:13px}.product h3{font-size:24px}
  .product .pitch{font-size:16.5px}.product li{font-size:15px}.product ul{gap:9px}
  .mock{max-width:360px;padding:15px;border-radius:18px;font-size:13px}
  .mock .qlogo svg{width:28px;height:28px}.mock .qh{margin-bottom:10px}
  .vs b{font-size:17px}.vs div{padding:8px 10px}.vfu{padding:8px 10px}.vai{padding:8px 10px;font-size:12px}.q .opt .k{width:20px;height:20px;font-size:11px}.q .qf{margin-top:8px}
  .chip{font-size:11.5px;padding:6px 10px}.chip.c0{left:10px;top:-16px}.chip.c1{top:auto;bottom:-16px;right:10px}.chip.c2{display:none}.q~.chip.c1{bottom:-26px;right:auto;left:10px}.vt~.chip.c1{top:auto;bottom:-24px;right:10px}.day~.chip.c1{bottom:-24px}
  .q h5{font-size:14.5px;margin:4px 0 10px}.q .opt{padding:7px 10px;margin-bottom:5px;font-size:13px}
  .day .now{font-size:30px}.day .meta:nth-of-type(2){margin-bottom:10px}.day .blk{padding:7px 10px;margin-bottom:5px;font-size:13px}
  .kan b{font-size:11.5px}.kan small{font-size:10px}.kan div div{padding:7px 8px}
  .chat p{font-size:12.5px}.chat .card{font-size:12px}
  .together{gap:10px;margin-bottom:72px}
  .feat{display:grid;grid-template-columns:40px 1fr;column-gap:14px;padding:18px;border-radius:18px}
  .feat .ic{grid-row:span 2;width:40px;height:40px;margin:0}.feat h3{font-size:17px;margin-bottom:4px}.feat p{font-size:15px}
  .ai-sec,.two{margin-bottom:72px}.ai-sec .r{border-left:0;padding:24px 16px}
  .sep{margin-bottom:64px}.faq{margin-bottom:72px}.faq summary{font-size:16.5px;padding:18px 2px}
  .final{padding:60px 16px}
  .phero .wrap{padding:28px 0 36px;gap:24px}.pname svg{width:60px;height:60px;border-radius:16px}.pname{gap:14px}
  .pp .lead{margin:18px 0 22px;font-size:17px}.crumb{margin-bottom:18px}
  .facts{margin-top:0}.factband{padding-bottom:44px}.facts b{font-size:21px}.facts span{font-size:13px}
  .pp-sec{padding:56px 0}.pp-sec .head{margin-bottom:24px}
  .pf h2{font-size:26px}.pf p:not(.label){font-size:16.5px}
  .st{display:grid;grid-template-columns:34px 1fr;column-gap:14px;padding:18px}
  .st .n{grid-row:span 2;margin:0}.st h3{font-size:17px;margin-bottom:2px}.st p{font-size:15px}
  .ft{display:grid;grid-template-columns:38px 1fr;column-gap:14px;padding:18px}
  .fic{grid-row:span 2;width:38px;height:38px;margin:0}.ft h3{font-size:16px;margin-bottom:3px}.ft p{font-size:14.5px}
  .wt b{font-size:18px}.wt span{font-size:15.5px}
  .nx>svg:first-child{width:44px;height:44px}.nx b{font-size:17px}
}
/* section bands: every section gets its own full-width background, alternating, with a hairline edge */
.band{position:relative;padding:96px 0}
.band-w{background:#FFFFFF;box-shadow:0 0 0 100vmax #FFFFFF;clip-path:inset(0 -100vmax)}
.band-g{background:#F2F3F7;box-shadow:0 0 0 100vmax #F2F3F7;clip-path:inset(0 -100vmax)}
.band::before{content:"";position:absolute;top:0;left:50%;width:100vw;margin-left:-50vw;height:1px;background:var(--line)}
html{overflow-x:clip}
.band .products,.band .together,.band .ai-sec,.band .two,.band .faq,.band.film{margin-bottom:0}
.band-g .feat,.band-g .two>div{background:#fff}
.band-w .feat,.band-w .two>div{background:#F7F8FA}
.final{background:#FFFFFF}
.factband{background:var(--tint);border-bottom:1px solid var(--pline);display:flow-root;padding:0 0 72px}
.lib{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.lrow{display:flex;gap:18px;align-items:stretch}
.lcat{--gc:#127A4F;--gt:rgba(18,122,79,.045);flex:var(--n) 1 0;min-width:0;display:flex;flex-direction:column;border:2px dotted var(--gc);border-radius:26px;background:var(--gt);padding:16px 16px 18px}
.lcat.ai{--gc:#6D4FD6;--gt:rgba(109,79,214,.06);background:var(--gt) radial-gradient(rgba(109,79,214,.16) 1px,transparent 1.4px) 0 0/14px 14px}
.lcat .lch{color:var(--gc);margin:2px 4px 14px;flex-wrap:wrap;row-gap:2px;white-space:nowrap}
.lcat.ai{flex:1.25 1 0}
.lcards{flex:1;display:grid;grid-template-columns:repeat(var(--n),1fr);gap:12px}
.lcat.ai .lc .lb{background:#ECE7FB;color:#5B3FC4}
.lcat.ai .lc h3{color:#2E2359}
@media (max-width:980px){.lrow{flex-direction:column}.lcards{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.lcards{grid-template-columns:1fr}}
.lch{display:flex;align-items:baseline;gap:10px;font-size:14px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--pc);margin:0 0 14px}
.lch span{font-size:13px;font-weight:500;letter-spacing:0;text-transform:none;color:var(--faint)}
.lc{position:relative;background:#fff;border:1.5px solid var(--pc);border-radius:20px;padding:24px 22px;box-shadow:0 18px 40px -28px rgba(20,30,60,.35)}
.lc.soon{border:1px solid #E3E6EE;box-shadow:none;background:#FFFFFF}
.lc .lb{display:inline-block;font-size:12.5px;font-weight:700;letter-spacing:.04em;padding:4px 11px;border-radius:999px;color:#fff;background:var(--pc);margin-bottom:14px}
.lc.soon .lb{color:var(--soft);background:#EDEFF4}
.lc h3{font-size:19px;font-weight:700;letter-spacing:-.02em;margin-bottom:6px}.lc p{color:var(--soft);font-size:15.5px;line-height:1.45}
.lc.soon h3{color:#3A3F4B}
@media (max-width:980px){.lib{grid-template-columns:1fr 1fr}}@media (max-width:560px){.lib{grid-template-columns:1fr}}
.pp-sec{background:#F2F3F7}.pp-sec:nth-of-type(odd){background:#FFFFFF}
.pp-sec:nth-of-type(even) .steps3,.pp-sec:nth-of-type(even) .fgrid{background:#fff}
@media (max-width:880px){.band{padding:64px 0}}
/* reveal */
@media (prefers-reduced-motion:no-preference){.rv{opacity:0;transform:translateY(20px);transition:opacity .7s ease,transform .7s cubic-bezier(.22,1,.36,1)}.rv.in{opacity:1;transform:none}}

/* phones: heading and a short line first, then the picture, then the points and buttons */
@media (max-width:880px){
  .product{display:flex;flex-direction:column}
  .product .left,.product.flip .left{display:contents}
  .product .top{order:1;padding:24px 20px 0}
  .product .pitch{order:2;padding:12px 20px 22px}
  .product .right,.product.flip .right{order:3;border-top:1px solid var(--pline);border-bottom:1px solid var(--pline)}
  .product ul{order:4;padding:22px 20px 0}
  .product .acts{order:5;padding:18px 20px 26px;margin-top:0}
  .ai-sec{display:flex;flex-direction:column}
  .ai-sec .l{display:contents}
  .ai-sec .l>.label{order:1;padding:26px 20px 0}
  .ai-sec .l>h2{order:2;padding:0 20px}
  .ai-sec .l>p:not(.label){order:3;padding:0 20px 22px}
  .ai-sec .r{order:4;border-top:1px solid #DCE0F2;border-bottom:1px solid #DCE0F2}
  .ai-sec .l>ul{order:5;padding:20px 20px 26px;margin:0}
}
"""

OVERVIEW_MAIN = """<main id="main">
  <section id="top" class="wrap hero">
    <div class="rv">
      <p class="eyebrow">Free for everyone</p>
      <h1>Your work, your day, your growth. <span>One calm world.</span></h1>
      <p class="lead">Consistency is the key, and it's easier with the right direction and the right tools. Know yourself with HV Test, stay consistent with HV Reset, and keep every opportunity in HV Vault. Just tell HV AI what you need.</p>
      <div class="ctas"><a class="btn" href="#apps">Explore the apps</a><a class="btn ghost" href="/story/">Watch Riya's story __ARROW__</a></div>
      <p class="note">Nothing to install. Works on your phone and laptop.</p>
    </div>
    <div class="orbit rv" aria-hidden="true">
      <div class="ring"></div><div class="ring r2"></div>
      <div class="core">__LOGO_WORLD__</div>
      <a class="planet p1" href="/test/" tabindex="-1">__LOGO_TEST__<span>HV Test</span></a>
      <a class="planet p2" href="/reset/" tabindex="-1">__LOGO_RESET__<span>HV Reset</span></a>
      <a class="planet p3" href="/vault/" tabindex="-1">__LOGO_VAULT__<span>HV Vault</span></a>
    </div>
  </section>

  <div class="wrap strip facts rv">
    <div><b>3 apps</b><span>know yourself, plan your day, land the job</span></div>
    <div><b>Free</b><span>for everyone, HV AI included</span></div>
    <div><b>Just talk</b><span>type or speak, in your language</span></div>
    <div><b>Any device</b><span>phone and laptop, one sign&#8209;in</span></div>
  </div>

  <section id="film" class="wrap film band band-w">
    <div class="head rv"><p class="label">The product</p><h2>See HV World in action.</h2><p>Real screens from all three apps.</p></div>
    <button type="button" class="filmbox rv" id="filmOpen" aria-label="Play the HV World video">
      <video id="loopVid" poster="/media/hv-world-loop-poster.jpg" muted loop playsinline autoplay preload="auto" aria-hidden="true" tabindex="-1"><source src="/media/hv-world-loop.mp4" type="video/mp4"><source src="/media/hv-world-loop.webm" type="video/webm"></video>
      <span class="play"><i><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12.5-7.5z"/></svg></i></span>
    </button>
  </section>

  <section id="apps" class="wrap band band-g">
    <div class="head rv"><p class="label">The apps</p><h2>Three apps. Each does one job well.</h2><p>Open any of them in your browser. Nothing to install.</p></div>
    <div class="products">__PRODUCTS__</div>
  </section>

  <section id="together" class="wrap band band-w">
    <div class="head rv"><p class="label">Better together</p><h2>Use one. Or let them work as a team.</h2><p>Each app stands on its own. Together, your plan and your progress stay in step.</p></div>
    <div class="together">
      <div class="feat rv"><div class="ic">__CHAIN__</div><h3>Reset and Vault, better together</h3><p>Use both with the same Google account and HV Reset shows your HV Vault follow-ups and weekly numbers right next to your day.</p></div>
      <div class="feat rv"><div class="ic">__USER__</div><h3>One Google sign-in</h3><p>Sign in with Google and your plans, dashboard and data follow you. Your phone and laptop show the same thing.</p></div>
      <div class="feat rv"><div class="ic">__SPARK__</div><h3>HV AI in each app</h3><p>In HV Vault it handles jobs, follow-ups and interviews. In HV Reset it builds and adjusts your day, and your dashboard shows how it went. Each one changes only its own app.</p></div>
    </div>
  </section>

  <section id="ai" class="wrap band band-g">
    <div class="ai-sec rv">
      <div class="l">
        <p class="label ailab"><span class="aiic">__LOGO_AI__</span>HV AI</p>
        <h2 class="sec-h">Just say it. HV AI does the work.</h2>
        <p>Type, or hold the mic and talk the way you normally do. HV AI turns it into clear changes you check before anything is saved.</p>
        <ul>
          <li>__CHECK__Hindi, English or Hinglish, typed or spoken</li>
          <li>__CHECK__Every change is a card: Confirm, Edit or Cancel</li>
          <li>__CHECK__Deletes always ask first. Unclear names get a question, not a guess</li>
          <li>__CHECK__Undo the last change any time</li>
          <li>__CHECK__Built in: no key, no setup</li>
        </ul>
      </div>
      <div class="r">__MOCK_AI__</div>
    </div>
  </section>

  <section id="access" class="wrap band band-w"><div class="two">
    <div class="rv"><p class="label">Privacy</p><h3>Your data is yours.</h3><p>HV Vault saves everything to your own private space, linked to your Google account. Only you can read it. HV Test never stores your answers: they stay in your browser. Only a short scorecard summary is saved, if you ask for one.</p></div>
    <div class="rv"><p class="label">Open to all</p><h3>Made for everyone.</h3><p>All three apps and HV AI are free for everyone. Open them in any browser, with nothing to install and no ads in your way.</p></div>
  </div></section>

  <section id="faq" class="wrap band band-g">
    <div class="head rv"><p class="label">FAQ</p><h2>Questions, answered.</h2></div>
    <div class="faq rv">__FAQ__</div>
  </section>

  <section class="final">
    <div class="wrap rv">
      <h2 class="sec-h">Pick one. It takes a minute.</h2>
      <p>Start with the app you need most. The others are one click away.</p>
      <div class="picks">
        <a class="pick" href="__U_TEST__">__LOGO_TEST_P__HV Test</a>
        <a class="pick" href="__U_RESET__">__LOGO_RESET_P__HV Reset</a>
        <a class="pick" href="__U_VAULT__">__LOGO_VAULT_P__HV Vault</a>
      </div>
      <p class="builder">Designed and built by Harsh Goyal · <a href="https://www.linkedin.com/in/harshvittori" target="_blank" rel="noopener">Connect on LinkedIn</a></p>
    </div>
  </section>
  <dialog id="filmDlg" class="filmdlg" aria-label="HV World in action">
    <button type="button" class="x" id="filmClose" aria-label="Close the video">×</button>
    <div class="fdv"><button type="button" class="again" id="filmAgain" hidden aria-label="Watch again"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg><span>Watch again</span></button>
    <video id="filmVid" controls playsinline preload="none" poster="/media/hv-world-poster.jpg"><source src="/media/hv-world-film.mp4" type="video/mp4"><source src="/media/hv-world-film.webm" type="video/webm"></video></div>
  </dialog>
</main>"""

# ---------------------------------------------------------------- icons for the feature grids
ICONS = {
 'GRID': '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 'BOARD': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 4v16"/>',
 'BRIEF': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
 'BELL': '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 8 3 8H3s3-1 3-8"/><path d="M10 20a2 2 0 0 0 4 0"/>',
 'CAL': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
 'WAND': '<path d="M15 4V2M15 10V8M11 6h2M17 6h2M4 20l10-10"/><path d="M18.5 12.5l1 1M20 16l1.5.5"/>',
 'USER': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 'FILE': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
 'MSG': '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-5A8 8 0 1 1 21 12z"/>',
 'LIST': '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>',
 'TARGET': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/>',
 'CHART': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 'CLOUD': '<path d="M7 18a5 5 0 1 1 .8-9.9A6 6 0 0 1 19 9.5a4.3 4.3 0 0 1-1 8.5z"/>',
 'CLOCK': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'ROUTE': '<circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.5 19H16a3.5 3.5 0 0 0 0-7H8a3.5 3.5 0 0 1 0-7h7.5"/>',
 'PAUSE': '<path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
 'CUP': '<path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 3v3M12 3v3"/>',
 'NOTE': '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
 'SUN': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 'SHUFFLE': '<path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/>',
 'SHIELD': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 'HEART': '<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21.5l8.8-8.8a5 5 0 0 0 0-7.1z"/>',
 'SPARK': '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',
 'SYNC': '<path d="M21 12a9 9 0 0 1-15.5 6.2M3 12A9 9 0 0 1 18.5 5.8"/><path d="M18.5 2v4h-4M5.5 22v-4h4"/>',
 'FLAME': '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.4 1.3-3.8 2.5-5 .3 2 1.3 3 2.5 3.4C11.4 9 11 6.2 12 3z"/>',
 'BULB': '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9V16h7v-2.1A6 6 0 0 0 12 3z"/>',
 'CHECKC': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16.5 9"/>',
}


# ---------------------------------------------------------------- HV Test: verify + share, and institute partnerships
SAMPLE_ID = "HVT-MA-68SM-E8LJ"
VERIFY_URL = "https://harshvittori.github.io/hv-tests/verify/"
SHARE = [("Portfolio", '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/>'),
         ("Resume", '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>'),
         ("LinkedIn", '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M8 10v7M8 7v.5M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/>'),
         ("Instagram", '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5v.5"/>'),
         ("WhatsApp", '<path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c.5 2 2.5 4 4.5 4.5l1-1.2 2 .8-.4 1.6c-3.8.4-7.6-3.4-7.2-7.2l1.6-.4.8 2z"/>'),
         ("Job applications", '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M3 12h18M10 12v2h4v-2"/>')]
VERIFY_HTML = '''
  <section class="pp-sec" id="verify"><div class="wrap vf">
    <div class="rv">
      <p class="label pc">Unique and checkable</p>
      <h2>Every scorecard has its own ID. Anyone can check it.</h2>
      <p>When you save your scorecard, HV Test gives it a unique ID and a QR code, and keeps a locked copy of the result. Anyone you share it with can scan the code, or enter the ID, and see the record exactly as HV Test issued it.</p>
      <ol class="vf-steps">
        <li><span>1</span><div><b>Save your scorecard</b>You get an ID like <code>HVT-MA-68SM-E8LJ</code> and a QR code.</div></li>
        <li><span>2</span><div><b>Share it</b>Add the image or PDF wherever people should see it.</div></li>
        <li><span>3</span><div><b>They check it</b>A scan opens the HV Test verify page with the real record. It can't be edited.</div></li>
      </ol>
      <div class="ctas"><a class="btn" href="https://harshvittori.github.io/hv-tests/verify/">Check a scorecard __ARROW__</a><a class="btn ghost" href="https://harshvittori.github.io/hv-tests/verify/#HVT-MA-68SM-E8LJ">Try the sample ID</a></div>
    </div>
    <div class="rv vf-card">
      <p class="vf-k">Share it where it counts</p>
      <div class="vf-share">__SHARE__</div>
      <div class="vf-note">
        <p><b>It confirms</b> HV Test issued this scorecard, and the name, date and scores are exactly as saved.</p>
        <p><b>It doesn't claim</b> to be an accredited certification. It's an honest self-assessment, issued by HV Test.</p>
      </div>
    </div>
  </div></section>''' % {"id": SAMPLE_ID, "v": VERIFY_URL}
PARTNERS = [("Colleges and universities", "Bring HV Test to students before placements and first interviews.", '<path d="M3 9l9-5 9 5-9 5z"/><path d="M7 11v5c0 1.5 2.2 3 5 3s5-1.5 5-3v-5M21 9v6"/>'),
            ("Training institutes", "Add HV Test to courses, so learners can see their real growth.", '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4M7 9l3 2 4-4 3 2"/>'),
            ("Skill programmes", "Measure where people start, and how far they come by the end.", '<path d="M4 19h16M7 16V11M12 16V7M17 16v-3"/>'),
            ("Hiring partners", "Help employers understand candidates beyond a resume.", '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>')]
PARTNER_HTML = '''
  <section class="pp-sec partner"><div class="wrap">
    <div class="head rv"><p class="label pc">Coming soon</p><h2>Partnering with top institutes.</h2>
      <p>We're working towards partnerships with leading colleges, universities and training institutes, so your HV Test scorecard carries even more weight where it matters.</p></div>
    <div class="pt-grid rv">__PARTNERS__</div>
    <p class="pt-small rv">Today HV Test is independent, and scorecards are issued by HV Test alone. We'll share partners here as they join.</p>
  </div></section>'''

# ---------------------------------------------------------------- one page per app
APPS = {
 "test": dict(name="HV Test", verb="Know yourself", color="#127A4F", tint="#EEF6F1", pline="#D3E7DA", mock=MOCK_TEST, cta="Take a test", story="/#test",
   showcase=dict(img="/test/scorecard.jpg", w=1080, h=1350, id="scorecard", label="Your scorecard", tall=True,
     title="A real scorecard, not just a number.", lead="Finish the Maturity Assessment and get a one-page Skill Assessment Scorecard: your score, level and marks for every skill, ready to save, share and check.",
     alt="A sample HV Test Skill Assessment Scorecard: Riya Verma (Sample), Maturity Assessment, 72 out of 100, Grounded, skill-wise marks, strengths, work on, scorecard ID and QR code",
     points=[(3.6, 20.4, "Your name and test", "The name you choose, the test and its category."),
             (91.5, 17.0, "Score out of 100 and level", "Developing, Emerging, Grounded or Highly Consistent."),
             (50.0, 39.4, "A unique scorecard ID", "Every scorecard gets its own ID, like HVT-MA-68SM-E8LJ, the day you save it."),
             (6.7, 47.3, "Marks for every skill", "All 10 skills out of 10, so strengths and gaps are clear at a glance."),
             (54.6, 47.3, "Strengths and what to work on", "Your top three and the three to grow next."),
             (6.7, 86.0, "QR code to verify", "Anyone can scan it and see the real record."),
             (3.6, 93.6, "Honest by design", "Issued by HV Test. A self-assessment, not an accredited certification.")]),
   after_show=VERIFY_HTML,
   before_faq=PARTNER_HTML,
   title="How well do you really know yourself? | HV Test",
   desc="Tests for how you think, learn, act and grow. Start with the free Maturity Assessment: an honest score, a checkable scorecard, a full report and a 30-day plan. No login.",
   lead="One place to understand yourself: how you handle life, your real strengths, how you communicate, how consistent you are, and how well you use AI. Take a test, see where you stand, and keep growing.",
   facts=[("10 min", "real-life situations, no right answers"), ("10 skills", "each scored out of 10"), ("Checkable", "scorecard with a unique ID and QR"), ("Free", "no login, answers stay on your device")],
   problem=("“So, what are your strengths?”", "Most of us have never measured how we think, learn or react. So in an interview, a review or a big decision, we guess."),
   fix=("See yourself clearly. Then grow.", "HV Test measures your traits, abilities and habits with honest, carefully designed tests. You see where you stand, what to improve, and how you change over time."),
   steps=[("Pick a test", "Choose what you want to understand. Start with the Maturity Assessment: about 10 minutes."),
          ("Answer honestly", "Real situations and questions, with no right answers to game. Pick what you'd really do."),
          ("See where you stand, then grow", "Your scorecard, a report and a plan. Share the scorecard, and retake later to see how you've grown.")],
   library=[("Maturity Assessment", "Live now", "How you decide, handle emotions and act in real-life situations. A score out of 100, a scorecard, a full report and a 30-day plan.", "Personal Growth"),
            ("Strengths Finder", "Coming soon", "Find what you are naturally good at, and how to talk about it in an interview.", "Personal Growth"),
            ("Communication Style", "Coming soon", "How clearly you speak, listen and explain, with a 7-day practice plan.", "Personal Growth"),
            ("Consistency Check", "Coming soon", "Why you start strong and then stop, and a simple plan to keep going.", "Personal Growth"),
            ("AI Basics", "Coming soon", "How well you understand and use AI, and when to double-check its answers.", "AI & Future Skills")],
   feats=[("CHECKC", "Maturity Assessment, live now", "The first test on HV Test: how you think, react and decide in real life. About 10 minutes."),
          ("SHUFFLE", "Real-life situations", "A bank of 104 situations. Each attempt picks 28 to 30, covering all 10 areas."),
          ("GRID", "10 areas", "Emotional control, accountability, self-awareness, conflict, relationships, decisions, patience, empathy, responsibility, long-term thinking."),
          ("TARGET", "Score out of 100", "Your overall score and a level: Developing, Emerging, Grounded or Highly Consistent."),
          ("CHECKC", "Skill Assessment Scorecard", "One page with your score, level and marks for every skill. Save it as an image or PDF."),
          ("SHIELD", "Unique ID and QR code", "Every saved scorecard gets its own ID. Anyone can scan the QR code to check it's real."),
          ("FILE", "Full report PDF", "About 12 pages on each area, opening with your scorecard."),
          ("ROUTE", "30-day plan PDF", "About 10 pages of small daily steps. Download both PDFs in one tap."),
          ("SYNC", "Fresh every time", "Questions and options are shuffled, and a retake avoids the ones you saw last time."),
          ("HEART", "Private by design", "No login. Your answers never leave your device. Only a short scorecard summary is saved, and only if you ask."),
          ("BULB", "Honest, not a quiz", "Four believable options with real trade-offs. It's for growth, not a diagnosis.")],
   who=[("Students", "Know your strengths before placements and first interviews."),
        ("Job seekers", "Real answers, with real examples, for “tell me about yourself”."),
        ("Professionals", "See how you handle conflict, pressure and feedback at work."),
        ("Team leads", "Understand your own patterns before you guide others."),
        ("Career switchers", "Check what you bring to a new field, beyond your old job title."),
        ("Anyone curious", "A calm look at yourself, and small steps to grow.")],
   faq=[("What tests are on HV Test?", "Personal Growth: the Maturity Assessment (live now), Strengths Finder, Communication Style and Consistency Check. AI and Future Skills: AI Basics. The new ones are coming soon."),
        ("Is there a test about AI?", "Yes. AI Basics, in the new AI and Future Skills category, is coming soon: how well you understand and use AI, and when to double-check it."),
        ("Is HV Test a diagnosis?", "No. It's a self-assessment for personal growth, not a clinical or psychological diagnosis."),
        ("What is the scorecard?", "A one-page Skill Assessment Scorecard with your score, level and marks for every skill. It's issued by HV Test and it's a self-assessment, not an accredited certification or qualification."),
        ("How can someone check my scorecard?", "They scan its QR code, or enter its ID at harshvittori.github.io/hv-tests/verify. They'll see the record exactly as HV Test saved it. Records can't be edited."),
        ("Is HV Test partnered with any institute?", "Not yet. We're working towards partnerships with colleges, universities and training institutes. Today, scorecards are issued by HV Test alone."),
        ("Do I need an account?", "No. There's no login, and your answers never leave your browser. If you save a scorecard, only its short summary is stored."),
        ("Can I take it again?", "Yes. Questions and options are shuffled, and a retake avoids the questions you saw last time."),
        ("Who can take it?", "Anyone. The Maturity Assessment is free for everyone, both PDFs included.")]),
 "reset": dict(name="HV Reset", verb="Plan your day. See your progress.", color="#4A72C8", tint="#EEF2FB", pline="#D6E0F4", mock=MOCK_RESET, cta="Open HV Reset", story="/#reset",
   showcase=dict(img="/reset/dashboard.jpg", w=1440, h=1002, id="dashboard", label="The dashboard", bar="harshvittori.github.io/hv-reset",
     alt="The HV Reset dashboard: today at a glance, three questions answered, key numbers, productivity score, a 14-day trend and tips",
     title="Your personal dashboard", lead="See what you planned, what you really did, and whether you're getting better. Every number comes from what you actually do. Nothing is made up.",
     points=[(17.9, 14.4, "Today at a glance", "Tasks done, time worked and what's next, with one tap back to your day."),
             (17.9, 25.6, "Three honest answers", "What am I doing with my time? Am I completing what I plan? Am I improving?"),
             (17.9, 39.1, "Four numbers that matter", "Tasks completed, time worked, started on time and your streak, each compared with last time."),
             (17.9, 59.4, "A fair productivity score", "One score from six parts you can see and adjust. Longer hours never count as better."),
             (60.9, 59.4, "Your last 14 days", "A simple trend of how much of your plan you finished each day."),
             (17.9, 85.3, "Worth a look", "One timely alert and one tip from your own patterns, never judgement."),
             (8.5, 80.0, "15 deeper views", "Time, focus, punctuality, calendar, goals, reports and more, one tap away.")],
     more=["Time tracking", "Focus", "Punctuality & delays", "Day timeline", "Trends", "Calendar heatmap", "Workload", "Goals & habits", "Daily, weekly, monthly reports", "Timer history"]),
   title="Plan your day and see where your time goes | HV Reset",
   desc="One task at a time, a day that moves when you're late, and a personal dashboard for your time, focus, streaks and progress. Free, in your browser.",
   lead="Plan your day, do one task at a time, and see what you really did. Your own dashboard shows where your time goes and whether you're getting better.",
   facts=[("1 sentence", "and HV AI plans your whole day"), ("1 tap", "shifts your day when you're late"), ("Dashboard", "time, focus, streaks and score"), ("Free", "in your browser, nothing to install")],
   problem=("“Where did my day go?”", "Busy all day, but you can't say what got done. Plans slip, and you never really know if you're improving."),
   fix=("Plan it. Do it. See it.", "HV Reset shows one task at a time and moves your day when you're late. Then your dashboard shows the real picture: time spent, focus, what started on time, and your progress week after week."),
   steps=[("Make your plan", "Add tasks with a time, pick a ready plan, or just tell HV AI how your day looks."),
          ("Press Start", "The clock shows what's on now. Pause when you step away. Running late? One tap moves the rest of the day."),
          ("See your progress", "Your dashboard shows your time, focus, streaks and score, with tips from your own patterns.")],
   feats=[("TARGET", "One task at a time", "Only the task in front of you, with the time left and what's up next."),
          ("CLOCK", "Focus clock with pause", "A calm countdown for each task. Pause when you step away, and the time waits for you."),
          ("ROUTE", "Running late? Shift the day", "Start late or early and one tap moves the rest of your day. Nothing gets lost."),
          ("GRID", "Your personal dashboard", "Time worked, focus, punctuality and streaks at a glance. Tap any number to see the tasks behind it."),
          ("CHART", "A score that's fair", "One productivity score built from six parts you can see and adjust. Longer hours don't count as better."),
          ("LIST", "Where your time really goes", "Planned vs actual time for every task, a 24-hour timeline, and which tasks always take longer."),
          ("FLAME", "Streaks, goals and habits", "Set your own goals, track habits and beat your personal records."),
          ("BULB", "Tips from your own patterns", "“You finish most tasks between 9 and 12.” Plain insights and gentle alerts, never judgement."),
          ("NOTE", "Daily, weekly and monthly reports", "What you did, what's left and what needs attention, ready to copy and share."),
          ("SUN", "Music that follows the day", "Soft ambient sound for morning, day focus, evening and night, based on the time of day."),
          ("SPARK", "HV AI plans your day", "“Kal subah 6 baje gym, 10 se 1 padhai, shaam 7 baje family time.” It builds the plan and keeps your exact times."),
          ("SYNC", "Better with HV Vault", "Use HV Vault too? Sign in to both with the same Google account and your follow-ups due and weekly numbers show up next to your day.")],
   who=[("Students", "Study blocks, real breaks, and a clear view of how much you really studied."),
        ("Parents and homemakers", "School runs, home, work and a little time for yourself, in one calm day."),
        ("Professionals", "Protect deep work between meetings and see where the hours go."),
        ("Freelancers", "Client work, admin and rest, balanced in one day."),
        ("Creators", "Make, edit and post in focused sessions."),
        ("Anyone restarting", "Missed your plan? Lost your routine? Hit reset and start fresh today.")],
   faq=[("Do I have to plan every task myself?", "No. Pick a ready plan and change it, or tell HV AI your day in one sentence and it builds the plan."),
        ("What happens if I fall behind?", "Tap to shift the rest of the day, pause the task, move it to tomorrow, or do a shorter version."),
        ("What does the dashboard show?", "Your time, focus, punctuality, streaks, a productivity score, trends, a calendar heatmap, goals and habits, and daily, weekly and monthly reports. Every number comes from what you really did, and nothing is made up."),
        ("Do I need an account?", "No. Try it freely. Sign in with Google to save your plan, keep your dashboard history, and use it on phone and laptop."),
        ("Does it work with HV Vault?", "Yes, if you use both. HV Reset works fully on its own. If you also use HV Vault with the same Google account, HV Reset shows your follow-ups due and this week's numbers from it, and HV AI knows about them."),
        ("Who can use it?", "Everyone. It's free for everyone, HV AI included, and runs right in your browser.")]),
 "vault": dict(name="HV Vault", verb="Act on every opportunity", color="#A87A22", tint="#F8F3E8", pline="#EADDC2", mock=MOCK_VAULT, cta="Open HV Vault", story="/#vault",
   title="Stop losing job leads in WhatsApp chats | HV Vault",
   desc="Every job, recruiter and interview on one board. Follow-ups set themselves. Just tell the AI what happened.",
   lead="Every job, company, follow-up and interview in one calm place, so nothing slips. Just tell HV AI what happened.",
   facts=[("1 board", "every job, Saved to Offer"), ("Auto", "follow-ups set the day you apply"), ("Just say it", "HV AI adds interviews and updates"), ("Any device", "synced, with Excel export")],
   problem=("“Did I ever follow up?”", "Links in chats, five versions of a resume, sticky notes everywhere. The good opportunities go quiet."),
   fix=("Nothing slips anymore.", "HV Vault puts every opportunity on one board and reminds you on time. Say “Kal 4 baje interview” and it's on the calendar."),
   steps=[("Sign in and upload", "Sign in with Google and upload your resume. Your profile fills itself in."),
          ("Save as you find", "Paste a job post, a PDF or a screenshot, and HV AI fills in the details."),
          ("Move it forward", "Drag each job along your board. Follow-ups, interviews and your weekly numbers take care of themselves.")],
   feats=[("GRID", "Dashboard", "Your day at a glance: what's due, upcoming interviews and this week's numbers."),
          ("BOARD", "Pipeline board", "Every job is a card. Drag it from Saved to Applied, Interview and Offer."),
          ("BRIEF", "Jobs and companies", "Links, salary, location, notes and contacts for every role and company."),
          ("BELL", "Automatic follow-ups", "Mark a job Applied and the first follow-up is scheduled. See what's due or overdue."),
          ("CAL", "Calendar", "Interviews, calls and deadlines in a month view and a list."),
          ("WAND", "AI auto-fill", "Paste a job post, upload a PDF or add a screenshot. The details fill themselves in for you to check."),
          ("USER", "Profile from your resume", "Upload it once. Name, role, skills, experience and education are filled in."),
          ("FILE", "Resume Vault", "Every version of your resume together, and which one you sent where."),
          ("MSG", "Message templates", "Ready messages for referrals, follow-ups and thank-yous, with your name and links."),
          ("TARGET", "2-minute apply rule", "A quick check on each job: right role, experience and city? Apply with confidence, or skip."),
          ("CHART", "Analytics", "Applications per week, response rate and how your pipeline is moving."),
          ("CLOUD", "Sync and backup", "The same data on phone and laptop. Export to Excel or download a full backup.")],
   who=[("Job seekers", "Every application, follow-up and interview in one place."),
        ("Students", "Internships and placement drives, tracked from first form to offer."),
        ("Career switchers", "New companies, new contacts, and a record of what's working."),
        ("Experienced hires", "Referrals, recruiters and senior roles, without the spreadsheet."),
        ("Freelancers", "Companies, contacts and follow-ups for the clients you pitch."),
        ("Mentors", "A clear structure to share with the people you guide.")],
   faq=[("Do I need an account?", "Yes, a Google sign-in, so your data is private to you and follows you across devices."),
        ("Can I get my data out?", "Yes. Export to Excel or download a full backup any time."),
        ("Do I need to set up HV AI?", "No. It's built in: no key, no setup. Every change shows as a card you confirm."),
        ("Who can use it?", "Everyone with a Google account. It's free for everyone.")]),
}
ORDER = ["test", "reset", "vault"]

def icon(k):
    return I(ICONS[k])

def app_page(key):
    a = APPS[key]
    facts = "".join('<div><b>%s</b><span>%s</span></div>' % f for f in a["facts"])
    steps = "".join('<div class="st rv"><span class="n">%d</span><h3>%s</h3><p>%s</p></div>' % (i + 1, h, p) for i, (h, p) in enumerate(a["steps"]))
    feats = "".join('<div class="ft"><div class="fic">%s</div><h3>%s</h3><p>%s</p></div>' % (icon(k), h, p) for k, h, p in a["feats"])
    who = "".join('<div class="wt"><b>%s</b><span>%s</span></div>' % w for w in a["who"])
    faq = "".join('<details><summary>%s</summary><p>%s</p></details>' % qa for qa in a["faq"])
    lib = ""
    if a.get("library"):
        groups = {}
        for t, st, d, c in a["library"]:
            groups.setdefault(c, []).append('<div class="lc%s"><span class="lb">%s</span><h3>%s</h3><p>%s</p></div>' % ("" if st == "Live now" else " soon", st, t, d))
        cards = '<div class="lrow">' + "".join('<div class="lcat%s" style="--n:%d"><h3 class="lch">%s<span>%d test%s</span></h3><div class="lcards">%s</div></div>' % (" ai" if "AI" in c else "", len(v), c, len(v), "" if len(v) == 1 else "s", "".join(v)) for c, v in groups.items()) + '</div>'
        lib = ('<section class="pp-sec" id="tests"><div class="wrap"><div class="head rv"><p class="label">The tests</p><h2>Five ways to understand yourself.</h2>'
               '<p>Each test looks at a different side of you. The Maturity Assessment is live now, and four more are on the way.</p></div><div class="rv">%s</div></div></section>') % cards
    show = ""
    if a.get("showcase"):
        sc = a["showcase"]
        marks = "".join('<span class="mk" data-n="%d" style="left:%s%%;top:%s%%">%d</span>' % (i + 1, x, y, i + 1) for i, (x, y, t, d) in enumerate(sc["points"]))
        pts = "".join('<li data-n="%d" tabindex="0"><span class="pn">%d</span><span><b>%s</b>%s</span></li>' % (i + 1, i + 1, t, d) for i, (x, y, t, d) in enumerate(sc["points"]))
        chips = "".join('<span>%s</span>' % m for m in sc.get("more", []))
        bar = '<div class="sc-bar"><i></i><i></i><i></i><span>%s</span></div>' % sc["bar"] if sc.get("bar") else ""
        show = ('<section class="pp-sec showcase%s" id="%s"><div class="wrap"><div class="head rv"><p class="label pc">%s</p><h2>%s</h2><p>%s</p></div>'
                '<div class="sc-grid rv"><figure class="sc-shot">%s'
                '<div class="sc-img"><img src="%s" width="%d" height="%d" loading="lazy" decoding="async" alt="%s">%s</div></figure>'
                '<ol class="sc-pts">%s</ol></div>%s</div></section>') % (" tall" if sc.get("tall") else "", sc["id"], sc["label"], sc["title"], sc["lead"], bar, sc["img"], sc["w"], sc["h"], sc["alt"], marks, pts,
                ('<div class="sc-more rv"><b>Also inside</b>%s</div>' % chips) if chips else "")
    nxt = "".join('<a class="nx rv" href="/%s/" style="--pc:%s;--tint:%s;--pline:%s">%s<span><b>%s</b><small>%s</small></span>%s</a>' % (
        k, APPS[k]["color"], APPS[k]["tint"], APPS[k]["pline"], logo(k), APPS[k]["name"], APPS[k]["verb"], ARROW) for k in ORDER if k != key)
    return '''<main id="main" class="pp" style="--pc:%(color)s;--tint:%(tint)s;--pline:%(pline)s">
  <section class="phero" id="top"><div class="wrap">
    <div class="rv">
      <p class="crumb"><a href="/">HV World</a> <span>/</span> %(name)s</p>
      <div class="pname">%(logo)s<div><h1>%(name)s</h1><p class="verb">%(verb)s</p></div></div>
      <p class="lead">%(lead)s</p>
      <div class="ctas"><a class="btn" href="%(url)s">%(cta)s %(arrow)s</a><a class="btn ghost" href="#features">See every feature</a></div>
    </div>
    <div class="pmock rv">%(stagehtml)s</div>
  </div></section>
  <div class="factband"><div class="wrap facts rv">%(facts)s</div></div>

  <section class="pp-sec"><div class="wrap pf">
    <div class="rv"><p class="label">The problem</p><h2>%(p1)s</h2><p>%(p2)s</p></div>
    <div class="rv"><p class="label pc">What %(name)s does</p><h2>%(f1)s</h2><p>%(f2)s</p><a class="more" href="%(story)s">See it in Riya's story %(arrow)s</a></div>
  </div></section>
%(show)s
%(after_show)s
  <section class="pp-sec"><div class="wrap">
    <div class="head rv"><p class="label">How it works</p><h2>Three steps. That's it.</h2></div>
    <div class="steps3">%(steps)s</div>
  </div></section>

%(lib)s
  <section class="pp-sec" id="features"><div class="wrap">
    <div class="head rv"><p class="label">Every feature</p><h2>Everything %(name)s does.</h2></div>
    <div class="fgrid rv">%(feats)s</div>
  </div></section>

  <section class="pp-sec"><div class="wrap">
    <div class="head rv"><p class="label">Who it's for</p><h2>Made for every walk of life.</h2></div>
    <div class="who rv">%(who)s</div>
  </div></section>

%(before_faq)s
  <section class="pp-sec"><div class="wrap">
    <div class="head rv"><p class="label">FAQ</p><h2>Questions about %(name)s.</h2></div>
    <div class="faq rv">%(faq)s</div>
    <div class="pcta rv"><a class="btn" href="%(url)s">%(cta)s %(arrow)s</a></div>
  </div></section>

  <section class="pp-sec next"><div class="wrap">
    <p class="label">The rest of HV World</p>
    <div class="nxs">%(nxt)s</div>
    <p class="back"><a href="/">See all three apps together %(arrow)s</a></p>
  </div></section>
</main>''' % dict(a, show=show, after_show=a.get("after_show", "").replace("__ARROW__", ARROW).replace("__SHARE__", "".join('<span>%s%s</span>' % (I(d), t) for t, d in SHARE)), before_faq=a.get("before_faq", "").replace("__PARTNERS__", "".join('<div class="pt-c"><div class="pt-top"><span class="pt-ic">%s</span><span class="pt-tag">Upcoming</span></div><h3>%s</h3><p>%s</p></div>' % (I(d), t, x) for t, x, d in PARTNERS)), stagehtml=stage(key, a["mock"]), logo=logo(key), url=URL[key], arrow=ARROW, facts=facts, steps=steps, feats=feats, lib=lib, who=who, faq=faq, nxt=nxt,
                  p1=a["problem"][0], p2=a["problem"][1], f1=a["fix"][0], f2=a["fix"][1])


FILM_MAIN = """<main id="main" class="filmpage">
  <section class="wrap fp">
    <p class="label">HV World in action</p>
    <h1>See all 3 apps in action.</h1>
    <div class="fpv" data-yt="SaSfRrtvrTg"><button type="button" class="again" id="fpAgain" hidden aria-label="Watch again"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg><span>Watch again</span></button><button type="button" class="unmute" id="fpUnmute" hidden>🔊&nbsp; Tap for sound</button><div class="prem" id="fpPrem" hidden><div class="pin"><p class="pk">World premiere</p><p class="pd">1 October 2026 · 12:00 PM IST</p><p class="pc" id="fpCount" role="timer" aria-live="off"></p><p class="ps">Same time on YouTube.</p></div></div><div class="yt" id="fpYT" hidden><div id="fpYTp"></div></div><button type="button" class="ytgo" id="fpGo" hidden aria-label="Play the film"><span class="pb"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg></span><span>Watch the film</span></button><div class="ytc" id="fpCtl" hidden><button type="button" id="fpPlay" aria-label="Pause"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-pause" d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" fill="currentColor"/><path class="i-play" d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg></button><span class="tm" id="fpCur">0:00</span><input type="range" id="fpSeek" min="0" max="1000" value="0" step="1" aria-label="Seek"><span class="tm" id="fpDur">0:00</span><button type="button" id="fpMute" aria-label="Mute"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor"/><path class="i-on" d="M15 8.5a5 5 0 0 1 0 7M17.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path class="i-off" d="M15.5 9.5l5 5M20.5 9.5l-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button><button type="button" id="fpFull" aria-label="Full screen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div><video id="fpVid" playsinline preload="metadata" poster="/watch/premiere.jpg" data-src="/media/hv-world-launch.mp4"></video></div>
    <p class="fpsub">Real screens from HV Test, HV Reset and HV Vault.</p>
    <div class="ctas"><a class="btn" href="/">Explore HV World __ARROW__</a><a class="btn ghost" href="/story/">Read Riya's story</a></div>
    <div class="fpapps"><a href="__U_TEST__">__LOGO_TEST__HV Test</a><a href="__U_RESET__">__LOGO_RESET__HV Reset</a><a href="__U_VAULT__">__LOGO_VAULT__HV Vault</a></div>
  </section>
</main>"""
FILM_CSS = """
.filmpage{background:#070B18;color:#fff;border-bottom:1px solid #1B2138}
.fp{padding:56px 0 72px;text-align:center}
.fp .label{color:#9AA7FF}
.fp h1{font-size:clamp(34px,5vw,60px);font-weight:700;letter-spacing:-.045em;line-height:1.05;margin:6px 0 30px}
.fpv{position:relative;max-width:1040px;margin:0 auto;border-radius:22px;overflow:hidden;border:1px solid #232A45;box-shadow:0 50px 100px -40px rgba(0,0,0,.9)}
.fpv video{display:block;width:100%;aspect-ratio:16/9;background:#000}
.fpv video[hidden],.prem[hidden]{display:none}
.yt{position:relative;aspect-ratio:16/9;background:#070B18 url(/watch/premiere.jpg) center/cover}.yt[hidden],.ytgo[hidden],.ytc[hidden]{display:none}
.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.ytend .yt iframe{visibility:hidden}
.ytgo{position:absolute;inset:0;z-index:2;display:flex;align-items:flex-end;justify-content:center;gap:12px;padding:0 0 9%;border:0;cursor:pointer;background:#070B18 url(/watch/premiere.jpg) center/cover;font:600 17px/1 inherit;color:#1D1D1F}
.ytgo>span:last-child{background:rgba(255,255,255,.62);-webkit-backdrop-filter:blur(14px) saturate(1.6);backdrop-filter:blur(14px) saturate(1.6);border:1px solid rgba(255,255,255,.85);padding:10px 20px 10px 10px;border-radius:999px;display:inline-flex;align-items:center;gap:10px;box-shadow:0 18px 40px -16px rgba(46,67,166,.55),inset 0 1px 0 #fff;transition:transform .25s}
.ytgo .pb{display:none}
.ytgo>span:last-child::before{content:"";width:34px;height:34px;border-radius:50%;background:#2E43A6 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 6.5v11l9-5.5z' fill='white'/%3E%3C/svg%3E") center/18px no-repeat}
.ytgo:hover>span:last-child,.ytgo:focus-visible>span:last-child{transform:scale(1.05)}
.ytc{position:absolute;left:14px;right:14px;bottom:14px;z-index:3;display:flex;align-items:center;gap:10px;padding:6px 12px 6px 6px;border-radius:999px;color:#fff;background:rgba(14,18,38,.5);-webkit-backdrop-filter:blur(16px) saturate(1.5);backdrop-filter:blur(16px) saturate(1.5);border:1px solid rgba(255,255,255,.18);box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 16px 36px -18px rgba(0,0,0,.8);transition:opacity .35s,transform .35s}
.ytc.dim{opacity:0;transform:translateY(8px);pointer-events:none}
.ytc button{flex:none;width:36px;height:36px;border:0;border-radius:50%;background:transparent;color:#fff;cursor:pointer;display:grid;place-items:center}
.ytc button:hover,.ytc button:focus-visible{background:rgba(255,255,255,.16)}
.ytc svg{width:20px;height:20px}
.ytc #fpPlay{background:rgba(255,255,255,.92);color:#1D1D1F}
.ytc .i-play,.ytc.paused .i-pause,.ytc .i-off,.ytc.muted .i-on{display:none}.ytc.paused .i-play,.ytc.muted .i-off{display:inline}
.ytc .tm{flex:none;font-size:13px;font-variant-numeric:tabular-nums;color:#DDE2FF;min-width:34px;text-align:center}
.ytc input{flex:1;min-width:40px;height:4px;margin:0;-webkit-appearance:none;appearance:none;border-radius:4px;background:linear-gradient(90deg,#9AA7FF var(--p,0%),rgba(255,255,255,.25) var(--p,0%));cursor:pointer}
.ytc input::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.4)}
.ytc input::-moz-range-thumb{width:14px;height:14px;border:0;border-radius:50%;background:#fff}
.ytc.live .tm,.ytc.live input{visibility:hidden}
.fpv:fullscreen{border-radius:0;border:0;display:flex;align-items:center;justify-content:center;background:#000}
.fpv:fullscreen .yt{width:min(100vw,177.78vh)}
@media (max-width:560px){.ytgo{font-size:14px;padding-bottom:6%}.ytgo>span:last-child{padding:6px 14px 6px 6px}.ytgo>span:last-child::before{width:26px;height:26px;background-size:14px}.ytc{left:8px;right:8px;bottom:8px;gap:4px;padding:3px 8px 3px 3px}.ytc button{width:30px;height:30px}.ytc svg{width:17px;height:17px}.ytc .tm{font-size:11px;min-width:28px}}
.prem{position:absolute;inset:0;z-index:2;display:flex;align-items:center;justify-content:center;padding:0 20px;background:rgba(7,11,24,.66);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.prem .pin{text-align:center}.prem p{margin:0}
.prem .pk{font-size:13px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#C9D0FF}
.prem .pd{font-size:clamp(18px,2.4vw,24px);font-weight:600;margin-top:6px}
.prem .pc{font-size:clamp(34px,6vw,64px);font-weight:700;letter-spacing:-.03em;font-variant-numeric:tabular-nums;line-height:1.1;margin-top:6px}
.prem .ps{color:#AEB6D6;font-size:15px;margin-top:6px}
@media (max-width:560px){.prem .pk{font-size:11px}.prem .pd{font-size:16px}.prem .pc{font-size:40px}.prem .ps{font-size:13px}}
.unmute{position:absolute;left:50%;top:18px;transform:translateX(-50%);z-index:3;border:0;cursor:pointer;font:600 17px/1 inherit;color:#1D1D1F;background:#fff;padding:13px 22px;border-radius:999px;box-shadow:0 14px 34px -10px rgba(0,0,0,.7);animation:unpulse 1.6s ease-in-out infinite}
@keyframes unpulse{50%{transform:translateX(-50%) scale(1.06)}}
@media (prefers-reduced-motion:reduce){.unmute{animation:none}}
.fpsub{color:#AEB6D6;font-size:18px;margin:22px 0 22px}
.fp .ctas{justify-content:center}.fp .btn.ghost{color:#B9C3FF}
.fpapps{display:flex;flex-wrap:wrap;gap:10px 22px;justify-content:center;margin-top:30px}
.fpapps a{display:inline-flex;align-items:center;gap:9px;color:#DDE2F5;text-decoration:none;font-weight:600;font-size:15px}.fpapps svg{width:26px;height:26px;border-radius:7px}
@media (max-width:880px){.fp{padding:32px 0 48px}.fpv{border-radius:14px}}
"""
# ---------------------------------------------------------------- shared page shell
def shell(path, title, desc, og, body, active):
    nav = [("overview", "/", "Home", "opt"), ("test", "/test/", '<span class="d">HV </span>Test', ""),
           ("reset", "/reset/", '<span class="d">HV </span>Reset', ""), ("vault", "/vault/", '<span class="d">HV </span>Vault', ""), ("watch", "/watch/", '<svg class="ni" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 8.3v7.4l6-3.7z" fill="currentColor"/></svg><span class="nt">Watch</span>', "ic")]
    links = "".join('<a class="%s"%s%s href="%s">%s</a>' % (c, ' aria-current="page"' if k == active else "", ' aria-label="Watch"' if k == "watch" else "", h, t) for k, h, t, c in nav)
    url = "https://harshvittori.github.io" + path
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta name="theme-color" content="#F9F9FB">
<link rel="canonical" href="%s">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="HV World">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="%s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s">
<style>%s</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="wrap nav"><a class="brand" href="/">%sHV World</a>
<nav aria-label="Main">%s<a class="ic" aria-label="Riya's story" href="/story/"><svg class="ni" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.5C10 5 7 4.5 3.5 5v13c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5z"/><path d="M12 6.5v13"/></svg><span class="nt"><span class="d">Riya's </span>Story</span></a></nav></div></header>
%s
<footer><div class="wrap row"><span>© <span id="yr">2026</span> HV World · Built by Harsh Goyal</span>
<nav aria-label="Footer"><a href="/">Home</a><a href="/watch/">Watch</a><a href="/story/">Riya's story</a><a href="/test/">HV Test</a><a href="/reset/">HV Reset</a><a href="/vault/">HV Vault</a><a href="https://www.linkedin.com/in/harshvittori" target="_blank" rel="noopener">LinkedIn</a><a href="https://github.com/harshvittori" target="_blank" rel="noopener">GitHub</a><a href="/terms/">Terms</a><a href="/privacy/">Privacy</a></nav></div></footer>
<script>
(function () {
  document.getElementById("yr").textContent = new Date().getFullYear();
  // dashboard showcase: pointing at a highlight enlarges its number on the picture
  document.querySelectorAll(".sc-pts li").forEach(function (li) {
    var mk = document.querySelector('.mk[data-n="' + li.dataset.n + '"]');
    var on = function (v) { if (mk) mk.classList.toggle("on", v); li.classList.toggle("on", v); };
    ["mouseenter", "focus"].forEach(function (ev) { li.addEventListener(ev, function () { on(true); }); });
    ["mouseleave", "blur"].forEach(function (ev) { li.addEventListener(ev, function () { on(false); }); });
  });
  // smooth scrolling: a section's animations run only while it's on screen
  if ("IntersectionObserver" in window) {
    var ao = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle("aoff", !e.isIntersecting); }); }, { rootMargin: "150px 0px" });
    document.querySelectorAll("main > section, main article").forEach(function (s) { ao.observe(s); });
  }
  // product pictures lean a little toward the mouse (computers only, and not when motion is reduced)
  if (matchMedia("(hover:hover) and (prefers-reduced-motion:no-preference)").matches) {
    document.querySelectorAll(".stage").forEach(function (st) {
      var box = st.closest(".phero,.product") || st;
      box.addEventListener("pointermove", function (e) { var r = box.getBoundingClientRect(); st.style.setProperty("--px", ((e.clientX - r.left) / r.width - .5).toFixed(3)); st.style.setProperty("--py", ((e.clientY - r.top) / r.height - .5).toFixed(3)); });
      box.addEventListener("pointerleave", function () { st.style.setProperty("--px", 0); st.style.setProperty("--py", 0); });
    });
  }
  var fv = document.getElementById("fpVid");
  if (fv) {
    // the launch film premieres on 1 October 2026 at 12:00 PM IST; until then the page shows a countdown and no video is loaded
    var PREM = Date.parse("2026-10-01T12:00:00+05:30");
    // start playing with sound; if the browser blocks sound, play muted and offer one tap to unmute
    var ub = document.getElementById("fpUnmute");
    var unmute = function () { fv.muted = false; fv.volume = 1; ub.hidden = true; fv.play().catch(function () {}); off(); };
    var onTap = function (e) { if (fv.muted) unmute(); };
    var off = function () { document.removeEventListener("pointerdown", onTap, true); document.removeEventListener("keydown", onTap, true); };
    var start = function () {
    fv.muted = false;
    fv.play().catch(function () {
      fv.muted = true;
      fv.play().catch(function () {});
      ub.hidden = false;
      document.addEventListener("pointerdown", onTap, true);
      document.addEventListener("keydown", onTap, true);
    });
    };
    var go = function () { fv.src = fv.dataset.src; fv.preload = "auto"; fv.controls = true; start(); };
    var prem = document.getElementById("fpPrem"), cnt = document.getElementById("fpCount");
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var tick = function () {
      var ms = PREM - Date.now();
      if (ms <= 0) { prem.hidden = true; goYT(); return; }
      var t = Math.floor(ms / 1000), d = Math.floor(t / 86400), h = Math.floor(t %% 86400 / 3600), m = Math.floor(t %% 3600 / 60), x = t %% 60;
      cnt.textContent = (d ? d + "d " : "") + pad(h) + ":" + pad(m) + ":" + pad(x);
      setTimeout(tick, 1000 - Date.now() %% 1000 + 5);
    };
    // after the premiere the film plays from YouTube (so every play counts as a YouTube view) inside our own cover and glass controls;
    // if YouTube can't load (blocked, offline, embedding off), the page falls back to the film file on this site
    var box = fv.parentNode, ytId = box.dataset.yt, P = null, ytOk = false, want = false, played = false, ytTimer = 0, idleT = 0;
    var yt = document.getElementById("fpYT"), cover = document.getElementById("fpGo"), ctl = document.getElementById("fpCtl");
    var bPlay = document.getElementById("fpPlay"), bMute = document.getElementById("fpMute"), bFull = document.getElementById("fpFull");
    var seek = document.getElementById("fpSeek"), tCur = document.getElementById("fpCur"), tDur = document.getElementById("fpDur");
    var fmt = function (v) { v = Math.max(0, Math.floor(v || 0)); return Math.floor(v / 60) + ":" + pad(v - 60 * Math.floor(v / 60)); };
    var fallback = function () { if (played) return; clearTimeout(ytTimer); try { if (P && P.destroy) P.destroy(); } catch (e) {} P = null; ytOk = false; yt.hidden = true; cover.hidden = true; ctl.hidden = true; fv.hidden = false; go(); };
    var paint = function () {
      if (!P || !ytOk) return;
      var cur = P.getCurrentTime() || 0, dur = P.getDuration() || 0;
      ctl.classList.toggle("live", !(dur > 0));
      if (dur > 0 && document.activeElement !== seek) { seek.value = Math.round(cur / dur * 1000); }
      seek.style.setProperty("--p", (seek.value / 10) + "%%");
      tCur.textContent = fmt(cur); tDur.textContent = fmt(dur);
    };
    setInterval(function () { if (P && ytOk && P.getPlayerState && P.getPlayerState() === 1) paint(); }, 250);
    var idle = function () { clearTimeout(idleT); ctl.classList.remove("dim"); idleT = setTimeout(function () { if (P && P.getPlayerState() === 1 && !(matchMedia("(hover:hover)").matches && ctl.matches(":hover")) && !ctl.querySelector(":focus-visible")) ctl.classList.add("dim"); }, 2800); };
    var syncMute = function () { var m = P.isMuted(); ctl.classList.toggle("muted", m); bMute.setAttribute("aria-label", m ? "Unmute" : "Mute"); };
    var onState = function (e) {
      var st = e.data;
      if (st === 1) { played = true; clearTimeout(ytTimer); cover.hidden = true; ctl.hidden = false; box.classList.remove("ytend"); again.hidden = true; ctl.classList.remove("paused"); bPlay.setAttribute("aria-label", "Pause"); syncMute(); paint(); idle(); }
      else if (st === 2) { ctl.classList.add("paused"); bPlay.setAttribute("aria-label", "Play"); clearTimeout(idleT); ctl.classList.remove("dim"); paint(); }
      else if (st === 0) { ctl.hidden = true; box.classList.add("ytend"); again.hidden = false; }
    };
    var ytPlay = function () { want = true; if (!ytOk) return; if (P.isMuted()) P.unMute(); P.playVideo(); };
    var goYT = function () {
      if (!ytId) { go(); return; }
      fv.hidden = true; yt.hidden = false; cover.hidden = false;
      ytTimer = setTimeout(function () { if (!ytOk) fallback(); }, 12000);
      var mk = function () {
        P = new YT.Player("fpYTp", { videoId: ytId, host: "https://www.youtube.com", playerVars: { controls: 0, rel: 0, playsinline: 1, iv_load_policy: 3, fs: 0, enablejsapi: 1, origin: location.origin },
          events: { onReady: function () { ytOk = true; clearTimeout(ytTimer); P.getIframe().title = "HV World launch film"; paint(); if (want) ytPlay(); }, onStateChange: onState, onError: fallback } });
      };
      if (window.YT && YT.Player) { mk(); return; }
      var prev = window.onYouTubeIframeAPIReady;
      window.onYouTubeIframeAPIReady = function () { if (prev) prev(); mk(); };
      var sc = document.createElement("script"); sc.src = "https://www.youtube.com/iframe_api"; sc.async = true; sc.onerror = fallback; document.head.appendChild(sc);
    };
    cover.addEventListener("click", function () { cover.hidden = true; ytPlay(); });
    bPlay.addEventListener("click", function () { if (P.getPlayerState() === 1) P.pauseVideo(); else ytPlay(); });
    bMute.addEventListener("click", function () { if (P.isMuted()) P.unMute(); else P.mute(); setTimeout(syncMute, 60); ctl.classList.toggle("muted"); });
    seek.addEventListener("input", function () { var dur = P.getDuration() || 0; seek.style.setProperty("--p", (seek.value / 10) + "%%"); if (dur > 0) { P.seekTo(seek.value / 1000 * dur, true); tCur.textContent = fmt(seek.value / 1000 * dur); } });
    seek.addEventListener("change", function () { seek.blur(); });
    var fsIn = box.requestFullscreen || box.webkitRequestFullscreen;
    if (!fsIn) bFull.hidden = true;
    bFull.addEventListener("click", function () {
      if (document.fullscreenElement || document.webkitFullscreenElement) (document.exitFullscreen || document.webkitExitFullscreen).call(document);
      else fsIn.call(box);
    });
    box.addEventListener("mouseenter", idle); box.addEventListener("mousemove", idle); ctl.addEventListener("pointerdown", idle); ctl.addEventListener("focusin", idle);
    var begin = function () { if (Date.now() >= PREM) goYT(); else { prem.hidden = false; tick(); } };
    if (document.prerendering) document.addEventListener("prerenderingchange", begin, { once: true }); else begin();
    ub.addEventListener("click", function (e) { e.stopPropagation(); unmute(); });
    fv.addEventListener("volumechange", function () { if (!fv.muted) { ub.hidden = true; off(); } });
    // when the film ends: hide the player controls and rest on the HV World logo frame (just before it fades); a tap brings the controls back and plays again
    var again = document.getElementById("fpAgain");
    var replay = function () { if (P && ytOk) { again.hidden = true; box.classList.remove("ytend"); P.seekTo(0, true); ytPlay(); return; } again.hidden = true; fv.controls = true; fv.currentTime = 0; fv.play().catch(function () {}); };
    fv.addEventListener("ended", function () { fv.controls = false; if (isFinite(fv.duration)) fv.currentTime = Math.max(0, fv.duration - 1.2); again.hidden = false; ub.hidden = true; off(); });
    again.addEventListener("click", replay);
    fv.addEventListener("click", function () { if (!fv.controls && fv.currentSrc) replay(); });
  }
  var fo = document.getElementById("filmOpen");
  if (fo) {
    var dlg = document.getElementById("filmDlg"), film = document.getElementById("filmVid"), loopv = document.getElementById("loopVid");
    var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (still) { loopv.removeAttribute("autoplay"); loopv.pause(); }
    else if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { if (dlg.open) return; e.isIntersecting ? loopv.play().catch(function () {}) : loopv.pause(); }); }).observe(loopv);
    }
    fo.addEventListener("click", function () {
      loopv.pause();
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
      fagain.hidden = true; film.controls = true; film.currentTime = 0; film.play().catch(function () {});
    });
    // when the film ends: hide the controls and rest on the logo frame; a tap plays it again
    var fagain = document.getElementById("filmAgain");
    var freplay = function () { fagain.hidden = true; film.controls = true; film.currentTime = 0; film.play().catch(function () {}); };
    film.addEventListener("ended", function () { film.controls = false; if (isFinite(film.duration)) film.currentTime = Math.max(0, film.duration - 1.2); fagain.hidden = false; });
    fagain.addEventListener("click", freplay);
    film.addEventListener("click", function () { if (!film.controls) freplay(); });
    document.getElementById("filmClose").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", function () { film.pause(); if (!still) loopv.play().catch(function () {}); });
  }
  var els = document.querySelectorAll(".rv");
  if (!("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("in"); }); return; }
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8%% 0px" });
  els.forEach(function (e) { io.observe(e); });
})();
</script>
</body>
</html>
''' % (title, desc, url, title, desc, url, og, title, title, desc, og, CSS, logo("world"), links, body)

def fill(page):
    page = page.replace("__PRODUCTS__", "\n".join(product(*p, flip=(i == 1)) for i, p in enumerate(PRODUCTS)))
    page = page.replace("__FAQ__", "".join('<details><summary>%s</summary><p>%s</p></details>' % qa for qa in FAQ))
    page = page.replace("__MOCK_AI__", MOCK_AI)
    for k, v in {"ARROW": ARROW, "CHECK": CHECK, "SYNC": SYNC, "CHAIN": CHAIN, "USER": USER, "SPARK": SPARK}.items():
        page = page.replace("__%s__" % k, v)
    for k in ("TEST", "RESET", "VAULT"):
        page = page.replace("__U_%s__" % k, URL[k.lower()])
    page = re.sub(r"__LOGO_(AI|WORLD|TEST|RESET|VAULT)(_P)?__", lambda m: logo(m.group(1).lower()), page)
    left = re.findall(r"__[A-Z_]+__", page)
    assert not left, left
    return page

def write(path, page):
    d = os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    page = page.replace("</style>", transitions.CSS + "</style>", 1).replace("</head>", transitions.HEAD + "\n</head>", 1)
    open(os.path.join(d, "index.html"), "w").write(app_links_new_tab(page))
    print("ok", path, len(page), "bytes")

def build():
    write("/", fill(shell("/", "Stop guessing. Start growing. | HV World",
          "3 free apps that show your strengths, plan your day and chase your follow-ups for you. Just talk to the AI.",
          "https://harshvittori.github.io/og.jpg", OVERVIEW_MAIN, "overview")))
    film = fill(shell("/watch/", "3 apps. 1 AI. One calm day. | HV World", "See HV Test, HV Reset and HV Vault in action. Three free apps, one AI.",
                      "https://harshvittori.github.io/watch/og.jpg", FILM_MAIN, "watch"))
    film = film.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="video.other">'
        '<meta property="og:video" content="https://harshvittori.github.io/media/hv-world-film.mp4">'
        '<meta property="og:video:secure_url" content="https://harshvittori.github.io/media/hv-world-film.mp4">'
        '<meta property="og:video:type" content="video/mp4"><meta property="og:video:width" content="1920"><meta property="og:video:height" content="1080">'
        '<meta property="video:duration" content="109">', 1).replace("</style>", FILM_CSS + "</style>", 1)
    write("/watch/", film)
    for k in ORDER:
        a = APPS[k]
        write("/%s/" % k, fill(shell("/%s/" % k, a["title"], a["desc"], "https://harshvittori.github.io/%s/og.jpg" % k, app_page(k), k)))
    for path, title, desc, kind, lead, secs in [
        ("/terms/", "Terms and Conditions | HV World", "The terms for using HV World, HV Test, HV Reset, HV Vault and HV AI.", "terms", legal.TERMS_LEAD, legal.TERMS),
        ("/privacy/", "Privacy Policy | HV World", "What data HV World, HV Test, HV Reset, HV Vault and HV AI collect, why, and your rights.", "privacy", legal.PRIVACY_LEAD, legal.PRIVACY)]:
        name = "Terms and Conditions" if kind == "terms" else "Privacy Policy"
        page = shell(path, title, desc, "https://harshvittori.github.io/og.jpg", legal.page(kind, name, lead, secs), kind)
        write(path, fill(page.replace("</style>", legal.CSS + "</style>", 1)))

if __name__ == "__main__":
    build()
