#!/usr/bin/env python3
"""Search arXiv API and print clean results."""
import urllib.request
import xml.etree.ElementTree as ET
import sys
import urllib.parse

def search(query, max_results=10, sort_by="submittedDate", sort_order="descending", author=None, category=None):
    parts = []
    if author:
        parts.append(f"au:{urllib.parse.quote(author)}")
    if category:
        parts.append(f"cat:{category}")
    if query:
        parts.append(f"all:{urllib.parse.quote(query)}")
    search_query = "+AND+".join(parts) if len(parts) > 1 else (parts[0] if parts else "all:*")
    
    url = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(search_query)}"
    url += f"&sortBy={sort_by}&sortOrder={sort_order}&max_results={max_results}"
    
    req = urllib.request.Request(url, headers={"User-Agent": "SyntheticMembraneWiki/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml_data = resp.read()
    
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(xml_data)
    results = []
    for entry in root.findall('a:entry', ns):
        title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
        arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
        published = entry.find('a:published', ns).text[:10]
        authors = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
        summary = entry.find('a:summary', ns).text.strip()[:400]
        cats = ', '.join(c.get('term') for c in entry.findall('a:category', ns))
        results.append({
            'id': arxiv_id, 'title': title, 'published': published,
            'authors': authors, 'summary': summary, 'categories': cats
        })
    
    for i, r in enumerate(results):
        print(f"{i+1}. [{r['id']}] {r['title']}")
        print(f"   Authors: {r['authors']}")
        print(f"   Published: {r['published']} | Categories: {r['categories']}")
        print(f"   Abstract: {r['summary']}...")
        print()
    
    return results

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "multi-agent LLM"
    search(query)
