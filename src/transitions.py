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
