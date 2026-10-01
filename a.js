/* HV analytics: first-party, aggregate-only usage counts for HV World, HV Test, HV Reset and HV Vault.
   Loaded by /status.js on every page. No cookies, no third-party services, no user IDs, names, emails or content
   are ever sent: each event only adds +1 to a counter in a daily/weekly/monthly document (Firestore "analytics",
   readable only by the admin). Device-level state (first-seen day, last active day, first-touch channel) stays in
   this browser's localStorage. Respects Do Not Track, Global Privacy Control and the opt-out on /privacy/.
   API (also works before this file loads, via the stub in status.js):
     hva("event", "test_start")            count an event (+ unique devices doing it today)
     hva("page")                           count a page view (automatic, incl. SPA navigation)
   Everything is wrapped so analytics can never break a page. Docs: hv-vault-web/docs/analytics/ */
(function () {
  "use strict";
  var W = window;
  if (W.__hvaLoaded) return; W.__hvaLoaded = true;
  var stubQ = (W.hva && W.hva.q) || [];
  var noop = function () {}; W.hva = noop;
  try {
    var LS = W.localStorage, SS = W.sessionStorage, p = location.pathname, qs = location.search;
    var DEBUG = /[?&]hvadebug=1\b/.test(qs);
    var P = /^\/hv-tests(\/|$)/.test(p) ? "test" : /^\/(hv-reset|harsh-reset)(\/|$)/.test(p) ? "reset" : /^\/hv-vault-web(\/|$)/.test(p) ? "vault" : "world";
    if (/^\/admin(\/|$)/.test(p)) return;
    // opt-out / opt-in links on /privacy/ (?hvoptout=1, ?hvoptin=1)
    try { if (/[?&]hvoptout=1\b/.test(qs)) LS.setItem("hvnoa", "1"); if (/[?&]hvoptin=1\b/.test(qs)) LS.removeItem("hvnoa"); } catch (e) {}
    var off = false;
    try { off = LS.getItem("hvnoa") === "1" || (LS.getItem("hvadmin") === "1" && !DEBUG); } catch (e) {}
    if (navigator.doNotTrack === "1" || W.doNotTrack === "1" || navigator.globalPrivacyControl === true) off = true;
    if (location.hostname !== "harshvittori.github.io" && !DEBUG && !W.__HVA_TEST) off = true;   // never count local copies
    if (off) { W.hva = noop; return; }

    var ENDPOINT = "https://firestore.googleapis.com/v1/projects/harsh-reset/databases/(default)/documents";
    var KEY = "AIzaSyDggasAVdqpvamkn1xeex2NmPUqG9JiZJ4";             // public web key (same as the apps)
    var DOCROOT = "projects/harsh-reset/databases/(default)/documents/analytics/";
    var CONV = { signup: 1, sign_in: 1, activation: 1, test_start: 1, test_complete: 1, scorecard: 1, open_app: 1, open_test: 1, open_reset: 1, open_vault: 1 };
    var slug = function (s, n) { return String(s || "").toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "").slice(0, n || 40) || "none"; };
    var ist = function (d) { return (d || new Date()).toLocaleDateString("en-CA", { timeZone: "Asia/Kolkata" }); };   // YYYY-MM-DD in India time
    var DAY = ist();
    var dayNum = function (s) { var a = s.split("-"); return Date.UTC(+a[0], +a[1] - 1, +a[2]) / 864e5; };
    var isoWeek = function (s) {
      var a = s.split("-"), d = new Date(Date.UTC(+a[0], +a[1] - 1, +a[2])), wd = d.getUTCDay() || 7;
      d.setUTCDate(d.getUTCDate() + 4 - wd); var y = d.getUTCFullYear(), w = Math.ceil(((d - Date.UTC(y, 0, 1)) / 864e5 + 1) / 7);
      return y + "-W" + (w < 10 ? "0" : "") + w;
    };
    var WEEK = isoWeek(DAY), MONTH = DAY.slice(0, 7);
    var did = function (kind, id) { return P + "_" + kind + "_" + id; };

    /* ---------- batched +1 writes ---------- */
    var Q = {}, timer = null, sent = 0;
    var inc = function (doc, field, n) { if (!field) return; (Q[doc] = Q[doc] || {})[field] = ((Q[doc] || {})[field] || 0) + (n || 1); schedule(); };
    var d = function (f, n) { inc(did("d", DAY), f, n); };
    var schedule = function () { if (!timer) timer = setTimeout(flush, 2500); };
    var flush = function (beacon) {
      clearTimeout(timer); timer = null;
      var docs = Object.keys(Q); if (!docs.length) return;
      if (sent > 300) { Q = {}; return; }                               // hard cap per page load
      var writes = docs.map(function (doc) {
        var f = Q[doc];
        return { transform: { document: DOCROOT + doc, fieldTransforms: Object.keys(f).slice(0, 40).map(function (k) { return { fieldPath: k, increment: { integerValue: String(f[k]) } }; }) } };
      });
      var body = JSON.stringify({ writes: writes }); sent += docs.length; Q = {};
      if (DEBUG) console.log("[hva]", P, JSON.parse(body));
      try { fetch(ENDPOINT + ":commit?key=" + KEY, { method: "POST", headers: { "Content-Type": "application/json" }, body: body, keepalive: !!beacon }).catch(noop); } catch (e) {}
    };
    addEventListener("pagehide", function () { tick(); flush(true); });
    document.addEventListener("visibilitychange", function () { if (document.hidden) { tick(); flush(true); } else lastVis = Date.now(); });

    /* ---------- device + session ---------- */
    var dev = {}; try { dev = JSON.parse(LS.getItem("hva:" + P) || "{}") || {}; } catch (e) {}
    var saveDev = function () { try { LS.setItem("hva:" + P, JSON.stringify(dev)); } catch (e) {} };
    var ses = null; try { ses = JSON.parse(SS.getItem("hva:s:" + P) || "null"); } catch (e) {}
    var now = Date.now();
    var params = {}; qs.replace(/^\?/, "").split("&").forEach(function (kv) { var i = kv.indexOf("="); if (i > 0) { try { params[decodeURIComponent(kv.slice(0, i)).toLowerCase()] = decodeURIComponent(kv.slice(i + 1).replace(/\+/g, " ")); } catch (e) {} } });
    var channel = function () {
      var s = slug(params.utm_source, 24), m = slug(params.utm_medium, 24);
      if (params.utm_source || params.utm_medium) {
        if (/^(linkedin|lnkd)/.test(s)) return "linkedin"; if (/^(instagram|ig)$/.test(s)) return "instagram"; if (/^(youtube|yt)$/.test(s)) return "youtube";
        if (/^(whatsapp|wa)$/.test(s)) return "whatsapp"; if (/^(facebook|fb)$/.test(s)) return "facebook"; if (/^(twitter|x)$/.test(s)) return "x";
        if (m === "email" || s === "email" || s === "newsletter") return "email"; if (m === "community" || m === "group") return "community";
        if (m === "share" || s === "scorecard") return "shared";
        if (s === "qr" || m === "offline") return "qr";
        if (m === "referral" || m === "friend") return "referral"; if (m === "cpc" || m === "paid" || m === "ads") return "paid";
        return "campaign_other";
      }
      var r = document.referrer, h = ""; try { h = r ? new URL(r).hostname.replace(/^www\./, "") : ""; } catch (e) {}
      if (!h) return "direct";
      if (h === location.hostname) {
        var rp = ""; try { rp = new URL(r).pathname; } catch (e) {}
        var rP = /^\/hv-tests/.test(rp) ? "test" : /^\/(hv-reset|harsh-reset)/.test(rp) ? "reset" : /^\/hv-vault-web/.test(rp) ? "vault" : "world";
        return rP === P ? "internal" : "from_" + rP;                   // e.g. from_world = discovered through HV World
      }
      if (/linkedin\.com$|lnkd\.in$/.test(h)) return "linkedin"; if (/instagram\.com$/.test(h)) return "instagram";
      if (/youtube\.com$|youtu\.be$/.test(h)) return "youtube"; if (/facebook\.com$|fb\.com$/.test(h)) return "facebook";
      if (/(^|\.)t\.co$|twitter\.com$|x\.com$/.test(h)) return "x"; if (/whatsapp\.com$|wa\.me$/.test(h)) return "whatsapp";
      if (/google\.|bing\.com$|duckduckgo\.com$|yahoo\.|yandex\.|ecosia\.org$|search\.brave\.com$/.test(h)) return "search";
      if (/chatgpt\.com$|openai\.com$|perplexity\.ai$|gemini\.google\.com$|claude\.ai$|copilot\.microsoft\.com$/.test(h)) return "ai_assistant";
      if (/github\.com$/.test(h)) return "github";
      return "referral";
    };
    var newSession = !ses || now - (ses.last || 0) > 30 * 60 * 1000;
    if (newSession) {
      var ch = channel();
      if (ch === "internal" && dev.lt) ch = dev.lt;                     // carry the last real channel through internal hops
      ses = { start: now, last: now, pv: 0, eng: 0, sec: 0, ch: ch };
      var ua = navigator.userAgent || "", mob = /Mobi|Android.+Mobile|iPhone/.test(ua), tab = /iPad|Tablet|Android(?!.*Mobile)/.test(ua);
      var br = /Edg\//.test(ua) ? "edge" : /OPR\/|Opera/.test(ua) ? "opera" : /SamsungBrowser/.test(ua) ? "samsung" : /Firefox\//.test(ua) ? "firefox" : /Chrome\//.test(ua) ? "chrome" : /Safari\//.test(ua) ? "safari" : "other";
      var os = /Android/.test(ua) ? "android" : /iPhone|iPad|iPod/.test(ua) ? "ios" : /Windows/.test(ua) ? "windows" : /Mac OS X/.test(ua) ? "macos" : /Linux/.test(ua) ? "linux" : "other";
      var tz = ""; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) {}
      var geo = /Kolkata|Calcutta/.test(tz) ? "india" : /^America\//.test(tz) ? "americas" : /^Europe\//.test(tz) ? "europe" : /^Asia\//.test(tz) ? "asia_other" : /^(Africa|Australia|Pacific)\//.test(tz) ? "rest" : "unknown";
      d("ss"); d("ch_" + ch); d("dev_" + (mob ? "mobile" : tab ? "tablet" : "desktop")); d("br_" + br); d("os_" + os); d("geo_" + geo);
      if (params.utm_campaign) d("cmp_" + slug(params.utm_campaign, 32));
      if (params.utm_content) d("cnt_" + slug(params.utm_content, 32));
      if (ch !== "internal") dev.lt = ch;
      // first visit ever on this device for this product
      if (!dev.fs) {
        dev.fs = DAY; dev.ft = ch; d("nu"); d("ft_" + ch); inc(did("c", DAY), "n");
      }
      dev.n = (dev.n || 0) + 1;
    }
    ses.last = now;
    // first activity of the day / week / month on this device
    if (dev.ld !== DAY) {
      if (dev.ld) {
        d("ru");                                                     // returning device today
        var gap = dayNum(DAY) - dayNum(dev.fs || DAY);
        if (gap === 1 || gap === 7 || gap === 14 || gap === 30) inc(did("c", dev.fs), "d" + gap);
        if (gap >= 1 && gap <= 7 && !(dev.r7)) { inc(did("c", dev.fs), "r7"); dev.r7 = 1; }
        if (gap >= 8 && gap <= 30 && !(dev.r30)) { inc(did("c", dev.fs), "r30"); dev.r30 = 1; }
      }
      d("uv"); dev.ld = DAY; dev.ev = {};
    }
    if (dev.lw !== WEEK) { inc(did("w", WEEK), "wau"); dev.lw = WEEK; }
    if (dev.lm !== MONTH) { inc(did("m", MONTH), "mau"); dev.lm = MONTH; }
    var saveSes = function () { try { SS.setItem("hva:s:" + P, JSON.stringify(ses)); } catch (e) {} };
    saveDev(); saveSes();

    /* ---------- engagement time (visible time only) ---------- */
    var lastVis = Date.now(), engagedSent = !!ses.eng;
    var tick = function () {
      if (!document.hidden) { var dt = Math.min(60, Math.round((Date.now() - lastVis) / 1000)); if (dt > 0) { d("sec", dt); ses.sec += dt; } lastVis = Date.now(); }
      if (!engagedSent && (ses.sec >= 10 || ses.pv >= 2)) { engagedSent = true; ses.eng = 1; d("es"); }
      ses.last = Date.now(); saveSes();
    };
    setInterval(function () { if (!document.hidden) tick(); }, 15000);

    /* ---------- page views (incl. single-page navigation) ---------- */
    var lastPath = null, depth = 0;
    var pageSlug = function () {
      var x = location.pathname.replace(/^\/(hv-tests|hv-reset|harsh-reset|hv-vault-web)(\/|$)/, "/").replace(/index\.html$/, "");
      x = x.replace(/\/tests\/([^/]+)\/?.*/, "/test_$1");
      return slug(x === "/" ? "home" : x, 40);
    };
    var page = function (name) {
      var path = name ? "v:" + name : location.pathname;
      if (path === lastPath) return; lastPath = path; depth = 0;
      d("pv"); d("pg_" + (name ? slug(name, 30) : pageSlug())); ses.pv++; saveSes(); tick();
    };
    var hook = function (fn) { var o = history[fn]; history[fn] = function () { var r = o.apply(this, arguments); setTimeout(function () { try { page(); } catch (e) {} }, 60); return r; }; };
    hook("pushState"); hook("replaceState"); addEventListener("popstate", function () { setTimeout(function () { try { page(); } catch (e) {} }, 60); });
    page();

    /* ---------- events ---------- */
    var event = function (name, opt) {
      name = slug(name, 32); opt = opt || {};
      dev.ev = dev.ev || {};
      d("ev_" + name);
      if (!dev.ev[name]) { dev.ev[name] = 1; d("ue_" + name); }        // unique devices doing this today (for funnels)
      if (opt.first && !(dev.fe || {})[name]) { dev.fe = dev.fe || {}; dev.fe[name] = 1; d("fe_" + name); }   // first time ever on this device
      if (CONV[name]) { d("cv_" + name + "_" + slug(ses.ch, 20)); d("cf_" + name + "_" + slug(dev.ft || ses.ch, 20)); }
      if (!engagedSent) { engagedSent = true; ses.eng = 1; d("es"); }
      saveDev(); saveSes();
    };
    W.hva = function (type, a, b) { try { if (type === "event") event(a, b); else if (type === "page") page(a); } catch (e) {} };

    /* ---------- automatic: errors, outbound and app links, scroll depth (HV World) ---------- */
    var errs = 0;
    var onErr = function () { if (errs++ < 5) d("err"); };
    addEventListener("error", function (e) { if (e && e.message) onErr(); });
    addEventListener("unhandledrejection", onErr);
    document.addEventListener("click", function (e) {
      try {
        var t = e.target && e.target.closest && e.target.closest("a[href],[data-hva]"); if (!t) return;
        if (t.getAttribute("data-hva")) { event(t.getAttribute("data-hva")); return; }
        var u = new URL(t.href, location.href);
        if (u.hostname === location.hostname) {
          var m = /^\/(hv-tests|hv-reset|harsh-reset|hv-vault-web)(\/|$)/.exec(u.pathname);
          if (m && P === "world") { var to = m[1] === "hv-tests" ? "test" : m[1] === "hv-vault-web" ? "vault" : "reset"; event("open_" + to); event("open_app"); }
        } else if (/^https?:$/.test(u.protocol)) event("out_" + slug(u.hostname.replace(/^www\./, "").split(".").slice(-2, -1)[0], 20));
      } catch (x) {}
    }, true);
    if (P === "world") {
      var seen = {};
      addEventListener("scroll", function () {
        var h = document.documentElement, max = h.scrollHeight - innerHeight; if (max < 200) return;
        var pct = (scrollY / max) * 100;
        [50, 90].forEach(function (s) { var k = lastPath + s; if (pct >= s && !seen[k]) { seen[k] = 1; d("sd" + s); } });
      }, { passive: true });
      // product card / app link impressions (once per page view)
      if ("IntersectionObserver" in W) {
        var io = new IntersectionObserver(function (es) {
          es.forEach(function (en) {
            if (!en.isIntersecting) return; var a = en.target, m = /\/(hv-tests|hv-reset|harsh-reset|hv-vault-web)(\/|$)/.exec(a.getAttribute("href") || "");
            if (!m) return; var k = lastPath + m[1]; if (seen[k]) return; seen[k] = 1;
            d("imp_" + (m[1] === "hv-tests" ? "test" : m[1] === "hv-vault-web" ? "vault" : "reset"));
          });
        }, { threshold: .6 });
        var scan = function () { document.querySelectorAll('a[href*="/hv-tests/"],a[href*="/hv-reset/"],a[href*="/hv-vault-web/"]').forEach(function (a) { if (!a.__hvaIO) { a.__hvaIO = 1; io.observe(a); } }); };
        if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", scan); else scan();
        setInterval(scan, 3000);
      }
    }
    stubQ.forEach(function (args) { W.hva.apply(null, args); });
  } catch (e) { W.hva = noop; }
})();
