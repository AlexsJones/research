#!/usr/bin/env python3
"""Query Semantic Scholar API. Usage: python scripts/semanticscholar.py query "agent search" [--limit N] [--fields ...]"""
import urllib.request, json, sys, time, argparse

def query(url, timeout=30, retries=3):
    for attempt in range(retries):
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 10 * (2 ** attempt)
                print(f"Rate limited (429), waiting {wait}s before retry...", file=sys.stderr)
                time.sleep(wait)
            else:
                raise
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['search', 'paper', 'citations', 'references', 'recommend', 'author'])
    parser.add_argument('target', nargs='?', default=None, help='Query string or arXiv ID')
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--fields', type=str, default='title,authors,citationCount,year,externalIds,abstract')
    args = parser.parse_args()

    if args.action == 'search':
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={args.target}&limit={args.limit}&fields={args.fields}"
    elif args.action == 'paper':
        paper_id = args.target or 'arXiv:2402.03300'
        if not paper_id.startswith('arXiv:') and not paper_id.startswith('DOI:'):
            paper_id = f'arXiv:{paper_id}'
        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields={args.fields}"
    elif args.action == 'citations':
        paper_id = args.target or 'arXiv:2402.03300'
        if not paper_id.startswith('arXiv:'): paper_id = f'arXiv:{paper_id}'
        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields={args.fields}&limit={args.limit}"
    elif args.action == 'references':
        paper_id = args.target or 'arXiv:2402.03300'
        if not paper_id.startswith('arXiv:'): paper_id = f'arXiv:{paper_id}'
        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?fields={args.fields}&limit={args.limit}"
    elif args.action == 'author':
        url = f"https://api.semanticscholar.org/graph/v1/author/search?query={args.target}&fields={args.fields}&limit={args.limit}"
    elif args.action == 'recommend':
        url = "https://api.semanticscholar.org/recommendations/v1/papers/"
        time.sleep(1)
        req = urllib.request.Request(url,
            data=json.dumps({"positivePaperIds": [args.target], "negativePaperIds": []}).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        print(json.dumps(data, indent=2))
        return

    time.sleep(1)
    data = query(url)
    print(json.dumps(data, indent=2))

if __name__ == '__main__':
    main()
