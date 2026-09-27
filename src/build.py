import re, os, sys
here = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
page = open(os.path.join(here, 'page.html')).read()
def load(n):
    s = open(os.path.join(here, n)).read().strip()
    s = s.replace('xmlns="http://www.w3.org/2000/svg" ', '')
    if 'aria-hidden' not in s: s = s.replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1)
    return s
logos = {'WORLD': load('world.svg'), 'VAULT': load('logo-vault.svg'), 'RESET': load('logo-reset.svg'), 'TEST': load('logo-test.svg')}
n = [0]
def unique(svg):                      # every inline copy gets its own gradient ids
    n[0] += 1; k = 'i%d' % n[0]
    ids = re.findall(r'id="([^"]+)"', svg)
    for i in ids:
        svg = svg.replace('id="%s"' % i, 'id="%s-%s"' % (i, k)).replace('url(#%s)' % i, 'url(#%s-%s)' % (i, k))
    return svg
def sub_logo(m):
    name, sm = m.group(1), m.group(2)
    s = unique(logos[name])
    if sm: s = s.replace('<svg ', '<svg style="width:22px;height:22px;border-radius:7px" ', 1)
    return s
page = re.sub(r'\{\{LOGO_(WORLD|VAULT|RESET|TEST)(_SM)?\}\}', sub_logo, page)
I = lambda d: '<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' + d + '</svg>'
icons = {
 'CHECK': I('<circle cx="12" cy="12" r="10" stroke-width="2"/><path d="M8 12.5l2.6 2.6L16.5 9"/>'),
 'ARROW': I('<path d="M5 12h14M13 6l6 6-6 6"/>'),
 'SYNC': I('<path d="M21 12a9 9 0 0 1-15.5 6.2M3 12A9 9 0 0 1 18.5 5.8"/><path d="M18.5 2v4h-4M5.5 22v-4h4"/>'),
 'USER': I('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
 'GRID': I('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
 'BOARD': I('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 4v16"/>'),
 'BRIEF': I('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>'),
 'BELL': I('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 8 3 8H3s3-1 3-8"/><path d="M10 20a2 2 0 0 0 4 0"/>'),
 'CAL': I('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>'),
 'WAND': I('<path d="M15 4V2M15 10V8M11 6h2M17 6h2M4 20l10-10"/><path d="M18.5 12.5l1 1M20 16l1.5.5"/>'),
 'FILE': I('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>'),
 'MSG': I('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-5A8 8 0 1 1 21 12z"/>'),
 'LIST': I('<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>'),
 'TARGET': I('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/>'),
 'CHART': I('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'),
 'CLOUD': I('<path d="M7 18a5 5 0 1 1 .8-9.9A6 6 0 0 1 19 9.5a4.3 4.3 0 0 1-1 8.5z"/>'),
 'CLOCK': I('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 'ROUTE': I('<circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.5 19H16a3.5 3.5 0 0 0 0-7H8a3.5 3.5 0 0 1 0-7h7.5"/>'),
 'PAUSE': I('<path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/>'),
 'CUP': I('<path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 3v3M12 3v3"/>'),
 'NOTE': I('<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>'),
 'SUN': I('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
 'SHUFFLE': I('<path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/>'),
 'SHIELD': I('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>'),
 'HEART': I('<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21.5l8.8-8.8a5 5 0 0 0 0-7.1z"/>'),
 'PLUS': I('<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>'),
 'LINKEDIN': '<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.5-1 1.8-2 3.7-2 4 0 4.7 2.6 4.7 6V21h-4v-5.3c0-1.3 0-2.9-1.8-2.9s-2 1.4-2 2.8V21H9z"/></svg>',
 'SPARK': I('<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 17l.7 1.8 1.8.7-1.8.7L19 22l-.7-1.8-1.8-.7 1.8-.7z"/>'),
}
page = re.sub(r'\{\{I_([A-Z]+)\}\}', lambda m: icons[m.group(1)], page)
assert '{{' not in page, re.findall(r'\{\{[^}]+\}\}', page)
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w').write(page)
open(os.path.join(out, 'favicon.svg'), 'w').write(open(os.path.join(here, 'world.svg')).read())
print('ok', len(page), 'bytes,', n[0], 'logos')
