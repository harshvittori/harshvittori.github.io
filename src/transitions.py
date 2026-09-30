"""Smooth, app-like page switching shared by every HV World page.

Uses the browser's cross-document View Transitions (the menu stays put, the page content slides like
switching tabs, direction follows the menu order) and Speculation Rules (a page is prerendered when you
hover or touch its link, so it opens instantly). Browsers without support just navigate normally."""

ORDER = ["/", "/test/", "/reset/", "/vault/", "/watch/", "/story/"]

CSS = r"""
@view-transition{navigation:auto}
header{view-transition-name:site-header}
main{view-transition-name:page}
::view-transition-group(site-header){animation:none}
::view-transition-old(site-header){display:none}
::view-transition-new(site-header){animation:none}
::view-transition-old(page){animation:vt-fade-out .2s cubic-bezier(.4,0,1,1) both}
::view-transition-new(page){animation:vt-rise-in .42s cubic-bezier(.2,.8,.2,1) both}
html:active-view-transition-type(forward)::view-transition-old(page){animation:vt-out-left .28s cubic-bezier(.4,0,.2,1) both}
html:active-view-transition-type(forward)::view-transition-new(page){animation:vt-in-right .42s cubic-bezier(.2,.8,.2,1) both}
html:active-view-transition-type(back)::view-transition-old(page){animation:vt-out-right .28s cubic-bezier(.4,0,.2,1) both}
html:active-view-transition-type(back)::view-transition-new(page){animation:vt-in-left .42s cubic-bezier(.2,.8,.2,1) both}
@keyframes vt-fade-out{to{opacity:0}}
@keyframes vt-rise-in{from{opacity:0;transform:translateY(16px)}}
@keyframes vt-out-left{to{opacity:0;transform:translateX(-48px)}}
@keyframes vt-in-right{from{opacity:0;transform:translateX(64px)}}
@keyframes vt-out-right{to{opacity:0;transform:translateX(48px)}}
@keyframes vt-in-left{from{opacity:0;transform:translateX(-64px)}}
@media (prefers-reduced-motion:reduce){::view-transition-group(*),::view-transition-old(*),::view-transition-new(*){animation:none!important}}
"""

HEAD = ("""<script type="speculationrules">{"prerender":[{"urls":%s,"eagerness":"moderate"}]}</script>
<script>
// reload keeps the reader exactly where they were: the browser's own restore can land a little lower each time
// (smooth scrolling plus content settling above), so the page saves its position and puts it back instantly
(function () {
  if (!("scrollRestoration" in history)) return;
  history.scrollRestoration = "manual";
  var K = "hvscroll:" + location.pathname, nav = performance.getEntriesByType && performance.getEntriesByType("navigation")[0];
  var type = nav ? nav.type : "", y = null;
  try { if (type === "reload" || type === "back_forward") y = +sessionStorage.getItem(K); } catch (e) {}
  addEventListener("pagehide", function () { try { sessionStorage.setItem(K, String(Math.round(scrollY))); } catch (e) {} });
  if (location.hash || !(y > 0)) return;
  var put = function () { if (Math.abs(scrollY - y) > 2) scrollTo({ top: y, left: 0, behavior: "instant" }); };
  addEventListener("DOMContentLoaded", put); addEventListener("load", function () { put(); setTimeout(put, 120); });
  // stop restoring once the reader scrolls on their own
  var stop = function () { put = function () {}; };
  addEventListener("wheel", stop, { passive: true, once: true }); addEventListener("touchstart", stop, { passive: true, once: true }); addEventListener("keydown", stop, { once: true });
})();
(function () {
  var ORDER = %s;
  function idx(u) { try { var p = new URL(u, location.href).pathname; return ORDER.indexOf(p); } catch (e) { return -1; } }
  // tell the transition which way to slide: along the menu order, like switching tabs
  window.addEventListener("pageswap", function (e) {
    if (!e.viewTransition || !e.activation || !e.activation.entry) return;
    var a = idx(location.href), b = idx(e.activation.entry.url);
    if (a > -1 && b > -1 && a !== b) e.viewTransition.types.add(b > a ? "forward" : "back");
  });
  window.addEventListener("pagereveal", function (e) {
    if (!e.viewTransition || !navigation || !navigation.activation || !navigation.activation.from) return;
    var a = idx(navigation.activation.from.url), b = idx(location.href);
    if (a > -1 && b > -1 && a !== b) e.viewTransition.types.add(b > a ? "forward" : "back");
  });
})();
</script>""") % (str(ORDER).replace("'", '"'), str(ORDER).replace("'", '"'))


