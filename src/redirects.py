"""Old links that forward to a new page. Each keeps the target's link-preview tags, because WhatsApp,
LinkedIn and others read the preview from the first page and do not follow the redirect.
Run after src/site.py:  python3 src/redirects.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REDIRECTS = [("film/index.html", "watch/index.html", "/watch/"), ("overview/index.html", "index.html", "/")]
for out, src, dest in REDIRECTS:
    h = open(os.path.join(ROOT, src)).read()
    metas = "\n".join(re.findall(r'<meta (?:property|name)="(?:og:[^"]*|twitter:[^"]*|video:[^"]*|description)" content="[^"]*">', h))
    title = re.search(r"<title>([^<]*)</title>", h).group(1)
    page = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>%s</title>\n%s\n'
            '<link rel="canonical" href="https://harshvittori.github.io%s"><meta name="robots" content="noindex">\n'
            '<meta http-equiv="refresh" content="0; url=%s"></head>\n<body><p><a href="%s">Open HV World</a></p>'
            '<script>location.replace("%s" + location.hash)</script></body></html>\n') % (title, metas, dest, dest, dest, dest)
    os.makedirs(os.path.dirname(os.path.join(ROOT, out)), exist_ok=True)
    open(os.path.join(ROOT, out), "w").write(page)
    print("ok", out, "->", dest)
