#!/usr/bin/env python3
"""Fetch arXiv paper abstracts and save as raw sources."""
import urllib.request
import xml.etree.ElementTree as ET
import hashlib
import sys
import time

def fetch(arxiv_id):
    url = f'https://export.arxiv.org/api/query?id_list={arxiv_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'SyntheticMembraneWiki/1.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(data)
    entry = root.find('a:entry', ns)
    if entry is None:
        print(f'ERROR: Paper {arxiv_id} not found')
        return
    
    title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    summary = entry.find('a:summary', ns).text.strip()
    authors = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
    published = entry.find('a:published', ns).text[:10]
    
    fname = arxiv_id.replace('.', '-')
    body = f'# {title}\n\n'
    body += f'**Authors:** {authors}\n\n'
    body += f'**Published:** {published}\n\n'
    body += f'**arXiv:** [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})\n\n'
    body += f'**PDF:** https://arxiv.org/pdf/{arxiv_id}\n\n'
    body += f'## Abstract\n\n{summary}\n'
    
    sha = hashlib.sha256(body.encode()).hexdigest()
    content = f'---\nsource_url: https://arxiv.org/abs/{arxiv_id}\ningested: 2026-04-27\nsha256: {sha}\n---\n\n' + body
    
    with open(f'/home/axjns/wiki/synthetic-membrane/raw/articles/{fname}.md', 'w') as f:
        f.write(content)
    print(f'Saved: {fname}.md — {title[:80]}')

if __name__ == "__main__":
    ids = sys.argv[1:] if len(sys.argv) > 1 else []
    for arxiv_id in ids:
        fetch(arxiv_id)
        time.sleep(3)
