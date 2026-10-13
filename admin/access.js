/* Who you are in the HV World admin: the owner (everything), or a team member with access per area.
   The Firestore rules enforce it; this only decides what each page shows. Levels: 0 none, 1 view, 2 edit. */
(function () {
  var OWNER = "vbqJe9D5IAYSBytSzM850motekm2";
  var AREAS = [
    ["Control centre", [["site", "Websites, banner and home page", 2]]],
    ["Analytics", [["an_reset", "HV Reset", 1], ["an_vault", "HV Vault", 1], ["an_test", "HV Test", 1], ["an_world", "HV World site", 1]]],
    ["HV Reset Beta", [["b_reports", "Reports", 2], ["b_ideas", "Ideas & roadmap", 2], ["b_testers", "Testers (names, emails)", 2], ["b_survey", "Survey & polls", 2], ["b_hub", "Beta Hub content", 2], ["b_features", "Features list", 1]]],
    ["HV Test", [["t_scores", "Scorecards", 2]]],
    ["Haritt Developers", [["enquiries", "Project enquiries", 2]]],
    ["Social Media Accounts", [["social_logins", "Social media logins (passwords stay encrypted)", 2]]],
    ["Other admin pages", [["pg_brand", "Brand assets", 1], ["pg_media", "Covers & thumbnails", 1], ["pg_designs", "Design decisions", 1], ["pg_infra", "Infrastructure", 1], ["pg_launch", "Launch guide", 1], ["pg_setup", "haritt.com setup", 1], ["pg_programs", "Claude programs", 1], ["pg_rules", "Rules & scripts", 1], ["pg_changelog", "Changelog", 1]]],
    ["Team", [["team", "Add or remove people", 2]]]
  ];
  var KEYS = []; AREAS.forEach(function (g) { g[1].forEach(function (a) { KEYS.push(a[0]); }); });
  var ROLES = {
    cofounder: { n: "Co-founder", d: "Everything, can edit. Can add and remove people.", p: function () { var o = {}; AREAS.forEach(function (g) { g[1].forEach(function (a) { o[a[0]] = a[2]; }); }); return o; } },
    manager: { n: "Manager", d: "Edit only the pages you choose.", p: function () { return { an_reset: 1, b_reports: 2, b_ideas: 2, b_testers: 1, b_survey: 1, b_features: 1 }; } },
    viewer: { n: "Viewer", d: "Can look, can't change anything.", p: function () { return { an_reset: 1, b_reports: 1, b_ideas: 1, b_features: 1 }; } },
    custom: { n: "Custom", d: "Pick access page by page.", p: function () { return {}; } }
  };
  function full() { var o = {}; KEYS.forEach(function (k) { o[k] = 2; }); return o; }
  /* get(path) returns the Firestore REST document, or throws an error with .status */
  async function load(user, get) {
    if (!user) return null;
    if (window.__HV_TEST_ADMIN && window.__HV_TEST_ADMIN.member) return mk(window.__HV_TEST_ADMIN.member);
    if (window.__HV_TEST_ADMIN || user.uid === OWNER) return mk({ owner: true, role: "owner", p: full() });
    var em = String(user.email || "").toLowerCase(); if (!em) return null;
    try {
      var d = await get("/team/" + encodeURIComponent(em)), f = (d && d.fields) || {}, p = {};
      var pm = f.p && f.p.mapValue && f.p.mapValue.fields || {};
      Object.keys(pm).forEach(function (k) { p[k] = Number(pm[k].integerValue || pm[k].doubleValue || 0); });
      return mk({ owner: false, role: (f.role && f.role.stringValue) || "custom", name: f.name && f.name.stringValue, p: p });
    } catch (e) { if (e && (e.status === 403 || e.status === 404)) return null; throw e; }
  }
  function mk(a) { a.lv = function (k) { return a.p[k] || 0; }; a.any = function (pre) { return KEYS.some(function (k) { return (!pre || k.indexOf(pre) === 0) && a.lv(k) > 0; }); }; return a; }
  window.HVAccess = { OWNER: OWNER, AREAS: AREAS, KEYS: KEYS, ROLES: ROLES, load: load };
})();
