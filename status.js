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
    var CSS = ':host{all:initial}*{box-sizing:border-box;margin:0}' +
      '.w{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;padding:24px;font-family:Sora,Inter,system-ui,-apple-system,"Segoe UI",sans-serif;color:#0B0D1A;text-align:center;' +
      'background:radial-gradient(60% 55% at 18% 25%,#AEB8F5 0,transparent 70%),radial-gradient(55% 55% at 85% 80%,#CDB9F4 0,transparent 70%),radial-gradient(45% 40% at 60% 10%,#fff 0,transparent 70%),#E6E8F6}' +
      '.g{max-width:560px;width:100%;padding:40px 28px 34px;border-radius:28px;background:rgba(255,255,255,.58);-webkit-backdrop-filter:blur(22px) saturate(1.6);backdrop-filter:blur(22px) saturate(1.6);border:1px solid rgba(255,255,255,.9);box-shadow:0 30px 70px -30px rgba(46,67,166,.45),inset 0 1px 0 #fff}' +
      '.n{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#8A5A00;background:#FFF3D6;border:1px solid #F5DDA6;padding:7px 13px;border-radius:999px}.n i{width:7px;height:7px;border-radius:50%;background:#E0A21A}' +
      'h1{font-size:clamp(24px,5vw,34px);font-weight:700;letter-spacing:-.03em;margin:18px 0 0;line-height:1.15}' +
      '.m{font-size:16px;line-height:1.5;color:#474C68;margin:12px auto 0;max-width:440px;white-space:pre-line}' +
      '.k{font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#4B55A8;margin:24px 0 0}' +
      '.c{font-size:clamp(34px,8vw,52px);font-weight:700;letter-spacing:-.04em;font-variant-numeric:tabular-nums;line-height:1.1;margin:4px 0 0}' +
      '.d{font-size:14px;color:#555B7A;margin:6px 0 0}' +
      'a{display:inline-flex;margin-top:24px;font-size:15px;font-weight:600;color:#fff;background:#2E43A6;text-decoration:none;padding:12px 20px;border-radius:999px}' +
      '.pv{position:fixed;top:14px;left:50%;transform:translateX(-50%);font-size:12px;font-weight:600;color:#fff;background:#1D1D1F;padding:6px 12px;border-radius:999px}';
    var showMaint = function (m) {
      if (!document.body) { document.addEventListener("DOMContentLoaded", function () { showMaint(m); }); return; }
      d.classList.add("hvmaint");
      if (!stopper) { stopper = true; ["pointerdown", "mousedown", "click", "touchstart", "keydown", "keyup"].forEach(function (t) { window.addEventListener(t, block, true); }); }
      if (!host) { host = document.createElement("div"); host.id = "hvMaint"; host.setAttribute("role", "dialog"); host.setAttribute("aria-live", "polite"); (host.attachShadow ? host.attachShadow({ mode: "open" }) : host); document.body.appendChild(host); }
      var root = host.shadowRoot || host, until = num(m.until);
      var msg = m.message || "We're making a few improvements. Please check back soon.";
      var home = SITE === "world" ? "" : '<a href="/">Visit HV World</a>';
      root.innerHTML = '<style>' + CSS + '</style><div class="w">' + (preview ? '<span class="pv">Preview: this is what visitors see</span>' : '') + '<div class="g"><span class="n"><i></i>Maintenance</span><h1>' + esc(NAMES[SITE]) + ' will be right back.</h1><p class="m">' + esc(msg) + '</p>' +
        (until ? '<p class="k">Back in</p><p class="c" role="timer"></p><p class="d">' + esc(new Date(until).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })) + '</p>' : '') + home + '</div></div>';
      clearTimeout(tickT);
      if (until) { var c = root.querySelector(".c"); var tick = function () { var ms = until - Date.now(); if (ms <= 0) { if (!preview) location.reload(); return; } c.textContent = left(ms); tickT = setTimeout(tick, 1000 - Date.now() % 1000 + 5); }; tick(); }
    };
    var hideMaint = function () { d.classList.remove("hvmaint"); clearTimeout(tickT); if (host) { host.remove(); host = null; } };
    var st = document.createElement("style");
    st.textContent = "html.hvmaint,html.hvmaint body{overflow:hidden!important}html.hvmaint body>*:not(#hvMaint){visibility:hidden!important}html.hvmaint body>#hvMaint#hvMaint{position:fixed!important;inset:0!important;z-index:2147483647!important;display:block!important;visibility:visible!important}" +
      "#hvAdminPill{position:fixed;left:12px;bottom:12px;z-index:2147483646;font:600 12px/1 system-ui,sans-serif;color:#8A5A00;background:#FFF3D6;border:1px solid #F5DDA6;padding:8px 11px;border-radius:999px;box-shadow:0 8px 20px -10px rgba(0,0,0,.3)}";
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

    var apply = function (c) {
      window.HVStatus.cfg = c || {};
      var m = maint(c);
      if (m && !(admin && !preview)) showMaint(m); else hideMaint();
      var pill = document.getElementById("hvAdminPill");
      if (m && admin && !preview) { if (!pill && document.body) { pill = document.createElement("div"); pill.id = "hvAdminPill"; pill.textContent = "Maintenance is on · you see the site as admin"; document.body.appendChild(pill); } }
      else if (pill) pill.remove();
      banner(c);
      try { window.dispatchEvent(new CustomEvent("hvstatus", { detail: c || {} })); } catch (e) {}
    };
    if (cfg) apply(cfg);
    var load = function () {
      fetch(URL_, { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (doc) {
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
