"""Check local preview routes, resources, image alternatives and page metadata."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parent
errors = []
pages = list(root.rglob('index.html'))

class Check(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path = path; self.ids = []; self.refs = []; self.headings = 0; self.title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'h1': self.headings += 1
        if tag == 'title': self.title = True
        if tag == 'img' and not a.get('alt'): errors.append(f'{self.path}: image missing alt')
        for key in ('href', 'src'):
            if a.get(key): self.refs.append(a[key])

documents = {}
for path in pages:
    parser = Check(path.relative_to(root)); parser.feed(path.read_text(encoding='utf-8')); documents[path] = parser
    if parser.headings != 1 or not parser.title: errors.append(f'{parser.path}: title or H1 issue')
    for key, count in Counter(parser.ids).items():
        if count > 1: errors.append(f'{parser.path}: duplicate id {key}')
count = 0
for path, parser in documents.items():
    for ref in parser.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc or ref.startswith('//'): continue
        target = (root / unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (path.parent / unquote(url.path))
        target = target.resolve()
        if target.is_dir(): target = target / 'index.html'
        count += 1
        if not target.is_file(): errors.append(f'{parser.path}: missing {ref}')
        elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
            errors.append(f'{parser.path}: missing anchor {ref}')
print(f'Checked {len(pages)} pages and {count} local links/resources.')
print('\n'.join(errors) if errors else 'No missing targets, duplicate IDs, missing alt or title/H1 issues.')
raise SystemExit(bool(errors))

