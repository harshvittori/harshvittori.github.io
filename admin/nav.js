/* One navigation bar for every admin page: the same groups, the same place, the current page marked.
   Desktop: a menu per group. Phone: one Menu button with everything. Added to each page by tools/admin_nav.py. */
(function () {
  if (window.__hvxNav) return; window.__hvxNav = 1;
  var I = {
    home: '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
    chart: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    flask: '<path d="M9 3h6M10 3v6L4.5 18.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3"/><path d="M7.5 15h9"/>',
    check: '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 10"/>',
    inbox: '<path d="M3 13l3-8h12l3 8v6H3z"/><path d="M3 13h5l1.5 2.5h5L16 13h5"/>',
    server: '<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01"/>',
    palette: '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 1.6-.9 1.6-1.8 0-1.3-1-1.6-1-2.7 0-.9.7-1.5 1.6-1.5H17a4 4 0 0 0 4-4c0-4.4-4-8-9-8z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10.5" cy="7" r="1.2"/><circle cx="15.5" cy="7.5" r="1.2"/>',
    image: '<rect x="3" y="4" width="18" height="16" rx="2.5"/><circle cx="8.5" cy="9.5" r="1.8"/><path d="M21 16l-5-5-9 9"/>',
    layers: '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    at: '<circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8"/>',
    rocket: '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M9 11a14 14 0 0 1 11-8 14 14 0 0 1-8 11l-3 1-1-1z"/><circle cx="15" cy="9" r="1.5"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>',
    spark: '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.7 1.8 1.8.7-1.8.7L19 20l-.7-1.8-1.8-.7 1.8-.7z"/>',
    key: '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M14 9l2 2"/>',
    shield: '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    clock: '<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v4h4"/><path d="M12 7v5l3 2"/>',
    users: '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2c2.9.3 5.5 2.6 5.5 5.8"/>'
  };
  var G = [
    ["Control centre", [["/admin/", "Control centre", "Websites, maintenance, announcements", "home"]]],
    ["Apps", [["/admin/analytics/", "Analytics", "Visits and actions in every product", "chart"], ["/admin/beta/", "HV Reset Beta", "Reports, ideas, testers, emails", "flask"], ["/hv-tests/admin/", "HV Test", "Numbers and scorecards", "check"]]],
    ["Haritt Developers", [["/admin/enquiries/", "Enquiries", "Start a project form messages", "inbox"], ["/admin/infrastructure/", "Infrastructure", "Which platform runs what", "server"]]],
    ["Brand", [["/admin/brand/", "Brand assets", "Logos, colours, fonts, tokens", "palette"], ["/admin/media/", "Covers & thumbnails", "Every cover in 1920×1080", "image"], ["/admin/designs/", "Design decisions", "Chosen vs not chosen", "layers"], ["/admin/social/", "Social accounts", "Every handle and email", "at"], ["/admin/logins/", "Social Media Accounts", "Logins, passwords encrypted", "key"]]],
    ["Guides", [["/admin/launch/", "Launch guide", "Domain to email, step by step", "rocket"], ["/admin/setup/", "haritt.com setup", "Domain, DNS, hosting, email", "globe"], ["/admin/programs/", "Claude programs", "Startups and Open Source", "spark"], ["/admin/rules/", "Rules & scripts", "Firestore rules and email scripts", "shield"], ["/admin/changelog/", "Changelog", "What changed each day", "clock"]]],
    ["Team", [["/admin/team/", "Team & access", "Give people access by email", "users"]]]
  ];
  var path = location.pathname.replace(/index\.html$/, "").replace(/^\/w\//, "/");
  var alias = { "/admin/oss/": "/admin/programs/", "/admin/startups/": "/admin/programs/" };
  var cur = alias[path] || path, best = "";
  G.forEach(function (g) { g[1].forEach(function (l) { if (cur.indexOf(l[0]) === 0 && l[0].length > best.length) best = l[0]; }); });
  if (best === "/admin/" && cur !== "/admin/") best = "";
  var svg = function (k) { return '<svg viewBox="0 0 24 24" aria-hidden="true">' + I[k] + '</svg>'; };
  var item = function (l) { return '<a class="hvx-i' + (l[0] === best ? ' on' : '') + '" href="' + l[0] + '"' + (l[0] === best ? ' aria-current="page"' : '') + '><span class="hvx-ic">' + svg(l[3]) + '</span><span><b>' + l[1] + '</b><small>' + l[2] + '</small></span></a>'; };
  var css = '.hvx{position:sticky;top:0;z-index:900;background:rgba(251,250,247,.9);-webkit-backdrop-filter:saturate(1.4) blur(16px);backdrop-filter:saturate(1.4) blur(16px);border-bottom:1px solid rgba(20,24,40,.08);font-family:Inter,"Segoe UI",system-ui,sans-serif;color:#16182A}' +
    '.hvx-w{max-width:1240px;margin:0 auto;padding:0 20px;height:58px;display:flex;align-items:center;gap:6px}' +
    '.hvx-b{display:flex;align-items:center;gap:10px;text-decoration:none;color:inherit;font-weight:700;font-size:16px;margin-right:14px;white-space:nowrap}.hvx-b img{width:30px;height:30px;border-radius:50%;object-fit:cover}.hvx-b small{font-size:11px;font-weight:700;letter-spacing:.12em;color:#A70D22;background:#F7E8EA;border-radius:99px;padding:3px 8px}' +
    '.hvx-g{position:relative}.hvx-t{border:0;background:none;font:inherit;font-size:14px;font-weight:600;color:#3B3F55;padding:8px 12px;border-radius:10px;cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap;text-decoration:none}' +
    '.hvx-t:hover,.hvx-g.open .hvx-t{background:#F1EEE8;color:#16182A}.hvx-t.on{color:#A70D22;background:#F7E8EA}.hvx-t .car{font-size:10px;opacity:.6}' +
    '.hvx-p{position:absolute;top:calc(100% + 8px);left:0;min-width:300px;background:#fff;border:1px solid rgba(20,24,40,.08);border-radius:16px;box-shadow:0 24px 60px -18px rgba(20,24,60,.35);padding:8px;display:none}.hvx-g.open .hvx-p{display:block}' +
    '.hvx-i{display:flex;gap:12px;align-items:center;padding:10px;border-radius:12px;text-decoration:none;color:inherit}.hvx-i:hover{background:#F6F3EE}.hvx-i.on{background:#F7E8EA}' +
    '.hvx-i b{display:block;font-size:14px;font-weight:600}.hvx-i small{display:block;font-size:12.5px;color:#6B6F85;margin-top:1px}' +
    '.hvx-ic{flex:none;width:34px;height:34px;border-radius:10px;background:#F7E8EA;display:grid;place-items:center}.hvx-ic svg{width:18px;height:18px;fill:none;stroke:#A70D22;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}' +
    '.hvx-me{display:flex;align-items:center;gap:10px;margin-left:8px;font-size:13.5px;color:#55586B;white-space:nowrap}.hvx-me[hidden]{display:none}.hvx-me img{width:30px;height:30px;border-radius:50%;object-fit:cover}.hvx-me span{max-width:220px;overflow:hidden;text-overflow:ellipsis}.hvx-me .btn{padding:6px 12px;font-size:13px}' +
    '@media(max-width:1180px){.hvx-me span{display:none}}' +
    '.hvx-dk{flex:none;width:36px;height:36px;margin-left:6px;border:1px solid rgba(20,24,40,.12);border-radius:10px;background:#fff;cursor:pointer;display:grid;place-items:center}.hvx-dk svg{width:18px;height:18px;fill:none;stroke:#3B3F55;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}' +
    '.hvx-sp{flex:1}.hvx-m{display:none;border:1px solid rgba(20,24,40,.12);background:#fff;border-radius:10px;padding:8px 12px;font:inherit;font-size:14px;font-weight:600;color:#16182A;cursor:pointer}' +
    '.hvx-sh{position:fixed;inset:58px 0 0;font-family:Inter,"Segoe UI",system-ui,sans-serif;color:#16182A;background:#F7F6F2;overflow:auto;padding:12px 16px 40px;display:none;z-index:899}body.hvx-mopen .hvx-sh{display:block}body.hvx-mopen{overflow:hidden}' +
    '.hvx-sh h4{margin:18px 6px 6px;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:#8A8EA3}' +
    '@media(max-width:1020px){.hvx-d{display:none}.hvx-m{display:block}}' +
    /* phones: only the logo, the theme switch, your photo and Menu fit; Sign out moves into the Menu */
    '@media(max-width:640px){.hvx-w{padding:0 12px;gap:6px}.hvx-bn{display:none}.hvx-b{margin-right:auto;gap:8px}.hvx-me{margin-left:2px}.hvx-me .btn{display:none}.hvx-dk{margin-left:0}.hvx{overflow:hidden}}' +
    '.hvx-so{display:none;width:100%;margin-top:22px;padding:12px;border-radius:12px;border:1px solid rgba(20,24,40,.12);background:#fff;font:inherit;font-weight:600;color:#A70D22;cursor:pointer}@media(max-width:640px){body.hvx-signed .hvx-so{display:block}}' +
    /* the pages' own old bars: their links now live here */
    'body.hvx-on header.nav,body.hvx-on header.anav{display:none!important}body.hvx-on .top:has(.brand) .brand,body.hvx-on .top:has(.brand)>.wrap>a{display:none!important}' +
    'body.hvx-on .top:has(.brand)>.wrap{justify-content:flex-end}' +
    /* Haritt Group look for the whole admin: Haritt red as the accent */
    ':root{--accent:#A70D22!important;--accent2:#860A1B!important}.apage .ai{background:#F7E8EA!important}';
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
  var desk = G.map(function (g, i) {
    var on = g[1].some(function (l) { return l[0] === best; });
    if (g[1].length === 1) return '<div class="hvx-g hvx-d"><a class="hvx-t' + (on ? ' on' : '') + '" href="' + g[1][0][0] + '">' + g[0] + '</a></div>';
    return '<div class="hvx-g hvx-d" data-g="' + i + '"><button class="hvx-t' + (on ? ' on' : '') + '" type="button" aria-expanded="false">' + g[0] + '<span class="car">&#9662;</span></button><div class="hvx-p">' + g[1].map(item).join("") + '</div></div>';
  }).join("");
  var sheet = G.map(function (g) { return '<h4>' + g[0] + '</h4>' + g[1].map(item).join(""); }).join("");
  var n = document.createElement("nav"); n.className = "hvx"; n.setAttribute("aria-label", "Admin");
  n.innerHTML = '<div class="hvx-w"><a class="hvx-b" href="/admin/"><img src="/admin/haritt-logo.png" alt=""><span class="hvx-bn">Haritt Group</span> <small>ADMIN</small></a>' + desk + '<span class="hvx-sp"></span><button class="hvx-dk" type="button" aria-label="Dark mode" title="Dark mode"></button><button class="hvx-m" type="button" aria-expanded="false">Menu</button></div>';
  var sh = document.createElement("div"); sh.className = "hvx-sh"; sh.innerHTML = sheet;   /* outside the bar: the bar's blur would trap a fixed panel inside it */
  var put = function () { document.body.insertBefore(n, document.body.firstChild); document.body.appendChild(sh);
    /* the signed-in person and Sign out move up into this bar, so there is no second strip under it */
    var me = document.getElementById("me"), top = me && me.closest(".top");
    var so = document.getElementById("signOut");
    if (so) { var b2 = document.createElement("button"); b2.type = "button"; b2.className = "hvx-so"; b2.textContent = "Sign out"; b2.onclick = function () { document.body.classList.remove("hvx-mopen"); so.click(); }; sh.appendChild(b2);
      new MutationObserver(function () { document.body.classList.toggle("hvx-signed", !!me && !me.hidden); }).observe(me || document.body, { attributes: true }); document.body.classList.toggle("hvx-signed", !!me && !me.hidden); }
    if (me) { n.querySelector(".hvx-w").insertBefore(me, n.querySelector(".hvx-m")); me.classList.add("hvx-me"); if (top && !top.querySelector("button,input,select")) top.style.display = "none"; } document.body.classList.add("hvx-on"); };
  if (document.body) put(); else document.addEventListener("DOMContentLoaded", put);
  var MOON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>', SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  var dk = n.querySelector(".hvx-dk"), paint = function () { var on = document.documentElement.classList.contains("adm-dark"); dk.innerHTML = on ? SUN : MOON; dk.setAttribute("aria-pressed", String(on)); dk.title = on ? "Light mode" : "Dark mode"; };
  paint();
  dk.addEventListener("click", function () { var on = document.documentElement.classList.toggle("adm-dark"); try { localStorage.setItem("hv-adm-theme", on ? "dark" : "light"); } catch (e) {} paint(); });
  n.addEventListener("click", function (e) {
    var t = e.target.closest(".hvx-g[data-g] > .hvx-t");
    if (t) { var g = t.parentNode, was = g.classList.contains("open"); n.querySelectorAll(".hvx-g.open").forEach(function (x) { x.classList.remove("open"); x.firstChild.setAttribute("aria-expanded", "false"); }); if (!was) { g.classList.add("open"); t.setAttribute("aria-expanded", "true"); } return; }
    if (e.target.closest(".hvx-m")) { var o = document.body.classList.toggle("hvx-mopen"); n.querySelector(".hvx-m").setAttribute("aria-expanded", String(o)); n.querySelector(".hvx-m").textContent = o ? "Close" : "Menu"; }
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".hvx")) n.querySelectorAll(".hvx-g.open").forEach(function (x) { x.classList.remove("open"); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { n.querySelectorAll(".hvx-g.open").forEach(function (x) { x.classList.remove("open"); }); document.body.classList.remove("hvx-mopen"); } });
})();