# ---------------------------------------------------------------- phone menu: app icons instead of words
# On screens up to 720px the main menu shows icons: Home, the three apps, Watch and Riya's story, all black-and-white
# line icons; the page you are on sits in a soft blue pill (an app page shows its colour logo there); a long press (phones) or hover (devices with a pointer) shows the name, and every
# icon keeps its name for screen readers. Wider screens keep the words.
NAV_CSS = """
.nav nav a .mi{display:none}
.nav nav a.mn::after{content:attr(data-tip);position:absolute;top:calc(100% + 8px);left:50%;transform:translate(-50%,-4px);z-index:60;white-space:nowrap;font-size:13px;font-weight:600;line-height:1;color:#fff;background:#1D1D1F;padding:7px 10px;border-radius:9px;opacity:0;pointer-events:none;transition:opacity .18s,transform .18s;display:none}
@media (max-width:720px){
  .nav{height:58px}
  .nav nav{gap:2px}
  .nav nav a.mn,.nav nav a.opt.mn{display:grid;place-items:center;width:42px;height:42px;padding:0;line-height:0;border-radius:14px;font-size:0;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none}
  .nav nav a.mn .mt{display:none}
  .nav nav a.mn .mi{display:block}
  .nav nav a.mn .mi.col,.nav nav a.mn[aria-current] .mi.mono,.nav nav a.mn:active .mi.mono{display:none}
  .nav nav a.mn[aria-current] .mi.col,.nav nav a.mn:active .mi.col{display:block}
  .nav nav a.mn .mi svg{display:block;width:30px;height:30px;border-radius:8.5px;box-shadow:0 4px 10px -6px rgba(20,30,90,.6)}
  .nav nav a.mn .mi.line svg,.nav nav a.mn.ic .ni{width:24px;height:24px;border-radius:0;box-shadow:none;margin:0}
  .nav nav a.mn .mi.mono svg{width:25px;height:25px}
  .nav nav a.mn[aria-current]{background:#E8ECFB;box-shadow:inset 0 0 0 1px rgba(46,67,166,.16)}
  .nav nav a.mn::after{display:block}
  .nav nav a.mn:nth-last-child(-n+2)::after{left:auto;right:0;transform:translate(0,-4px)}
  .nav nav a.mn.tipon::after{opacity:1;transform:translate(-50%,0)}
  .nav nav a.mn.tipon:nth-last-child(-n+2)::after{transform:none}
}
@media (max-width:720px) and (hover:hover){
  .nav nav a.mn:hover::after{opacity:1;transform:translate(-50%,0)}
  .nav nav a.mn:nth-last-child(-n+2):hover::after{transform:none}
}
@media (max-width:360px){.nav nav a.mn,.nav nav a.opt.mn{width:38px}.nav nav a.mn .mi svg{width:28px;height:28px}}
"""
NAV_JS = """<script>
// phone menu: a long press shows the page name instead of opening the page
(function () {
  var go = function () {
    document.querySelectorAll(".nav nav a.mn").forEach(function (a) {
      var t = 0, long = false, hide = 0;
      var tip = function () { long = true; a.classList.add("tipon"); clearTimeout(hide); hide = setTimeout(function () { a.classList.remove("tipon"); }, 1600); };
      a.addEventListener("touchstart", function () { long = false; clearTimeout(t); t = setTimeout(tip, 450); }, { passive: true });
      a.addEventListener("touchmove", function () { clearTimeout(t); }, { passive: true });
      a.addEventListener("touchend", function (e) { clearTimeout(t); if (long) e.preventDefault(); });
      a.addEventListener("click", function (e) { if (long) { e.preventDefault(); long = false; } });
      a.addEventListener("contextmenu", function (e) { e.preventDefault(); });
    });
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go); else go();
})();
</script>"""
MONO = {
    "test": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="7.5" r="3.5"/><circle cx="16.5" cy="7.5" r="3.5"/><circle cx="7.5" cy="16.5" r="3.5"/><path d="M13.2 16.6l2.3 2.3 4.3-4.6"/></svg>',
    "reset": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19.3 9A8 8 0 1 0 20 13"/><path d="M20 4.5V9h-4.5"/><circle cx="12" cy="12" r="2.6" fill="currentColor" stroke="none"/></svg>',
    "vault": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.6 3.3a9 9 0 1 0 4.8 0"/><path d="M10.3 7.3a5 5 0 1 0 3.4 0"/><path d="M12 2.5v6"/><circle cx="12" cy="12.2" r="1.7" fill="currentColor" stroke="none"/></svg>',
}
HOME_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V20h5v-6h4v6h5V9.5"/></svg>'

def nav_icons(page, logo):
    import re
    m = re.search(r'<nav aria-label="Main">(.*?)</nav>', page, re.S)
    if not m:
        return page
    names = {"/": ("Home", None), "/test/": ("HV Test", "test"), "/reset/": ("HV Reset", "reset"), "/vault/": ("HV Vault", "vault"),
             "/watch/": ("Watch", None), "/story/": ("Riya's story", None)}
    def fix(a):
        tag, inner = a.group(1), a.group(2)
        h = re.search(r'href="([^"]+)"', tag)
        if not h or h.group(1) not in names:
            return a.group(0)
        name, app = names[h.group(1)]
        tag = re.sub(r'class="([^"]*)"', lambda c: 'class="%s mn"' % c.group(1), tag) if 'class="' in tag else tag.replace("<a ", '<a class="mn" ', 1)
        tag = re.sub(r' aria-label="[^"]*"', "", tag)
        tag = tag.replace("<a ", '<a aria-label="%s" data-tip="%s" ' % (name, name), 1)
        if h.group(1) in ("/watch/", "/story/"):
            return tag + inner + "</a>"
        if not app:
            return tag + '<span class="mt">' + inner + '</span><span class="mi line" aria-hidden="true">%s</span></a>' % HOME_ICON
        # app pages: a black-and-white line icon like the others, and the colour logo on the page you're on (or while pressed)
        return tag + '<span class="mt">' + inner + '</span><span class="mi line mono" aria-hidden="true">%s</span><span class="mi col" aria-hidden="true">%s</span></a>' % (MONO[app], logo(app))
    navhtml = re.sub(r'(<a [^>]*>)(.*?)</a>', fix, m.group(1), flags=re.S)
    page = page[:m.start(1)] + navhtml + page[m.end(1):]
    return page.replace("</style>", NAV_CSS + "</style>", 1).replace("</body>", NAV_JS + "\n</body>", 1)
