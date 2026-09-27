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
 'SPARK': I('<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 17l.7 1.8 1.8.7-1.8.7L19 22l-.7-1.8-1.8-.7 1.8-.7z"/>'),
}
page = re.sub(r'\{\{I_([A-Z]+)\}\}', lambda m: icons[m.group(1)], page)
assert '{{' not in page, re.findall(r'\{\{[^}]+\}\}', page)
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w').write(page)
open(os.path.join(out, 'favicon.svg'), 'w').write(open(os.path.join(here, 'world.svg')).read())
print('ok', len(page), 'bytes,', n[0], 'logos')
