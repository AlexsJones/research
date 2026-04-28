#!/usr/bin/env python3
"""Batch arXiv + Semantic Scholar research session with proper rate limiting."""
import urllib.request, xml.etree.ElementTree as ET, json, urllib.parse, time, sys

API_ARXIV = "https://export.arxiv.org/api/query"
API_SS = "https://api.semanticscholar.org/graph/v1/paper/search"
NS = {'a': 'http://www.w3.org/2005/Atom'}

def fetch_arxiv_ids(ids):
    """Fetch specific arXiv IDs."""
    results = []
    for iid in ids:
        time.sleep(3)
        iid_clean = iid.strip()
        url = f"{API_ARXIV}?id_list={iid_clean}"
        for attempt in range(3):
            time.sleep(3 * attempt)
            try:
                with urllib.request.urlopen(url, timeout=30) as resp:
                    root = ET.fromstring(resp.read())
                for entry in root.findall('a:entry', NS):
                    title = entry.find('a:title', NS).text.strip().replace('\n', ' ')
                    arxiv_id = entry.find('a:id', NS).text.strip().split('/abs/')[-1]
                    published = entry.find('a:published', NS).text[:10]
                    authors = ', '.join(a.find('a:name', NS).text for a in entry.findall('a:author', NS))
                    summary = entry.find('a:summary', NS).text.strip()[:500]
                    cats = ', '.join(c.get('term') for c in entry.findall('a:category', NS))
                    results.append({'id': arxiv_id, 'title': title, 'published': published,
                                   'authors': authors, 'summary': summary, 'categories': cats})
                break
            except Exception as e:
                print(f"  arXiv fetch {iid} attempt {attempt+1} failed: {e}", file=sys.stderr)
                if attempt == 2:
                    results.append({'id': iid, 'error': str(e)})
    return results

def search_ss(query, limit=5):
    """Search Semantic Scholar with retry."""
    fields = "title,authors,year,citationCount,abstract,externalIds"
    url = f"{API_SS}?query={urllib.parse.quote(query)}&limit={limit}&fields={fields}"
    for attempt in range(5):
        time.sleep(2 + 2 * attempt)
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = json.loads(resp.read())
            return data.get("data", [])
        except Exception as e:
            print(f"  SS search '{query}' attempt {attempt+1}: {e}", file=sys.stderr)
            if attempt == 4:
                return []
    return []

def format_ss(r):
    title = r.get("title", "N/A")
    authors = [a.get("name","") for a in r.get("authors",[])]
    authors_str = ', '.join(authors[:4]) + (f" (+{len(authors)-4})" if len(authors)>4 else "")
    year = r.get("year","?")
    cites = r.get("citationCount",0) or 0
    abstract = (r.get("abstract") or "No abstract")[:400]
    ext = r.get("externalIds",{})
    arxiv = ext.get("ArXiv","N/A")
    return f"[{arxiv}] {title}\n  Authors: {authors_str}\n  Year: {year} | Citations: {cites}\n  Abstract: {abstract}...\n"

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if mode in ("1", "all"):
        # Fetch key papers from first SS search
        print("\n=== Key Papers: Shared Memory & Multi-Agent Coordination ===")
        ids = ["2602.11510", "2604.13120", "2603.15183", "2508.04903", "2504.07303", "2601.06115"]
        for r in fetch_arxiv_ids(ids):
            if "error" in r:
                print(f"[{r['id']}] ERROR: {r['error']}")
            else:
                print(f"[{r['id']}] {r['title']}")
                print(f"  Authors: {r['authors']}")
                print(f"  Published: {r['published']} | Categories: {r['categories']}")
                print(f"  Abstract: {r['summary']}...")
                print()
    
    if mode in ("2", "all"):
        print("\n=== Semantic Scholar: Agent Protocol Standards ===")
        results = search_ss("agent interoperability protocol standard 2025 2026", limit=5)
        for r in results:
            print(format_ss(r))
    
    if mode in ("3", "all"):
        print("\n=== Semantic Scholar: CRDT gossip distributed state ===")
        results = search_ss("CRDT gossip protocol shared state LLM", limit=5)
        for r in results:
            print(format_ss(r))
    
    if mode in ("4", "all"):
        print("\n=== Semantic Scholar: Agent trust security ===")
        results = search_ss("multi-agent LLM trust security authentication", limit=5)
        for r in results:
            print(format_ss(r))
