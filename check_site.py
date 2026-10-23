"""Check all internal page links, fragment targets and local assets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent

class Page(HTMLParser):
    def __init__(self, file):
        super().__init__()
        self.links, self.ids, self.current, self.h1 = [], set(), [], 0
        self.feed(file.read_text(encoding='utf-8'))
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate id: {a["id"]}'
            self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        for k in ('href', 'src'):
            if k in a: self.links.append(a[k])
        if tag == 'a' and a.get('aria-current') == 'page': self.current.append(a['href'])

pages = {p.name: Page(p) for p in root.glob('*.html')}
assert len(pages) == 10
for name, page in pages.items():
    assert page.h1 == 1, f'{name}: must contain one primary heading'
    expected = name if name in ('index.html', 'research.html', 'portfolio.html', 'cv.html', 'work.html', 'contact.html') else 'portfolio.html'
    assert page.current == [expected], f'{name}: incorrect active navigation'
    for url in page.links:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc: continue
        path = unquote(parts.path)
        target = root / path if path else root / name
        assert target.is_file() and target.stat().st_size, f'{name}: missing {url}'
        if parts.fragment:
            assert target.name in pages and parts.fragment in pages[target.name].ids, f'{name}: invalid fragment {url}'
for svg in (root / 'assets').glob('*.svg'):
    el = ET.parse(svg).getroot()
    assert el.attrib.get('width') and el.attrib.get('height'), f'Missing SVG dimensions: {svg}'
assert (root / 'assets/CV-Jinman-Zhang.pdf').read_bytes().startswith(b'%PDF')
print('PASS: ten pages, active navigation, all local links/fragments/assets, SVG dimensions and CV PDF.')
