#!/usr/bin/env python3
"""Synthetic Membrane Wiki — ChromaDB operations.

Usage:
    python3 wiki_db.py query "search query" [n_results]
    python3 wiki_db.py upsert /path/to/page.md
    python3 wiki_db.py upsert-all
    python3 wiki_db.py list
    python3 wiki_db.py stats
"""
import chromadb
import os
import sys
import json
import glob
import yaml

WIKI = os.path.expanduser("~/wiki/synthetic-membrane")
DB_PATH = os.path.join(WIKI, ".chroma")


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name="synthetic_membrane",
        metadata={"hnsw:space": "cosine"},
    )


def parse_page(fpath):
    with open(fpath) as f:
        content = f.read()
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    fm = yaml.safe_load(parts[1])
    body = parts[2].strip()
    fname = os.path.basename(fpath)
    return {
        "id": fname.replace(".md", ""),
        "file": fname,
        "path": fpath,
        "type": os.path.basename(os.path.dirname(fpath)),
        "title": str(fm.get("title", fname)),
        "tags": fm.get("tags", []),
        "content": body,
        "updated": str(fm.get("updated", "")),
    }


def chunk_page(page):
    paragraphs = [p.strip() for p in page["content"].split("\n\n") if p.strip()]
    chunks = []
    chunk_text = ""
    chunk_id = 0
    for para in paragraphs:
        if len(chunk_text) + len(para) > 600:
            chunks.append({
                "id": f"{page['id']}_{chunk_id}",
                "text": chunk_text,
                "parent_file": str(page["file"]),
                "parent_type": str(page["type"]),
                "parent_title": str(page["title"]),
                "tags": json.dumps(page["tags"]),
                "updated": str(page["updated"]),
            })
            chunk_id += 1
            chunk_text = para
        else:
            chunk_text = (chunk_text + "\n\n" + para).strip()
    if chunk_text:
        chunks.append({
            "id": f"{page['id']}_{chunk_id}",
            "text": chunk_text,
            "parent_file": str(page["file"]),
            "parent_type": str(page["type"]),
            "parent_title": str(page["title"]),
            "tags": json.dumps(page["tags"]),
            "updated": str(page["updated"]),
        })
    return chunks


def cmd_query(query, n=5):
    coll = get_collection()
    results = coll.query(query_texts=[query], n_results=min(n, max(1, coll.count())))
    output = {"query": query, "results": []}
    if results["ids"][0]:
        for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
            output["results"].append({
                "parent_file": meta["parent_file"],
                "parent_type": meta["parent_type"],
                "parent_title": meta["parent_title"],
                "similarity": round(1 - dist, 3),
                "tags": json.loads(meta["tags"]),
                "text": doc,
            })
    print(json.dumps(output, indent=2))


def cmd_upsert(fpath):
    page = parse_page(fpath)
    if not page:
        print(f"Error: cannot parse {fpath}", file=sys.stderr)
        sys.exit(1)
    chunks = chunk_page(page)
    coll = get_collection()
    coll.upsert(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{k: v for k, v in c.items() if k != "text"} for c in chunks],
    )
    print(f"Upserted {len(chunks)} chunks from {page['file']}")


def cmd_upsert_all():
    pages = []
    for fpath in glob.glob(f"{WIKI}/entities/*.md") + glob.glob(f"{WIKI}/concepts/*.md"):
        page = parse_page(fpath)
        if page:
            pages.append(page)
    coll = get_collection()
    all_chunks = []
    for page in pages:
        all_chunks.extend(chunk_page(page))
    if all_chunks:
        coll.upsert(
            ids=[c["id"] for c in all_chunks],
            documents=[c["text"] for c in all_chunks],
            metadatas=[{k: v for k, v in c.items() if k != "text"} for c in all_chunks],
        )
    print(f"Upserted {len(all_chunks)} chunks from {len(pages)} pages")


def cmd_list():
    coll = get_collection()
    results = coll.get(include=["metadatas"])
    seen = set()
    for meta in results["metadatas"]:
        key = meta["parent_file"]
        if key not in seen:
            seen.add(key)
            print(f"  [{meta['parent_type']}] {meta['parent_title']} ({meta['updated']})")
    print(f"Total unique pages: {len(seen)}, total chunks: {coll.count()}")


def cmd_stats():
    coll = get_collection()
    print(json.dumps({
        "collection": coll.name,
        "chunks": coll.count(),
        "db_path": DB_PATH,
    }, indent=2))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "query":
        cmd_query(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 5)
    elif cmd == "upsert":
        cmd_upsert(sys.argv[2])
    elif cmd == "upsert-all":
        cmd_upsert_all()
    elif cmd == "list":
        cmd_list()
    elif cmd == "stats":
        cmd_stats()
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
