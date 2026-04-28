#!/usr/bin/env python3
"""Search Semantic Scholar API and print clean results. Uses only stdlib."""
import urllib.request, json, sys, urllib.parse, time

API = "https://api.semanticscholar.org/graph/v1/paper/search"

def search(query, limit=8, fields=None):
    if fields is None:
        fields = "title,authors,year,citationCount,abstract,externalIds"
    url = f"{API}?query={urllib.parse.quote(query)}&limit={limit}&fields={fields}"
    for attempt in range(5):
        time.sleep(1.5 * (2 ** attempt))  # Exponential backoff from 1.5s
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = json.loads(resp.read())
            return data.get("data", [])
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}", file=sys.stderr)
            if attempt == 4:
                print(f"  All attempts failed for: {query}", file=sys.stderr)
                return []

def print_results(results):
    for i, r in enumerate(results):
        title = r.get("title", "N/A")
        authors = [a.get("name", "") for a in r.get("authors", [])]
        authors_str = ', '.join(authors[:4])
        if len(authors) > 4:
            authors_str += f" (+{len(authors)-4})"
        year = r.get("year", "?")
        cite_count = r.get("citationCount", 0)
        abstract = (r.get("abstract") or "No abstract")[:300]
        ext = r.get("externalIds", {})
        arxiv_id = ext.get("ArXiv", "N/A")
        print(f"{i+1}. [{arxiv_id}] {title}")
        print(f"   Authors: {authors_str}")
        print(f"   Year: {year} | Citations: {cite_count}")
        print(f"   Abstract: {abstract}...")
        print()

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "multi-agent LLM coordination"
    results = search(query)
    print(f"=== Search: {query} ===\n")
    print_results(results)
