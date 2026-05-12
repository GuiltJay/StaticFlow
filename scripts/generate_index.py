from pathlib import Path
from datetime import datetime

ROOT = Path('.')

EXCLUDED = {
    'index.html',
    '404.html'
}

html_files = []

for file in ROOT.rglob('*.html'):
    if '.github' in file.parts:
        continue

    if file.name in EXCLUDED:
        continue

    if any(part.startswith('.') for part in file.parts):
        continue

    html_files.append(file)

html_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

cards = []

for file in html_files:
    relative = file.as_posix()
    title = file.stem.replace('-', ' ').replace('_', ' ').title()

    modified = datetime.fromtimestamp(file.stat().st_mtime)
    modified_str = modified.strftime('%Y-%m-%d %H:%M')

    cards.append(f'''
    <a class="card" href="{relative}">
        <div class="title">{title}</div>
        <div class="path">{relative}</div>
        <div class="time">Updated: {modified_str}</div>
    </a>
    ''')

html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard</title>

<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: Arial, sans-serif;
    background: #0f172a;
    color: white;
    padding: 30px;
}}

h1 {{
    margin-bottom: 10px;
    font-size: 32px;
}}

.subtitle {{
    opacity: 0.7;
    margin-bottom: 30px;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
}}

.card {{
    display: block;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 20px;
    text-decoration: none;
    color: white;
    transition: 0.2s;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: #60a5fa;
}}

.title {{
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}}

.path {{
    word-break: break-all;
    opacity: 0.7;
    font-size: 14px;
    margin-bottom: 12px;
}}

.time {{
    font-size: 13px;
    opacity: 0.6;
}}

.search {{
    width: 100%;
    padding: 15px;
    margin-bottom: 25px;
    border-radius: 12px;
    border: none;
    outline: none;
    background: #1e293b;
    color: white;
    font-size: 16px;
}}

.footer {{
    margin-top: 40px;
    opacity: 0.6;
    text-align: center;
}}
</style>
</head>
<body>

<h1>HTML Dashboard</h1>
<div class="subtitle">Automatically generated from GitHub repository</div>

<input type="text" class="search" id="search" placeholder="Search HTML files...">

<div class="grid" id="grid">
    {''.join(cards)}
</div>

<div class="footer">
    Total Files: {len(cards)}
</div>

<script>
const search = document.getElementById('search');
const cards = document.querySelectorAll('.card');

search.addEventListener('input', () => {{
    const q = search.value.toLowerCase();

    cards.forEach(card => {{
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(q) ? 'block' : 'none';
    }});
}});
</script>

</body>
</html>
'''

Path('index.html').write_text(html, encoding='utf-8')

print(f'Generated index with {len(cards)} HTML files.')
