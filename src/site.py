"""HV World: the product pages. Builds /overview/ (all three apps, HV AI, privacy, price, FAQ)
and one page per app: /test/, /reset/, /vault/. Logos come from src/.

Run from the repo root:  python3 src/site.py
The story page (index.html) comes from src/story.py."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def read(n):
    return open(os.path.join(HERE, n)).read().strip().replace('xmlns="http://www.w3.org/2000/svg" ', '')

LOGOS = {"world": read("world-orbit.svg"), "test": read("logo-test.svg"), "reset": read("logo-reset.svg"), "vault": read("logo-vault.svg")}
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
SYNC = I('<path d="M21 12a9 9 0 0 1-15.5 6.2M3 12A9 9 0 0 1 18.5 5.8"/><path d="M18.5 2v4h-4M5.5 22v-4h4"/>')
USER = I('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>')
SPARK = I('<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>')
LOCK = I('<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>')

URL = {"test": "https://harshvittori.github.io/hv-tests/", "reset": "https://harshvittori.github.io/harsh-reset/", "vault": "https://harshvittori.github.io/hv-vault-web/"}

# ---------------------------------------------------------------- product previews (plain HTML, no screenshots)
MOCK_TEST = '''<div class="mock q">
  <div class="prog"><i></i></div>
  <p class="meta">Maturity Assessment · 18 of 29</p>
  <h5>A teammate takes credit for your idea in a meeting. What do you do?</h5>
  <div class="opt"><i></i>Correct them right there</div>
  <div class="opt on"><i></i>Talk to them privately after</div>
  <div class="opt"><i></i>Let it go this time</div>
  <div class="opt"><i></i>Tell your manager later</div>
</div>'''

MOCK_RESET = '''<div class="mock day">
  <p class="meta">Now · until 12:30 PM</p>
  <div class="now">01:14:52</div>
  <p class="meta">Send applications</p>
  <div class="blk cur"><span>11:00 AM</span>Send applications</div>
  <div class="blk"><span>12:30 PM</span>Short break</div>
  <div class="blk meal"><span>1:15 PM</span>Lunch</div>
  <div class="blk"><span>2:00 PM</span>Outreach</div>
</div>'''

MOCK_VAULT = '''<div class="mock kan">
  <div><h4>Saved</h4><div><b>GTM Associate</b><small>Razorpay</small></div><div><b>Growth Analyst</b><small>Meesho</small></div></div>
  <div><h4>Applied</h4><div class="hot"><b>Founder's Office</b><small>Cred · follow-up in 5 days</small></div></div>
  <div><h4>Interview</h4><div><b>Partnerships Lead</b><small>Zomato · Tue, 4:00 PM</small></div></div>
</div>'''

MOCK_AI = '''<div class="mock chat">
  <p class="ai">Bolo, kya karna hai?</p>
  <p class="me">Kal 4 baje Zomato ka interview hai</p>
  <div class="card"><b>Interview</b>Zomato · Tue, 29 Sep · 4:00 PM<em>Confirm</em></div>
  <p class="me">Cred wale ko applied mark karo aur 5 din baad follow-up laga do</p>
  <div class="card"><b>2 changes</b>Founder's Office at Cred → Applied, follow-up on 4 Oct<em>Confirm all</em></div>
</div>'''

PRODUCTS = [
    ("test", "HV Test", "Know yourself", "Honest, everyday situations that show how you really think, react and decide.", [
        ("Maturity Assessment.", "28 to 30 real-life situations across 10 areas. About 10 minutes."),
        ("A score out of 100.", "See where you're strong and where to grow."),
        ("Two PDFs to keep.", "A full report and a personal 30-day plan."),
        ("Private by design.", "No login. Your answers never leave your browser."),
    ], MOCK_TEST, "Take a test"),
    ("reset", "HV Reset", "Plan your day", "A day made of simple blocks: one block, one task. You always know what to do right now.", [
        ("One block at a time.", "A big clock shows what's on now and what's next."),
        ("Running late? Shift the day.", "One tap moves the rest of the plan."),
        ("The basics never drop.", "Core tasks can shrink on a hard day. Meals are never skipped."),
        ("Plans from one sentence.", "“Aaj 3 ghante apply, 1 ghanta prep, shaam 7 ke baad free.”"),
    ], MOCK_RESET, "Open HV Reset"),
    ("vault", "HV Vault", "Act on every opportunity", "Every job, company, follow-up and interview in one calm place, so nothing slips.", [
        ("One board.", "Move jobs from Saved to Applied, Interview and Offer."),
        ("Follow-ups that set themselves.", "Mark a job Applied and the first reminder is ready."),
        ("Profile from your resume.", "Upload it once and your profile fills itself in."),
        ("Calendar, templates, numbers.", "Interviews, ready-to-send messages and your weekly progress."),
    ], MOCK_VAULT, "Open HV Vault"),
]

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
</article>''' % (key, " flip" if flip else "", key, logo(key), name, tag, pitch, lis, URL[key], cta, ARROW, key, mock))

FAQ = [
    ("Is it really free?", "Yes. HV Test, HV Reset and HV Vault are free to use, and so is HV AI. No card, no trial, no hidden plan."),
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
.nav nav{display:flex;gap:22px;margin-left:auto;font-size:14px}
.nav nav a{text-decoration:none;color:var(--soft)}.nav nav a:hover{color:var(--ink)}
.nav .story{color:var(--accent)!important;font-weight:600}
.nav nav a[aria-current]{color:var(--ink);font-weight:600}
@media (max-width:720px){.nav nav a.opt,.nav .d{display:none}.nav nav{gap:16px}}
@media (max-width:360px){.brand{font-size:0;gap:0}.nav nav{gap:14px}}
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
.orbit .ring{position:absolute;inset:8%;border-radius:50%;border:1.5px dashed #D2D2D7}
.orbit .ring.r2{inset:25%}
.orbit .core{position:absolute;inset:37%}
.orbit .core svg{width:100%;height:100%;border-radius:26%;box-shadow:0 24px 50px -22px rgba(30,40,110,.55)}
.planet{position:absolute;width:23%;text-decoration:none;display:flex;flex-direction:column;align-items:center;gap:10px;transition:transform .35s cubic-bezier(.22,1,.36,1)}
.planet svg{width:100%;aspect-ratio:1;border-radius:24%;box-shadow:0 16px 34px -18px rgba(20,30,70,.5)}
.planet span{font-weight:600;font-size:13.5px;white-space:nowrap}
.planet:hover{transform:translateY(-5px)}
.planet.p1{left:38.5%;top:-3%}.planet.p2{left:-1%;top:56%}.planet.p3{right:-1%;top:56%}
@media (prefers-reduced-motion:no-preference){.orbit .ring{animation:spin 90s linear infinite}.orbit .ring.r2{animation-duration:60s;animation-direction:reverse}.planet{animation:float 7s ease-in-out infinite}.planet.p2{animation-delay:-2.3s}.planet.p3{animation-delay:-4.6s}}
@keyframes spin{to{transform:rotate(360deg)}}@keyframes float{50%{translate:0 -8px}}
@media (max-width:880px){.hero{grid-template-columns:1fr;padding:48px 0 40px;gap:36px}.orbit{max-width:320px}}
/* strip */
.strip{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:96px}
.strip div{padding:22px 20px;border-right:1px solid var(--line)}.strip div:last-child{border-right:0}
.strip b{display:block;font-size:24px;font-weight:700;letter-spacing:-.03em}
.strip span{font-size:14.5px;color:var(--soft)}
@media (max-width:720px){.strip{grid-template-columns:1fr 1fr}.strip div:nth-child(2){border-right:0}.strip div:nth-child(-n+2){border-bottom:1px solid var(--line)}.strip div{padding:18px 14px}}
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
.product .right{background:var(--tint,var(--gray));border-left:1px solid var(--pline,var(--line));padding:40px;display:flex;align-items:center;justify-content:center;min-height:380px}
.product.flip .left{order:2}.product.flip .right{border-left:0;border-right:1px solid var(--pline)}
.p-test{--tint:#EEF6F1;--pline:#D3E7DA}.p-reset{--tint:#EEF2FB;--pline:#D6E0F4}.p-vault{--tint:#F8F3E8;--pline:#EADDC2}
.acts{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin-top:6px}.product .acts .btn{margin-top:0}
@media (max-width:880px){.product{grid-template-columns:1fr}.product.flip .left{order:0}.product .right,.product.flip .right{border-left:0;border-right:0;border-top:1px solid var(--pline)}.product .left{padding:28px 22px}.product .right{min-height:0;padding:28px 18px}}
/* mock screens: white cards on gray */
.mock{width:100%;max-width:400px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px;font-size:14px;box-shadow:0 24px 50px -32px rgba(20,30,60,.35)}
.meta{font-size:12.5px;color:var(--faint)}
.q .prog{height:5px;border-radius:9px;background:#E3F2EA;margin-bottom:12px;overflow:hidden}.q .prog i{display:block;height:100%;width:62%;background:var(--test)}
.q h5{font-size:16px;font-weight:600;line-height:1.35;margin:6px 0 14px;letter-spacing:-.02em}
.q .opt{display:flex;gap:10px;align-items:center;padding:10px 12px;border-radius:12px;border:1px solid var(--line);margin-bottom:7px}
.q .opt i{width:14px;height:14px;border-radius:50%;border:2px solid #C7C7CC;flex:none}
.q .opt.on{border-color:var(--test);background:#EEF7F2;font-weight:600}.q .opt.on i{border-color:var(--test);background:var(--test)}
.day .now{font-size:40px;font-weight:300;letter-spacing:-.02em;line-height:1.1;margin:4px 0 2px;font-variant-numeric:tabular-nums}
.day .meta:nth-of-type(2){margin-bottom:14px}
.day .blk{display:flex;gap:12px;align-items:center;padding:10px 12px;border-radius:12px;margin-bottom:6px;background:var(--gray)}
.day .blk span{font-size:12px;font-weight:600;width:62px;color:var(--faint)}
.day .blk.cur{background:var(--ink);color:#fff}.day .blk.cur span{color:#C7C7CC}
.day .blk.meal{background:#FBF4E4}
.kan{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.kan>div{min-width:0}
.kan h4{font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);margin:0 0 8px}
.kan div div{background:var(--gray);border-radius:10px;padding:9px 10px;margin-bottom:7px;line-height:1.3}
.kan div div.hot{background:#FBF4E4}
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
.ai-sec .l p:not(.label){font-size:18.5px;color:var(--soft);margin-top:14px}
.ai-sec ul{list-style:none;padding:0;margin:22px 0 0;display:grid;gap:10px}
.ai-sec li{display:flex;gap:10px;font-size:16px;color:var(--soft)}.ai-sec li svg{width:20px;height:20px;flex:none;color:var(--accent);margin-top:2px}
.ai-sec .r{background:#EEF0FA;border-left:1px solid #DCE0F2;padding:40px;display:flex;align-items:center;justify-content:center}
@media (max-width:880px){.ai-sec{grid-template-columns:1fr}.ai-sec .l{padding:28px 22px}.ai-sec .r{padding:28px 18px}}
/* privacy + free */
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:112px}
.two>div{background:#fff;border:1px solid var(--line);border-radius:28px;padding:40px}
.two h3{font-size:26px;font-weight:700;letter-spacing:-.03em;margin-bottom:10px}
.two p:not(.label){color:var(--soft);font-size:17px}
.big{font-size:clamp(64px,8vw,96px);font-weight:700;letter-spacing:-.05em;line-height:1;margin:4px 0 12px}
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
.sep{border:0;height:1px;background:var(--line);width:min(1120px,100% - 32px);margin:0 auto 96px}
.faq details p{max-width:none}
/* app pages */
.pp .label.pc,.pp .head .label{color:var(--pc)}
.pf .label:not(.pc){color:var(--faint)}
.phero{background:var(--tint);border-bottom:1px solid var(--pline)}
.phero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center;padding:72px 0 64px}
.crumb{font-size:14px;color:var(--soft);margin-bottom:26px}.crumb a{text-decoration:none;color:var(--soft)}.crumb a:hover{color:var(--ink)}.crumb span{margin:0 6px;color:var(--faint)}
.pname{display:flex;align-items:center;gap:18px}
.pname svg{width:76px;height:76px;border-radius:20px;flex:none;box-shadow:0 18px 36px -20px rgba(20,30,70,.5)}
.pname h1{font-size:clamp(40px,5.4vw,64px);font-weight:700;letter-spacing:-.045em;line-height:1}
.verb{font-size:clamp(18px,2vw,22px);font-weight:600;color:var(--pc);margin-top:6px}
.pp .lead{margin:24px 0 28px}
.pmock{display:flex;justify-content:center}.pmock .mock{border-color:var(--pline);box-shadow:0 30px 60px -36px rgba(20,30,60,.4)}
.facts{display:grid;grid-template-columns:repeat(4,1fr);background:#fff;border:1px solid var(--line);border-radius:20px;margin-top:-34px;position:relative}
.facts div{padding:20px 22px;border-right:1px solid var(--line)}.facts div:last-child{border-right:0}
.facts b{display:block;font-size:22px;font-weight:700;letter-spacing:-.03em;color:var(--pc)}.facts span{font-size:14px;color:var(--soft)}
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
.who{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.wt{background:#fff;border:1px solid var(--line);border-left:3px solid var(--pc);border-radius:14px;padding:18px 20px}
.wt b{display:block;font-size:17px;font-weight:700;letter-spacing:-.02em;margin-bottom:4px}.wt span{color:var(--soft);font-size:15.5px}
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
  .facts{grid-template-columns:1fr 1fr}.facts div:nth-child(2){border-right:0}.facts div:nth-child(-n+2){border-bottom:1px solid var(--line)}.facts div{padding:16px}
  .pp-sec{padding:64px 0}.pf{grid-template-columns:1fr}.pf>div,.pf>div+div{padding:0}.pf>div+div{border-left:0;border-top:1px solid var(--line);margin-top:32px;padding-top:32px}
  .steps3{grid-template-columns:1fr}.st{border-right:0;border-bottom:1px solid var(--line)}.st:last-child{border-bottom:0}
  .fgrid{grid-template-columns:1fr 1fr}.who{grid-template-columns:1fr 1fr}.nxs{grid-template-columns:1fr}}
@media (max-width:560px){.fgrid,.who{grid-template-columns:1fr}.ft{padding:22px 20px}}
/* reveal */
@media (prefers-reduced-motion:no-preference){.rv{opacity:0;transform:translateY(20px);transition:opacity .7s ease,transform .7s cubic-bezier(.22,1,.36,1)}.rv.in{opacity:1;transform:none}}
"""

