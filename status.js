/* HV World live settings: maintenance mode, announcement banner and a few page switches, controlled from /admin/.
   Loaded first on every page of HV World, HV Test, HV Reset and HV Vault (all on harshvittori.github.io).
   It reads one public Firestore document (config/site); only the admin account can change it (Firestore rules).
   Everything here fails open: if anything goes wrong, the site simply works as normal. */
(function () {
  "use strict";
  try {
    var URL_ = "https://firestore.googleapis.com/v1/projects/harsh-reset/databases/(default)/documents/config/site?key=AIzaSyDggasAVdqpvamkn1xeex2NmPUqG9JiZJ4";
    var KEY = "hvstatus:v1", p = location.pathname;
    var SITE = /^\/hv-tests(\/|$)/.test(p) ? "test" : /^\/(hv-reset|harsh-reset)(\/|$)/.test(p) ? "reset" : /^\/hv-vault-web(\/|$)/.test(p) ? "vault" : "world";
    var NAMES = { world: "HV World", test: "HV Test", reset: "HV Reset", vault: "HV Vault" };
    if (/^\/admin(\/|$)/.test(p)) return;                                   // the admin page itself is never blocked
    var qs = location.search, preview = /[?&]hvpreview=maintenance\b/.test(qs);
    var admin = false; try { admin = localStorage.getItem("hvadmin") === "1"; } catch (e) {}
    var cfg = null; try { cfg = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) {}
    var d = document.documentElement;
    window.HVStatus = { site: SITE, cfg: cfg || {} };

    var num = function (v) { var t = v ? Date.parse(v) : NaN; return isNaN(t) ? null : t; };
    var maint = function (c) {
      var m = c && c.sites && c.sites[SITE] && c.sites[SITE].maintenance;
      if (preview) return m || { on: true };
      if (!m || !m.on) return null;
      var now = Date.now(), from = num(m.from), until = num(m.until);
      if (from && now < from) return null;
      if (until && now >= until) return null;
      return m;
    };
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var left = function (ms) { var t = Math.max(0, Math.floor(ms / 1000)), h = Math.floor(t / 3600), m = Math.floor(t % 3600 / 60), s = t % 60; return (h ? h + "h " : "") + pad(m) + "m " + pad(s) + "s"; };
    var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
    var safeUrl = function (u) { return /^(https?:\/\/|\/)/.test(u || "") ? u : ""; };

    /* ---------- maintenance screen ---------- */
    var host = null, tickT = 0, stopper = null;
    var block = function (e) {
      if (!d.classList.contains("hvmaint")) return;
      if (e.composedPath && e.composedPath().some(function (n) { return n && n.id === "hvMaint"; })) return;
      e.stopImmediatePropagation(); if (e.type !== "pointerdown" && e.type !== "touchstart") e.preventDefault();
    };
    // each site's maintenance screen wears that site's own look (colours, type, logo)
    var LOGO = {"world": "<svg viewBox=\"0 0 48 48\"><defs><linearGradient id=\"hvw-1\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"><stop offset=\"0\" stop-color=\"#1C2A6B\"/><stop offset=\".6\" stop-color=\"#4A46C9\"/><stop offset=\"1\" stop-color=\"#7C5CE0\"/></linearGradient><radialGradient id=\"hvwc-1\" cx=\".4\" cy=\".35\" r=\".7\"><stop offset=\"0\" stop-color=\"#FFFFFF\"/><stop offset=\"1\" stop-color=\"#C9D3FF\"/></radialGradient></defs><rect width=\"48\" height=\"48\" rx=\"12\" fill=\"url(#hvw-1)\"/><ellipse cx=\"24\" cy=\"24\" rx=\"16.5\" ry=\"7.5\" fill=\"none\" stroke=\"#fff\" stroke-opacity=\".55\" stroke-width=\"1.8\" transform=\"rotate(-24 24 24)\"/><circle cx=\"24\" cy=\"24\" r=\"6.2\" fill=\"url(#hvwc-1)\"/><circle cx=\"37.6\" cy=\"17.9\" r=\"3.3\" fill=\"#F2C063\"/><circle cx=\"10.4\" cy=\"30.1\" r=\"3.3\" fill=\"#34C77B\"/><circle cx=\"17.4\" cy=\"14.6\" r=\"2.6\" fill=\"#F2A77E\"/></svg>", "test": "<svg viewBox=\"0 0 48 48\"><rect width=\"48\" height=\"48\" rx=\"12\" fill=\"#127A4F\"/><circle cx=\"16.5\" cy=\"16.5\" r=\"5.5\" stroke=\"#FFFFFF\" stroke-width=\"3\" fill=\"none\"/><circle cx=\"31.5\" cy=\"16.5\" r=\"5.5\" stroke=\"#FFFFFF\" stroke-width=\"3\" fill=\"none\"/><circle cx=\"16.5\" cy=\"31.5\" r=\"5.5\" stroke=\"#FFFFFF\" stroke-width=\"3\" fill=\"none\"/><circle cx=\"31.5\" cy=\"31.5\" r=\"7.5\" fill=\"#FFC54D\"/><path d=\"M28 31.6l2.5 2.5 4.8-5\" stroke=\"#17231C\" stroke-width=\"2.6\" fill=\"none\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>", "reset": "<svg viewBox=\"0 0 1024 1024\"><defs><linearGradient id=\"hvrbg-3\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"><stop offset=\"0\" stop-color=\"#5B86D6\"/><stop offset=\".55\" stop-color=\"#9C8BDA\"/><stop offset=\"1\" stop-color=\"#F2A77E\"/></linearGradient><radialGradient id=\"hvrsun-3\" cx=\".5\" cy=\".42\" r=\".6\"><stop offset=\"0\" stop-color=\"#FFF6DA\"/><stop offset=\".6\" stop-color=\"#FFD58F\"/><stop offset=\"1\" stop-color=\"#FFB066\"/></radialGradient><radialGradient id=\"hvrglow-3\" cx=\".5\" cy=\".5\" r=\".5\"><stop offset=\"0\" stop-color=\"#FFE9B8\" stop-opacity=\".75\"/><stop offset=\"1\" stop-color=\"#FFE9B8\" stop-opacity=\"0\"/></radialGradient></defs><rect width=\"1024\" height=\"1024\" rx=\"232\" fill=\"url(#hvrbg-3)\"/><circle cx=\"512\" cy=\"530\" r=\"300\" fill=\"url(#hvrglow-3)\"/><circle cx=\"512\" cy=\"530\" r=\"138\" fill=\"url(#hvrsun-3)\"/><path d=\"M704 318A292 292 0 1 1 452 244\" fill=\"none\" stroke=\"#fff\" stroke-width=\"62\" stroke-linecap=\"round\"/><path d=\"M548 225L454 318L424 176Z\" fill=\"#fff\" stroke=\"#fff\" stroke-width=\"30\" stroke-linejoin=\"round\"/></svg>", "vault": "<svg viewBox=\"0 0 1024 1024\"><defs><linearGradient id=\"hvaimk-4\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"><stop offset=\"0\" stop-color=\"#1B3157\"/><stop offset=\".5\" stop-color=\"#152647\"/><stop offset=\"1\" stop-color=\"#0C1830\"/></linearGradient></defs><rect width=\"1024\" height=\"1024\" rx=\"230\" fill=\"url(#hvaimk-4)\"/><path d=\"M 608.00 360.68 A 179.2 179.2 0 1 1 416.00 360.68\" fill=\"none\" stroke=\"#DFC18A\" stroke-width=\"96\" stroke-linecap=\"round\"/><path d=\"M 608.00 206.74 A 320 320 0 1 1 416.00 206.74\" fill=\"none\" stroke=\"#C9A45E\" stroke-width=\"83.2\" stroke-linecap=\"round\"/><circle cx=\"512\" cy=\"512\" r=\"96\" fill=\"#EAD9B0\"/></svg>"};
    var BASE = ':host{all:initial}*{box-sizing:border-box;margin:0}' +
      '.w{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;padding:24px;text-align:center;overflow:auto}' +
      '.g{max-width:540px;width:100%;padding:38px 28px 34px}.lg svg{display:block;width:100%;height:100%}' +
      '.n{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;font-weight:600;letter-spacing:.02em;padding:7px 13px;border-radius:999px}.n i{width:7px;height:7px;border-radius:50%;background:currentColor}' +
      'h1{font-size:clamp(26px,5.2vw,38px);font-weight:700;letter-spacing:-.03em;line-height:1.12;margin:18px 0 0}' +
      '.m{font-size:16px;line-height:1.55;margin:12px auto 0;max-width:440px;white-space:pre-line}' +
      '.k{font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;margin:26px 0 0}' +
      '.c{font-size:clamp(36px,8vw,54px);font-weight:700;letter-spacing:-.04em;font-variant-numeric:tabular-nums;line-height:1.1;margin:4px 0 0}' +
      '.d{font-size:14px;margin:6px 0 0}' +
      '.pv{position:fixed;top:14px;left:50%;transform:translateX(-50%);font:600 12px/1 system-ui,sans-serif;color:#fff;background:#1D1D1F;padding:7px 12px;border-radius:999px;z-index:2}';
    var THEME = {
      world: '.w{font-family:HVSora,Sora,Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#0B0D1A;background:radial-gradient(60% 55% at 18% 25%,#AEB8F5 0,transparent 70%),radial-gradient(55% 55% at 85% 80%,#CDB9F4 0,transparent 70%),radial-gradient(45% 40% at 60% 10%,#fff 0,transparent 70%),#E6E8F6}' +
        '.g{border-radius:30px;background:rgba(255,255,255,.58);-webkit-backdrop-filter:blur(22px) saturate(1.6);backdrop-filter:blur(22px) saturate(1.6);border:1px solid rgba(255,255,255,.9);box-shadow:0 30px 70px -30px rgba(46,67,166,.45),inset 0 1px 0 #fff}' +
        '.lg{width:60px;height:60px;margin:0 auto 18px;border-radius:17px;overflow:hidden;box-shadow:0 16px 30px -14px rgba(46,67,166,.6)}.n{color:#2E43A6;background:rgba(255,255,255,.8);border:1px solid rgba(255,255,255,.95)}.m{color:#474C68}.k{color:#4B55A8}.d{color:#555B7A}',
      test: '.w{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#17231C;background:radial-gradient(55% 50% at 85% 10%,rgba(18,122,79,.1),transparent 70%),radial-gradient(45% 45% at 10% 90%,rgba(255,197,77,.12),transparent 70%),#F7FAF7}' +
        '.g{border-radius:20px;background:#fff;border:1px solid #D3E7DA;box-shadow:0 24px 50px -32px rgba(18,122,79,.45)}' +
        '.br{display:flex;justify-content:center;align-items:center;gap:8px;font-weight:800;font-size:14px;letter-spacing:.06em;margin-bottom:22px}.br .lg{width:24px;height:24px;border-radius:6px;overflow:hidden}.br b{color:#127A4F}' +
        'h1{font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;font-weight:600;letter-spacing:-.02em}h1::after{content:"";display:block;width:44px;height:4px;border-radius:4px;background:#F2A33A;margin:14px auto 0}' +
        '.n{color:#127A4F;background:#EEF6F1;border:1px solid #D3E7DA}.m{color:#4A5A50}.k{color:#127A4F}.c{color:#127A4F}.d{color:#6B7A70}',
      reset: '.w{font-family:"Atkinson Hyperlegible","Segoe UI",system-ui,sans-serif;color:#EEF1F7;background:radial-gradient(38% 34% at 78% 72%,rgba(255,176,102,.55),transparent 70%),radial-gradient(40% 40% at 12% 18%,rgba(156,139,218,.35),transparent 70%),linear-gradient(180deg,#1C2853 0%,#2E2A5E 55%,#5B3F6B 82%,#8E5B6A 100%)}' +
        '.g{border-radius:26px;background:rgba(255,255,255,.07);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,.14);box-shadow:0 30px 70px -30px rgba(0,0,0,.6)}' +
        '.lg{width:66px;height:66px;margin:0 auto 18px;border-radius:18px;overflow:hidden;box-shadow:0 18px 36px -14px rgba(255,176,102,.55)}h1{font-family:Sora,"Segoe UI",system-ui,sans-serif;color:#fff}' +
        '.n{color:#FFD9B0;background:rgba(255,176,102,.14);border:1px solid rgba(255,176,102,.3)}.m{color:#C9CFE3}.k{color:#A3B6FF}.c{color:#fff}.d{color:#AEB6D6}',
      vault: '.w{font-family:Sora,Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#12213B;background:radial-gradient(55% 55% at 15% 15%,#D6D3F4 0,transparent 70%),radial-gradient(55% 55% at 90% 90%,#F8D6C2 0,transparent 70%),#E9E6F2}' +
        '.g{border-radius:26px;background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(20px) saturate(1.5);backdrop-filter:blur(20px) saturate(1.5);border:1px solid rgba(255,255,255,.95);box-shadow:0 26px 60px -30px rgba(18,33,59,.45)}' +
        '.br{display:flex;justify-content:center;align-items:center;gap:10px;text-align:left;margin-bottom:20px}.br .lg{width:40px;height:40px;border-radius:12px;overflow:hidden}.br b{display:block;font-size:15px}.br small{display:block;font-size:11.5px;color:#6A7390}' +
        'h1 em{font-style:normal;background:linear-gradient(90deg,#6E5BD8,#B07BD6);-webkit-background-clip:text;background-clip:text;color:transparent}' +
        '.n{color:#3B55D9;background:#EEF1FD;border:1px solid #DDE3FB}.m{color:#4E5877}.k{color:#3B55D9}.c{color:#12213B}.d{color:#6A7390}'
    };
    var head = function () {
      if (SITE === "test") return '<div class="br"><span class="lg">' + LOGO.test + '</span><span>HV <b>TEST</b></span></div>';
      if (SITE === "vault") return '<div class="br"><span class="lg">' + LOGO.vault + '</span><span><b>HV Vault</b><small>Job-hunt command center</small></span></div>';
      return '<div class="lg">' + LOGO[SITE] + '</div>';
    };
    var title = function () { return SITE === "vault" ? 'HV Vault will be <em>right back</em>.' : esc(NAMES[SITE]) + ' will be right back.'; };
    var showMaint = function (m) {
      if (!document.body) { document.addEventListener("DOMContentLoaded", function () { showMaint(m); }); return; }
      d.classList.add("hvmaint");
      // popups sit in the browser's top layer, above any z-index: close them so the maintenance screen stays on top
      try { document.querySelectorAll("dialog[open]").forEach(function (x) { x.close(); }); } catch (e) {}
      if (!stopper) { stopper = true; ["pointerdown", "mousedown", "click", "touchstart", "keydown", "keyup"].forEach(function (t) { window.addEventListener(t, block, true); }); }
      if (!host) { host = document.createElement("div"); host.id = "hvMaint"; host.setAttribute("role", "dialog"); host.setAttribute("aria-live", "polite"); (host.attachShadow ? host.attachShadow({ mode: "open" }) : host); document.body.appendChild(host); }
      var root = host.shadowRoot || host, until = num(m.until);
      var msg = m.message || "Sorry for the inconvenience. We're working on a better experience for you and will be back shortly.";
      root.innerHTML = '<style>' + BASE + THEME[SITE] + '</style><div class="w">' + (preview ? '<span class="pv">Preview: this is what visitors see</span>' : '') + '<div class="g">' + head() + '<span class="n"><i></i>Maintenance</span><h1>' + title() + '</h1><p class="m">' + esc(msg) + '</p>' +
        (until ? '<p class="k">Back in</p><p class="c" role="timer"></p><p class="d">' + esc(new Date(until).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })) + '</p>' : '') + '</div></div>';
      clearTimeout(tickT);
      if (until) { var c = root.querySelector(".c"); var tick = function () { var ms = until - Date.now(); if (ms <= 0) { if (!preview) location.reload(); return; } c.textContent = left(ms); tickT = setTimeout(tick, 1000 - Date.now() % 1000 + 5); }; tick(); }
    };
    var hideMaint = function () { d.classList.remove("hvmaint"); clearTimeout(tickT); if (host) { host.remove(); host = null; } };
    var st = document.createElement("style");
    st.textContent = "html.hvmaint,html.hvmaint body{overflow:hidden!important}html.hvmaint body>*:not(#hvMaint){visibility:hidden!important}html.hvmaint body>#hvMaint#hvMaint{position:fixed!important;inset:0!important;z-index:2147483647!important;display:block!important;visibility:visible!important}" +
      "html body>a#hvAdminPill#hvAdminPill{position:fixed!important;left:50%;bottom:16px;transform:translateX(-50%);z-index:2147483647!important;visibility:visible!important;display:block!important;max-width:calc(100vw - 24px);font:600 13px/1.35 system-ui,sans-serif;text-align:center;text-decoration:none;color:#8A5A00;background:#FFF3D6;border:1px solid #F5DDA6;padding:10px 14px;border-radius:14px;box-shadow:0 12px 28px -12px rgba(0,0,0,.35)}";
    (document.head || d).appendChild(st);

    /* ---------- announcement banner ---------- */
    var bar = null;
    var banner = function (c) {
      var b = c && c.banner, now = Date.now();
      var on = b && b.on && b.text && (!b.sites || b.sites.indexOf(SITE) > -1) && !(num(b.until) && now >= num(b.until));
      var id = on ? "hvbn:" + (b.id || b.text) : "";
      var dismissed = false; try { dismissed = on && sessionStorage.getItem(id) === "1"; } catch (e) {}
      if (!on || dismissed) { if (bar) { bar.remove(); bar = null; } return; }
      if (!document.body) { document.addEventListener("DOMContentLoaded", function () { banner(c); }); return; }
      if (!bar) { bar = document.createElement("div"); bar.id = "hvBanner"; (bar.attachShadow ? bar.attachShadow({ mode: "open" }) : bar); document.body.appendChild(bar); }
      var tones = { info: ["#1D2B72", "rgba(255,255,255,.82)", "#2E43A6"], success: ["#0F5C3A", "rgba(236,250,243,.9)", "#1FA463"], warning: ["#7A4B00", "rgba(255,247,228,.92)", "#E0A21A"] };
      var t = tones[b.tone] || tones.info, link = safeUrl(b.link);
      (bar.shadowRoot || bar).innerHTML = '<style>:host{all:initial}.b{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:2147483600;display:flex;align-items:center;gap:12px;max-width:calc(100vw - 24px);width:max-content;padding:10px 10px 10px 16px;border-radius:16px;font:500 14px/1.35 Sora,Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:' + t[0] + ';background:' + t[1] + ';-webkit-backdrop-filter:blur(16px) saturate(1.6);backdrop-filter:blur(16px) saturate(1.6);border:1px solid rgba(255,255,255,.95);box-shadow:0 18px 40px -16px rgba(20,30,90,.45);animation:up .35s ease}' +
        '@keyframes up{from{opacity:0;transform:translate(-50%,10px)}}@media (prefers-reduced-motion:reduce){.b{animation:none}}i{flex:none;width:8px;height:8px;border-radius:50%;background:' + t[2] + '}a{color:inherit;font-weight:700;white-space:nowrap}button{flex:none;width:28px;height:28px;border:0;border-radius:50%;background:rgba(0,0,0,.06);color:inherit;font-size:18px;line-height:1;cursor:pointer}</style>' +
        '<div class="b" role="status"><i></i><span>' + esc(b.text) + (link ? ' <a href="' + esc(link) + '">' + esc(b.linkText || "Learn more") + ' &rarr;</a>' : '') + '</span><button type="button" aria-label="Dismiss">&times;</button></div>';
      (bar.shadowRoot || bar).querySelector("button").onclick = function () { try { sessionStorage.setItem(id, "1"); } catch (e) {} bar.remove(); bar = null; };
    };

    // on the admin's own device the real site shows instead of the maintenance screen; this notice says so (and links to the preview)
    var adminPill = function (on) {
      if (!document.body) { document.addEventListener("DOMContentLoaded", function () { adminPill(on); }); return; }
      var pill = document.getElementById("hvAdminPill");
      if (!on) { if (pill) pill.remove(); return; }
      if (!pill) { pill = document.createElement("a"); pill.id = "hvAdminPill"; document.body.appendChild(pill); }
      pill.href = location.pathname + (location.search ? location.search + "&" : "?") + "hvpreview=maintenance";
      pill.textContent = "Maintenance is ON for visitors · you're signed in as admin, so you see the site · See what visitors see →";
      // keep it last in the page so it stays above other full-screen layers (like the premiere screen)
      var last = function () { if (pill.isConnected && document.body.lastElementChild !== pill) document.body.appendChild(pill); };
      setTimeout(last, 0); addEventListener("load", last);
    };
    // the premiere gate on the apps swallows clicks; open the preview ourselves (this listener is added before the gate's)
    window.addEventListener("click", function (e) { var a = e.target && e.target.closest && e.target.closest("#hvAdminPill"); if (a) { e.preventDefault(); e.stopImmediatePropagation(); location.href = a.href; } }, true);
    var apply = function (c) {
      window.HVStatus.cfg = c || {};
      var m = maint(c);
      if (m && !(admin && !preview)) showMaint(m); else hideMaint();
      adminPill(!!(m && admin && !preview));
      banner(c);
      try { window.dispatchEvent(new CustomEvent("hvstatus", { detail: c || {} })); } catch (e) {}
    };
    if (cfg) apply(cfg);
    /* App Check: once Firestore requires it, a request without a valid token is refused (401/403).
       A token saved from an earlier page goes along if there is one. Otherwise, only when a request is
       refused, get one: HV Vault and HV Reset share their own (HVCloud), HV Test pages share the
       scorecard's (HVScorecard), and pages with no Firebase at all load App Check themselves. This file
       never loads Firebase on a page that brings its own, so their sign-in is untouched. */
    var ACK = "hvac:v1", SDK = "https://www.gstatic.com/firebasejs/10.12.2/";
    var acSaved = function () { try { var o = JSON.parse(localStorage.getItem(ACK) || "null"); if (o && o.exp > Date.now() + 60000) return o.t; } catch (e) {} return null; };
    var acSave = function (t) { try { var j = JSON.parse(atob(t.split(".")[1].replace(/-/g, "+").replace(/_/g, "/"))); localStorage.setItem(ACK, JSON.stringify({ t: t, exp: j.exp * 1000 })); } catch (e) {} };
    var until = function (test, ms) { return new Promise(function (res) { var t0 = Date.now(); (function tick() { var v = test(); if (v || Date.now() - t0 > ms) res(v || null); else setTimeout(tick, 150); })(); }); };
    var script = function (src) { return new Promise(function (res, rej) { var el = document.createElement("script"); el.src = src; el.onload = res; el.onerror = rej; document.head.appendChild(el); }); };
    var ownAc = null;
    var acFresh = function () {
      if (location.hostname !== "harshvittori.github.io") return Promise.resolve(null);   // the reCAPTCHA key only works on the live site
      var ready = new Promise(function (res) { if (document.readyState !== "loading") res(); else document.addEventListener("DOMContentLoaded", function () { res(); }); });
      return ready.then(function () {
        if (SITE === "vault" || SITE === "reset")
          return until(function () { return window.HVCloud && window.HVCloud.appCheckOn && window.HVCloud; }, 10000).then(function (c) { return c ? c.appCheckToken() : null; });
        return until(function () { return window.HVScorecard; }, SITE === "test" ? 1500 : 0).then(function (sc) {
          if (sc) return sc.appCheckToken();
          if (window.firebase && !ownAc) return null;                                   // the page has its own Firebase: leave it alone
          if (!ownAc) ownAc = script(SDK + "firebase-app-compat.js").then(function () { return script(SDK + "firebase-app-check-compat.js"); }).then(function () {
            var app = window.firebase.apps.length ? window.firebase.app() : window.firebase.initializeApp({ apiKey: "AIzaSyDggasAVdqpvamkn1xeex2NmPUqG9JiZJ4", authDomain: "harsh-reset.firebaseapp.com", projectId: "harsh-reset", appId: "1:592094409539:web:57d3aa494464b867bbf5f6" });
            var ac = window.firebase.appCheck(app);
            ac.activate(new window.firebase.appCheck.ReCaptchaEnterpriseProvider("6LdZltEtAAAAANC5e-PJFqs2YrM1ubR3CKv0sOhl"), true);
            return ac;
          });
          return ownAc.then(function (ac) { return ac.getToken(false).then(function (r) { return r && r.token; }); });
        });
      }).then(function (t) { if (t) acSave(t); return t || null; }, function () { return null; });
    };
    var get = function (t) { return fetch(URL_, { cache: "no-store", headers: t ? { "X-Firebase-AppCheck": t } : {} }); };
    var fetchCfg = function () {
      return get(acSaved()).then(function (r) {
        if (r.status !== 401 && r.status !== 403) return r;
        try { localStorage.removeItem(ACK); } catch (e) {}
        return acFresh().then(function (t) { return t ? get(t) : r; });
      });
    };
    var load = function () {
      fetchCfg().then(function (r) { return r.ok ? r.json() : null; }).then(function (doc) {
        var s = doc && doc.fields && doc.fields.json && doc.fields.json.stringValue; if (!s) return;
        var c = JSON.parse(s); try { localStorage.setItem(KEY, s); } catch (e) {}
        cfg = c; window.HVStatus.loaded = true; apply(c);
      }).catch(function () {}).then(function () { if (!window.HVStatus.loaded) { window.HVStatus.loaded = true; try { window.dispatchEvent(new CustomEvent("hvstatus", { detail: cfg || {} })); } catch (e) {} } });
    };
    load();
    setInterval(function () { if (!document.hidden) load(); }, 60000);
    document.addEventListener("visibilitychange", function () { if (!document.hidden) load(); });
    // a scheduled start or end should happen on time even without a new fetch
    setInterval(function () { if (cfg) { var on = !!maint(cfg); if (on !== d.classList.contains("hvmaint") && !(admin && !preview)) apply(cfg); } }, 15000);
  } catch (e) {}
})();
