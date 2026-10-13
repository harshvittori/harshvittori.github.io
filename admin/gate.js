/* Page lock for the static admin pages (Brand, Guides, Rules, ...): sign in with Google, then the page opens only if the Team page gave you access to it.
   The owner always has access. Each page names its area in <script src="/admin/gate.js" data-area="pg_brand">. Added by tools/admin_nav.py. */
(function () {
  var me = document.currentScript, AREA = me && me.getAttribute("data-area"); if (!AREA) return;
  var root = document.documentElement; root.classList.add("hvg-wait");
  var st = document.createElement("style");
  st.textContent = "html.hvg-wait body>*:not(#hvgGate):not(.hvx){visibility:hidden}#hvgGate{position:fixed;inset:58px 0 0;z-index:800;display:flex;align-items:center;justify-content:center;padding:20px;background:#F6F7FB;font-family:Inter,system-ui,-apple-system,sans-serif}" +
    "#hvgGate .c{max-width:420px;width:100%;background:#fff;border:1px solid rgba(20,24,40,.08);border-radius:20px;padding:30px 26px;text-align:center;box-shadow:0 18px 40px -28px rgba(30,40,110,.45);color:#1B1D2A}#hvgGate h2{margin:0 0 8px;font-size:21px}#hvgGate p{margin:0 0 16px;color:#5A5F73;font-size:15px;line-height:1.5}" +
    "#hvgGate button{border:0;border-radius:999px;background:#A60F23;color:#fff;font-weight:600;font-size:15px;padding:11px 22px;cursor:pointer}#hvgGate button.g{background:#fff;color:#A60F23;border:1px solid rgba(20,24,40,.15);margin-left:8px}";
  document.head.appendChild(st);
  var box = null;
  function card(h, p, btns) {
    if (!box) { box = document.createElement("div"); box.id = "hvgGate"; document.body.appendChild(box); }
    box.innerHTML = '<div class="c"><h2></h2><p></p><div></div></div>'; box.querySelector("h2").textContent = h; box.querySelector("p").textContent = p;
    btns.forEach(function (b) { var e = document.createElement("button"); e.textContent = b[0]; if (b[2]) e.className = "g"; e.onclick = b[1]; box.querySelector("div div").appendChild(e); });
  }
  function load(src) { return new Promise(function (ok, no) { var s = document.createElement("script"); s.src = src; s.onload = ok; s.onerror = no; document.head.appendChild(s); }); }
  var CFG = { apiKey: "AIzaSyDggasAVdqpvamkn1xeex2NmPUqG9JiZJ4", authDomain: "harsh-reset.firebaseapp.com", projectId: "harsh-reset", appId: "1:592094409539:web:57d3aa494464b867bbf5f6" };
  var DOCS = "https://firestore.googleapis.com/v1/projects/harsh-reset/databases/(default)/documents";
  function start() {
    card("Checking access…", "One moment.", []);
    var G = "https://www.gstatic.com/firebasejs/10.12.2/";
    load(G + "firebase-app-compat.js").then(function () { return Promise.all([load(G + "firebase-auth-compat.js"), load(G + "firebase-app-check-compat.js"), load("/admin/access.js")]); }).then(async function () {
      firebase.initializeApp(CFG); var ap = null;
      if (/^(harshvittori\.github\.io|hvworld\.haritt\.com|haritt\.com)$/.test(location.hostname)) { try { ap = firebase.appCheck(); ap.activate(new firebase.appCheck.ReCaptchaEnterpriseProvider("6LdZltEtAAAAANC5e-PJFqs2YrM1ubR3CKv0sOhl"), true); } catch (e) { ap = null; } }
      var auth = firebase.auth();
      async function get(path) {
        var h = { Authorization: "Bearer " + (await auth.currentUser.getIdToken()) };
        if (ap) { try { var t = await ap.getToken(false); if (t && t.token) h["X-Firebase-AppCheck"] = t.token; } catch (e) {} }
        var r = await fetch(DOCS + path + "?key=" + CFG.apiKey, { headers: h, cache: "no-store" });
        if (!r.ok) { var e = new Error("HTTP " + r.status); e.status = r.status; throw e; }
        return r.json();
      }
      async function isPublic() {
        try {
          var h = {}; if (ap) { try { var t = await ap.getToken(false); if (t && t.token) h["X-Firebase-AppCheck"] = t.token; } catch (e) {} }
          var r = await fetch(DOCS + "/pagePublic/main?key=" + CFG.apiKey, { headers: h, cache: "no-store" }); if (!r.ok) return false;
          var d = await r.json(), j = JSON.parse((d.fields && d.fields.json && d.fields.json.stringValue) || "[]"); return j.indexOf(AREA) >= 0;
        } catch (e) { return false; }
      }
      if (await isPublic()) { root.classList.remove("hvg-wait"); if (box) { box.remove(); box = null; } return; }
      auth.onAuthStateChanged(async function (u) {
        if (!u) { card("Sign in to open this page", "Use your Google account. Access is given by the founder on the Team page.", [["Sign in with Google", async function () { try { await auth.signInWithPopup(new firebase.auth.GoogleAuthProvider()); } catch (e) {} }]]); return; }
        var acc = null, err = false;
        try { acc = await HVAccess.load(u, get); } catch (e) { err = true; }
        if (acc && acc.lv(AREA) > 0) { root.classList.remove("hvg-wait"); if (box) { box.remove(); box = null; } return; }
        card(err ? "Couldn't check access" : "No access to this page", err ? "Check your connection and reload." : (u.email || "This account") + " isn't allowed here. Ask the founder to give you access on the Team page.", [["Switch account", function () { auth.signOut(); }, 1]]);
      });
    }).catch(function () { card("Couldn't load", "Check your connection and reload.", [["Reload", function () { location.reload(); }]]); });
  }
  if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);
})();