OVERVIEW_MAIN = """<main id="main">
  <section id="top" class="wrap hero">
    <div class="rv">
      <p class="eyebrow">By Harsh Vittori · Free for everyone</p>
      <h1>Your work, your day, your growth. <span>One calm world.</span></h1>
      <p class="lead">Three simple apps that work together. Know yourself with HV Test, plan your day with HV Reset, and keep every opportunity in HV Vault. Just tell HV AI what you need.</p>
      <div class="ctas"><a class="btn" href="#apps">Explore the apps</a><a class="btn ghost" href="/">Watch Riya's story __ARROW__</a></div>
      <p class="note">No card, no trial, no ads. Everything runs in your browser.</p>
    </div>
    <div class="orbit rv" aria-hidden="true">
      <div class="ring"></div><div class="ring r2"></div>
      <div class="core">__LOGO_WORLD__</div>
      <a class="planet p1" href="/test/" tabindex="-1">__LOGO_TEST__<span>HV Test</span></a>
      <a class="planet p2" href="/reset/" tabindex="-1">__LOGO_RESET__<span>HV Reset</span></a>
      <a class="planet p3" href="/vault/" tabindex="-1">__LOGO_VAULT__<span>HV Vault</span></a>
    </div>
  </section>

  <div class="wrap strip rv">
    <div><b>3 apps</b><span>One world, one sign-in</span></div>
    <div><b>₹0</b><span>Everything, for everyone</span></div>
    <div><b>HV AI</b><span>Type or talk, your language</span></div>
    <div><b>Any device</b><span>Phone and laptop</span></div>
  </div>

  <section id="apps" class="wrap">
    <div class="head rv"><p class="label">The apps</p><h2>Three apps. Each does one job well.</h2><p>Open any of them in your browser. Nothing to install.</p></div>
    <div class="products">__PRODUCTS__</div>
  </section>

  <hr class="sep">
  <section id="together" class="wrap">
    <div class="head rv"><p class="label">Better together</p><h2>Use one. Or let them work as a team.</h2><p>Each app stands on its own. Together, your plan and your progress stay in step.</p></div>
    <div class="together">
      <div class="feat rv"><div class="ic">__SYNC__</div><h3>Reset and Vault in sync</h3><p>Log an application in HV Reset and it lands in HV Vault as Applied, with its first follow-up. Your day counter counts it too.</p></div>
      <div class="feat rv"><div class="ic">__USER__</div><h3>One Google sign-in</h3><p>Sign in to HV Vault once and HV Reset on the same browser is connected. Your phone and laptop show the same data.</p></div>
      <div class="feat rv"><div class="ic">__SPARK__</div><h3>HV AI in each app</h3><p>In HV Vault it handles jobs, follow-ups and interviews. In HV Reset it builds and adjusts your day. Each one changes only its own app.</p></div>
    </div>
  </section>

  <hr class="sep">
  <section id="ai" class="wrap">
    <div class="ai-sec rv">
      <div class="l">
        <p class="label">HV AI</p>
        <h2 class="sec-h">Just say it. HV AI does the work.</h2>
        <p>Type, or hold the mic and talk the way you normally do. HV AI turns it into clear changes you check before anything is saved.</p>
        <ul>
          <li>__CHECK__Hindi, English or Hinglish, typed or spoken</li>
          <li>__CHECK__Every change is a card: Confirm, Edit or Cancel</li>
          <li>__CHECK__Deletes always ask first. Unclear names get a question, not a guess</li>
          <li>__CHECK__Undo the last change any time</li>
          <li>__CHECK__Built in and free: no key, no setup</li>
        </ul>
      </div>
      <div class="r">__MOCK_AI__</div>
    </div>
  </section>

  <hr class="sep">
  <section id="free" class="wrap two">
    <div class="rv"><p class="label">Privacy</p><h3>Your data is yours.</h3><p>HV Vault saves everything to your own private space, linked to your Google account. Only you can read it. HV Test never stores your answers: everything happens in your browser.</p></div>
    <div class="rv"><p class="label">Price</p><div class="big">₹0</div><p>All three apps are free for everyone, including HV AI. No card, no trial, no ads.</p></div>
  </section>

  <hr class="sep">
  <section id="faq" class="wrap">
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
      <p class="builder">Designed and built by Harsh Vittori · <a href="https://www.linkedin.com/in/harshvittori" target="_blank" rel="noopener">Connect on LinkedIn</a></p>
    </div>
  </section>
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
 'CHECKC': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16.5 9"/>',
}

# ---------------------------------------------------------------- one page per app
APPS = {
 "test": dict(name="HV Test", verb="Know yourself", color="#127A4F", tint="#EEF6F1", pline="#D3E7DA", mock=MOCK_TEST, cta="Take a test", story="/#test",
   title="HV Test | Know yourself with real-life situations",
   desc="HV Test shows how you really think, react and decide. The Maturity Assessment: 10 areas, a score out of 100, a full report and a 30-day plan. Free, no login.",
   lead="Honest, everyday situations that show how you really think, react and decide. Then a clear score and a plan to grow.",
   facts=[("10 min", "to finish"), ("10", "areas measured"), ("2 PDFs", "report and 30-day plan"), ("No login", "answers stay on your device")],
   problem=("“So, what are your strengths?”", "Most of us have never really measured ourselves. So in an interview, a review or a big decision, we guess."),
   fix=("A clear picture, in 10 minutes.", "HV Test puts you in real situations and scores how you actually respond, so you know where you're strong and where to grow."),
   steps=[("Pick a test", "Start with the Maturity Assessment, and add your name, age and focus."),
          ("Answer honestly", "28 to 30 everyday situations. There are no right answers: pick what you'd really do."),
          ("Get your plan", "Your score, strengths and growth areas, and two PDFs to keep.")],
   feats=[("CHECKC", "Maturity Assessment", "The first HV Test: how you think, react and decide in real life. About 10 minutes."),
          ("SHUFFLE", "Real-life situations", "A bank of 104 situations. Each attempt picks 28 to 30, covering all 10 areas."),
          ("GRID", "10 areas", "Emotional control, accountability, self-awareness, conflict, relationships, decisions, patience, empathy, responsibility, long-term thinking."),
          ("TARGET", "Score out of 100", "Your overall score and a level: Developing, Emerging, Grounded or Highly Consistent."),
          ("FILE", "Full report PDF", "About 12 pages on each area: where you're strong and where to grow."),
          ("ROUTE", "30-day plan PDF", "About 10 pages of small daily steps. Download both PDFs in one tap."),
          ("SYNC", "Fresh every time", "Questions and options are shuffled, and a retake avoids the ones you saw last time."),
          ("SHIELD", "Private by design", "No login and no server. Your answers never leave your device."),
          ("HEART", "Honest, not a quiz", "Four believable options with real trade-offs. It's for growth, not a diagnosis.")],
   who=[("Students", "Know your strengths before placements and first interviews."),
        ("Job seekers", "Real answers, with real examples, for “tell me about yourself”."),
        ("Professionals", "See how you handle conflict, pressure and feedback at work."),
        ("Team leads", "Understand your own patterns before you guide others."),
        ("Career switchers", "Check what you bring to a new field, beyond your old job title."),
        ("Anyone curious", "A calm look at yourself, and small steps to grow.")],
   faq=[("Is HV Test a diagnosis?", "No. It's a self-assessment for personal growth, not a clinical or psychological diagnosis."),
        ("Do I need an account?", "No. There's no login, and your answers never leave your browser."),
        ("Can I take it again?", "Yes. Questions and options are shuffled, and a retake avoids the questions you saw last time."),
        ("Is it free?", "Yes, completely. Both PDFs included.")]),
 "reset": dict(name="HV Reset", verb="Plan your day", color="#4A72C8", tint="#EEF2FB", pline="#D6E0F4", mock=MOCK_RESET, cta="Open HV Reset", story="/#reset",
   title="HV Reset | A calm day, one block at a time",
   desc="HV Reset turns your day into simple blocks: one block, one task. Shift the day when you're late, never skip meals, and let HV AI plan it from one sentence. Free.",
   lead="A day made of simple blocks: one block, one task. You always know what to do right now, and the day bends instead of breaking.",
   facts=[("1 task", "per block"), ("90 min", "longest work block"), ("1 tap", "to shift a late day"), ("HV AI", "plans from one sentence")],
   problem=("“Where did my day go?”", "Notifications, coffee and a to-do list that never shrinks. The clock spins and the important work waits."),
   fix=("One block at a time.", "HV Reset shows only what matters now. If you fall behind, one tap moves the rest of the day, and nothing is lost."),
   steps=[("Open your day", "Today's plan is ready, block by block. Or tell HV AI how your day looks."),
          ("Tap Start", "The big clock shows what's on now and how much time is left."),
          ("Tick and adjust", "Tick blocks off as you go. If the day slips, shift it or do the minimum version.")],
   feats=[("TARGET", "One block, one task", "Each block has one clear job, why it matters, and what “done” looks like."),
          ("CLOCK", "Big focus clock", "A calm countdown for the block you're in, and a focus room that hides everything else."),
          ("LIST", "Full-day timeline", "See the whole day: what's done, what's now and what's next."),
          ("ROUTE", "Running late? Shift the day", "One tap moves the rest of your plan later. Nothing gets lost."),
          ("PAUSE", "Minimum version", "On a hard day, do the smallest useful version of a block instead of skipping it."),
          ("CUP", "Meals and breaks built in", "Lunch and dinner are never skipped, and work blocks stay at 90 minutes or less."),
          ("CHART", "Linked to HV Vault", "Applications and messages are counted for you. See follow-ups due and your week's review."),
          ("NOTE", "Evening reflection", "One good thing from today and tomorrow's first step, so mornings start easy."),
          ("SPARK", "HV AI plans your day", "“Kal subah 10 se 12 apply, 2 se 3 outreach.” It builds the plan and keeps your exact times.")],
   who=[("Students", "Study blocks, real breaks and exam days that don't fall apart."),
        ("Job seekers", "Apply, outreach and prep blocks, counted into HV Vault."),
        ("Professionals", "Protect deep work between meetings."),
        ("Freelancers", "Client work, admin and rest, balanced in one day."),
        ("Creators", "Make, edit and post in focused sessions."),
        ("Anyone restarting", "A gentle routine after a break, one block at a time.")],
   faq=[("Do I have to plan every block myself?", "No. Today's plan is ready when you open it, and HV AI can build or change it from one sentence."),
        ("What happens if I fall behind?", "Tap to shift the rest of the day later, move it to tomorrow, or do the minimum version of a block."),
        ("Does it work with HV Vault?", "Yes. Log an application in HV Reset and it lands in HV Vault as Applied, with its first follow-up."),
        ("Is it free?", "Yes, including HV AI.")]),
 "vault": dict(name="HV Vault", verb="Act on every opportunity", color="#A87A22", tint="#F8F3E8", pline="#EADDC2", mock=MOCK_VAULT, cta="Open HV Vault", story="/#vault",
   title="HV Vault | Every opportunity in one calm place",
   desc="HV Vault keeps every job, company, follow-up and interview in one place. Automatic follow-ups, AI auto-fill, a profile from your resume and HV AI in Hindi, English or Hinglish. Free.",
   lead="Every job, company, follow-up and interview in one calm place, so nothing slips. Just tell HV AI what happened.",
   facts=[("1 board", "Saved to Offer"), ("Auto", "follow-ups"), ("AI", "fills in job posts"), ("Any device", "same data everywhere")],
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
        ("Does HV AI cost anything?", "No. It's built in and free: no key, no setup. Every change shows as a card you confirm."),
        ("Is it free?", "Yes. No card, no trial, no ads.")]),
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
    nxt = "".join('<a class="nx rv" href="/%s/" style="--pc:%s;--tint:%s;--pline:%s">%s<span><b>%s</b><small>%s</small></span>%s</a>' % (
        k, APPS[k]["color"], APPS[k]["tint"], APPS[k]["pline"], logo(k), APPS[k]["name"], APPS[k]["verb"], ARROW) for k in ORDER if k != key)
    return '''<main id="main" class="pp" style="--pc:%(color)s;--tint:%(tint)s;--pline:%(pline)s">
  <section class="phero" id="top"><div class="wrap">
    <div class="rv">
      <p class="crumb"><a href="/overview/">HV World</a> <span>/</span> %(name)s</p>
      <div class="pname">%(logo)s<div><h1>%(name)s</h1><p class="verb">%(verb)s</p></div></div>
      <p class="lead">%(lead)s</p>
      <div class="ctas"><a class="btn" href="%(url)s">%(cta)s %(arrow)s</a><a class="btn ghost" href="#features">See every feature</a></div>
    </div>
    <div class="pmock rv">%(mock)s</div>
  </div></section>
  <div class="wrap facts rv">%(facts)s</div>

  <section class="pp-sec"><div class="wrap pf">
    <div class="rv"><p class="label">The problem</p><h2>%(p1)s</h2><p>%(p2)s</p></div>
    <div class="rv"><p class="label pc">What %(name)s does</p><h2>%(f1)s</h2><p>%(f2)s</p><a class="more" href="%(story)s">See it in Riya's story %(arrow)s</a></div>
  </div></section>

  <section class="pp-sec"><div class="wrap">
    <div class="head rv"><p class="label">How it works</p><h2>Three steps. That's it.</h2></div>
    <div class="steps3">%(steps)s</div>
  </div></section>

  <section class="pp-sec" id="features"><div class="wrap">
    <div class="head rv"><p class="label">Every feature</p><h2>Everything %(name)s does.</h2></div>
    <div class="fgrid rv">%(feats)s</div>
  </div></section>

  <section class="pp-sec"><div class="wrap">
    <div class="head rv"><p class="label">Who it's for</p><h2>Made for every walk of life.</h2></div>
    <div class="who rv">%(who)s</div>
  </div></section>

  <section class="pp-sec"><div class="wrap">
    <div class="head rv"><p class="label">FAQ</p><h2>Questions about %(name)s.</h2></div>
    <div class="faq rv">%(faq)s</div>
    <div class="pcta rv"><a class="btn" href="%(url)s">%(cta)s %(arrow)s</a></div>
  </div></section>

  <section class="pp-sec next"><div class="wrap">
    <p class="label">The rest of HV World</p>
    <div class="nxs">%(nxt)s</div>
    <p class="back"><a href="/overview/">See all three apps together %(arrow)s</a></p>
  </div></section>
</main>''' % dict(a, logo=logo(key), url=URL[key], arrow=ARROW, facts=facts, steps=steps, feats=feats, who=who, faq=faq, nxt=nxt,
                  p1=a["problem"][0], p2=a["problem"][1], f1=a["fix"][0], f2=a["fix"][1])

# ---------------------------------------------------------------- shared page shell
def shell(path, title, desc, og, body, active):
    nav = [("overview", "/overview/", "Overview", "opt"), ("test", "/test/", '<span class="d">HV </span>Test', ""),
           ("reset", "/reset/", '<span class="d">HV </span>Reset', ""), ("vault", "/vault/", '<span class="d">HV </span>Vault', "")]
    links = "".join('<a class="%s"%s href="%s">%s</a>' % (c, ' aria-current="page"' if k == active else "", h, t) for k, h, t, c in nav)
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
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<style>%s</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="wrap nav"><a class="brand" href="/overview/">%sHV World</a>
<nav aria-label="Main">%s<a class="story" href="/"><span class="d">Riya's </span>Story</a></nav></div></header>
%s
<footer><div class="wrap row"><span>© <span id="yr">2026</span> Harsh Vittori · HV World</span>
<nav aria-label="Footer"><a href="/">Riya's story</a><a href="/overview/">Overview</a><a href="/test/">HV Test</a><a href="/reset/">HV Reset</a><a href="/vault/">HV Vault</a><a href="https://www.linkedin.com/in/harshvittori" target="_blank" rel="noopener">LinkedIn</a><a href="https://github.com/harshvittori" target="_blank" rel="noopener">GitHub</a></nav></div></footer>
<script>
(function () {
  document.getElementById("yr").textContent = new Date().getFullYear();
  var els = document.querySelectorAll(".rv");
  if (!("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("in"); }); return; }
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8%% 0px" });
  els.forEach(function (e) { io.observe(e); });
})();
</script>
</body>
</html>
''' % (title, desc, url, title.replace(" | ", ": "), desc, url, og, CSS, logo("world"), links, body)

def fill(page):
    page = page.replace("__PRODUCTS__", "\n".join(product(*p, flip=(i == 1)) for i, p in enumerate(PRODUCTS)))
    page = page.replace("__FAQ__", "".join('<details><summary>%s</summary><p>%s</p></details>' % qa for qa in FAQ))
    page = page.replace("__MOCK_AI__", MOCK_AI)
    for k, v in {"ARROW": ARROW, "CHECK": CHECK, "SYNC": SYNC, "USER": USER, "SPARK": SPARK}.items():
        page = page.replace("__%s__" % k, v)
    for k in ("TEST", "RESET", "VAULT"):
        page = page.replace("__U_%s__" % k, URL[k.lower()])
    page = re.sub(r"__LOGO_(WORLD|TEST|RESET|VAULT)(_P)?__", lambda m: logo(m.group(1).lower()), page)
    left = re.findall(r"__[A-Z_]+__", page)
    assert not left, left
    return page

def write(path, page):
    d = os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(page)
    print("ok", path, len(page), "bytes")

def build():
    write("/overview/", fill(shell("/overview/", "HV World | All three apps: HV Test, HV Reset, HV Vault",
          "Everything in HV World: HV Test to know yourself, HV Reset to plan your day, HV Vault to act on every opportunity, and HV AI in Hindi, English or Hinglish. Free, by Harsh Vittori.",
          "https://harshvittori.github.io/overview/og.png", OVERVIEW_MAIN, "overview")))
    for k in ORDER:
        a = APPS[k]
        write("/%s/" % k, fill(shell("/%s/" % k, a["title"], a["desc"], "https://harshvittori.github.io/%s/og.png" % k, app_page(k), k)))

if __name__ == "__main__":
    build()
