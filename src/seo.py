"""HV World: search-engine data for every page (JSON-LD structured data, robots meta, sitemap).
Kept honest: only facts that are true on the site (free apps, web apps, the launch video, the FAQs shown on the page)."""
import json, datetime

SITE = "https://harshvittori.github.io"
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "HV World", "alternateName": "HVWorld", "url": SITE + "/", "description": "HV World makes three free AI-powered apps for personal and career growth: HV Test (self-assessment), HV Reset (daily planner) and HV Vault (job search tracker), with HV AI built in.", "foundingDate": "2026-10-01",
       "logo": SITE + "/icons/hv-world-512.png", "founder": {"@type": "Person", "name": "Harsh Goyal", "url": "https://www.linkedin.com/in/harshvittori"},
       "sameAs": ["https://www.linkedin.com/in/harshvittori", "https://www.youtube.com/watch?v=SaSfRrtvrTg"]}
APP_INFO = {
    "test": dict(name="HV Test", url=SITE + "/hv-tests/", cat="EducationalApplication",
                 desc="Free self-assessment tests with an honest score, a checkable scorecard, a full report and a 30-day plan. No login."),
    "reset": dict(name="HV Reset", url=SITE + "/hv-reset/", cat="LifestyleApplication",
                  desc="Free daily planner: one task at a time, a day that adjusts when you're late, and a personal dashboard for time, focus and streaks."),
    "vault": dict(name="HV Vault", url=SITE + "/hv-vault-web/", cat="BusinessApplication",
                  desc="Free job-search tracker: every job, company, follow-up and interview on one board, with HV AI to update it for you."),
}

def ld(*items):
    return '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@graph": list(items)}, ensure_ascii=False, separators=(",", ":"))

def faq(qas):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}

def crumbs(*pairs):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(pairs)]}

def app(key, page_url):
    a = APP_INFO[key]
    return {"@type": "WebApplication", "@id": a["url"] + "#app", "name": a["name"], "url": a["url"], "description": a["desc"],
            "applicationCategory": a["cat"], "operatingSystem": "Any (web browser)", "inLanguage": ["en", "hi"],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "publisher": {"@id": SITE + "/#org"},
            "mainEntityOfPage": SITE + page_url}

def home(qas):
    web = {"@type": "WebSite", "@id": SITE + "/#website", "name": "HV World", "alternateName": ["HVWorld", "HV World by Harsh Goyal"], "url": SITE + "/", "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en"}
    return ld(ORG, web, app("test", "/test/"), app("reset", "/reset/"), app("vault", "/vault/"), faq(qas))

def app_page(key, qas):
    return ld(ORG, app(key, "/%s/" % key), crumbs(("HV World", "/"), (APP_INFO[key]["name"], "/%s/" % key)), faq(qas))

def watch():
    v = {"@type": "VideoObject", "name": "Say hello to HV World", "description": "The HV World launch video: three free apps and one AI to know yourself, plan your day and land the job.",
         "thumbnailUrl": [SITE + "/watch/og-reveal.jpg", SITE + "/watch/premiere.jpg"], "uploadDate": "2026-10-01T12:00:00+05:30",
         "duration": "PT2M21S", "contentUrl": SITE + "/media/hv-world-launch.mp4", "embedUrl": "https://www.youtube.com/embed/SaSfRrtvrTg",
         "publisher": {"@id": SITE + "/#org"}}
    return ld(ORG, v, crumbs(("HV World", "/"), ("Watch", "/watch/")))

def simple(name, url):
    return ld(ORG, crumbs(("HV World", "/"), (name, url)))

ROBOTS = '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"><meta property="og:locale" content="en_IN"><meta name="author" content="Harsh Goyal">'

def add(page, block):
    return page.replace("</head>", ROBOTS + block + "\n</head>", 1)

def sitemap(root):
    today = datetime.date.today().isoformat()
    urls = [("/", "weekly", "1.0"), ("/watch/", "monthly", "0.9"), ("/story/", "monthly", "0.8"), ("/test/", "weekly", "0.9"), ("/reset/", "weekly", "0.9"), ("/vault/", "weekly", "0.9"),
            ("/hv-tests/", "weekly", "0.8"), ("/hv-tests/tests/maturity-assessment/", "weekly", "0.8"), ("/hv-reset/", "weekly", "0.7"), ("/hv-vault-web/", "weekly", "0.7"),
            ("/terms/", "yearly", "0.2"), ("/privacy/", "yearly", "0.2")]
    body = "".join("  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>\n" % (SITE, u, today, f, p) for u, f, p in urls)
    open(root + "/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
