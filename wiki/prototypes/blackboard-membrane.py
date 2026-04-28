#!/usr/bin/env python3
"""
Prototype B: Blackboard Membrane

SQLite-backed shared blackboard with event subscriptions.
Agents contribute to a shared board, others react to changes.
No network needed — single SQLite file persists state.

Inspired by: classic AI blackboard architecture, mycelial networks.
"""
import sqlite3
import json
import time
import uuid
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any


DB_FILE = Path(__file__).parent / "blackboard.db"


@dataclass
class BoardEntry:
    id: str
    agent_id: str
    section: str       # e.g. "research.findings", "draft.body", "review.comments"
    data: str          # JSON-encoded
    priority: int = 0  # 0=normal, 1=high, 2=urgent
    created: float = field(default_factory=time.time)
    expiry: float | None = None
    status: str = "active"  # active | resolved | superseded
    
    def to_dict(self) -> dict:
        return asdict(self)


class BlackboardMembrane:
    """
    SQLite-backed blackboard with event-driven subscriptions.
    
    Architecture:
    - BOARD table: persistent entries from all agents
    - EVENTS table: immutable log of all changes
    - AGENTS table: registered agents with capabilities
    - SUBSCRIPTIONS table: agent -> section mappings
    """
    
    def __init__(self, db_path: Path | str = DB_FILE):
        self._conn = sqlite3.connect(str(db_path))
        self._conn.row_factory = sqlite3.Row
        self._init_schema()
    
    def _init_schema(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                capabilities TEXT NOT NULL DEFAULT '[]',
                registered_at REAL NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS subscriptions (
                agent_id TEXT NOT NULL,
                section TEXT NOT NULL,
                PRIMARY KEY (agent_id, section),
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
            );
            
            CREATE TABLE IF NOT EXISTS board (
                entry_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                section TEXT NOT NULL,
                data TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                created REAL NOT NULL,
                expiry REAL,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
            );
            
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                section TEXT,
                entry_id TEXT,
                payload TEXT,
                created REAL NOT NULL,
                FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
                FOREIGN KEY (entry_id) REFERENCES board(entry_id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_board_section ON board(section, status);
            CREATE INDEX IF NOT EXISTS idx_board_priority ON board(priority, created);
            CREATE INDEX IF NOT EXISTS idx_events_agent ON events(agent_id, created);
            CREATE INDEX IF NOT EXISTS idx_events_section ON events(section, created);
        """)
        self._conn.commit()
    
    # ── Agent Registration ──
    
    def register_agent(self, agent_id: str, capabilities: list[str],
                       subscriptions: list[str] | None = None):
        self._conn.execute(
            "INSERT OR REPLACE INTO agents VALUES (?, ?, ?)",
            (agent_id, json.dumps(capabilities), time.time()),
        )
        if subscriptions:
            for section in subscriptions:
                self._conn.execute(
                    "INSERT OR REPLACE INTO subscriptions VALUES (?, ?)",
                    (agent_id, section),
                )
        event_id = str(uuid.uuid4())
        self._conn.execute(
            "INSERT INTO events VALUES (?, 'register', ?, NULL, NULL, ?, ?)",
            (event_id, agent_id, json.dumps({"capabilities": capabilities, "subscriptions": subscriptions or []}), time.time()),
        )
        self._conn.commit()
    
    # ── Board Operations ──
    
    def contribute(self, agent_id: str, section: str, data: Any,
                   priority: int = 0, expiry: float | None = None) -> str:
        entry_id = str(uuid.uuid4())
        self._conn.execute(
            "INSERT INTO board VALUES (?, ?, ?, ?, ?, ?, ?, 'active')",
            (entry_id, agent_id, section, json.dumps(data), priority, time.time(), expiry),
        )
        event_id = str(uuid.uuid4())
        self._conn.execute(
            "INSERT INTO events VALUES (?, 'contribute', ?, ?, ?, ?, ?)",
            (event_id, agent_id, section, entry_id, json.dumps(data), time.time()),
        )
        self._conn.commit()
        return entry_id
    
    def read_board(self, reader_id: str, section: str | None = None,
                   status: str = "active") -> list[dict]:
        query = "SELECT * FROM board WHERE status = ?"
        params: list = [status]
        if section:
            query += " AND section = ?"
            params.append(section)
        query += " ORDER BY priority DESC, created DESC"
        rows = self._conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    
    def resolve(self, entry_id: str, resolver_id: str, resolution: Any):
        section = self._conn.execute(
            "SELECT section FROM board WHERE entry_id = ?", (entry_id,)
        ).fetchone()
        self._conn.execute(
            "UPDATE board SET status = 'resolved' WHERE entry_id = ?",
            (entry_id,),
        )
        event_id = str(uuid.uuid4())
        self._conn.execute(
            "INSERT INTO events VALUES (?, 'resolve', ?, ?, ?, ?, ?)",
            (event_id, resolver_id, section[0] if section else None,
             entry_id, json.dumps(resolution), time.time()),
        )
        self._conn.commit()
    
    # ── Events ──
    
    def get_events(self, agent_id: str, since: float | None = None,
                   limit: int = 50) -> list[dict]:
        query = """
            SELECT e.* FROM events e
            JOIN subscriptions s ON e.section = s.section AND s.agent_id = ?
            WHERE e.event_type != 'register'
        """
        params: list = [agent_id]
        if since:
            query += " AND e.created > ?"
            params.append(since)
        query += " ORDER BY e.created DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    
    def get_event_stream(self, since: float | None = None,
                         section: str | None = None, limit: int = 100) -> list[dict]:
        query = "SELECT * FROM events WHERE 1=1"
        params: list = []
        if since:
            query += " AND created > ?"
            params.append(since)
        if section:
            query += " AND section = ?"
            params.append(section)
        query += " ORDER BY created DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    
    # ── Cleanup ──
    
    def expire_entries(self) -> int:
        now = time.time()
        cur = self._conn.execute(
            "UPDATE board SET status = 'expired' WHERE expiry IS NOT NULL AND expiry < ? AND status = 'active'",
            (now,),
        )
        self._conn.commit()
        return cur.rowcount
    
    # ── Stats ──
    
    def stats(self) -> dict:
        agents = self._conn.execute("SELECT COUNT(*) FROM agents").fetchone()[0]
        entries = self._conn.execute("SELECT COUNT(*) FROM board").fetchone()[0]
        events = self._conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        sections = self._conn.execute("SELECT COUNT(DISTINCT section) FROM board").fetchone()[0]
        return {"agents": agents, "entries": entries, "events": events, "sections": sections}
    
    def close(self):
        self._conn.close()


# ── Demo: Three agents collaborating on a document ──

def demo():
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        bb = BlackboardMembrane(tmp.name)
        
        print("=" * 60)
        print("SYNTHETIC MEMBRANE — Blackboard Prototype")
        print("=" * 60)
        
        # Register agents
        bb.register_agent("researcher", ["web_search", "data_analysis"],
                          subscriptions=["research.findings", "review.comments"])
        bb.register_agent("writer", ["drafting", "editing"],
                          subscriptions=["research.findings", "review.comments"])
        bb.register_agent("reviewer", ["code_review", "fact_checking"],
                          subscriptions=["draft.body"])
        print(f"\n[Agents] researcher, writer, reviewer registered")
        print(f"[Stats] {json.dumps(bb.stats(), indent=2)}")
        
        # Researcher contributes findings
        bb.contribute("researcher", "research.findings",
                      {"topic": "synthetic membrane", "source": "biological literature",
                       "finding": "Cell membranes use selective permeability and signal transduction"})
        bb.contribute("researcher", "research.findings",
                      {"topic": "multi-agent systems", "source": "arxiv survey 2025",
                       "finding": "A2A protocol emerging as standard for agent communication"})
        print("\n[Contribute] researcher -> research.findings (2 entries)")
        
        # Writer reads research and drafts
        findings = bb.read_board("writer", "research.findings")
        print(f"[Read] writer sees {len(findings)} research findings")
        
        bb.contribute("writer", "draft.body",
                      {"section": "introduction",
                       "text": "The synthetic membrane concept draws from biological cell membranes,"
                               " which control what passes through while enabling cells to sense and"
                               " respond to their environment."})
        print(f"[Contribute] writer -> draft.body (introduction)")
        
        # Reviewer reads draft and comments
        draft = bb.read_board("reviewer", "draft.body")
        print(f"[Read] reviewer sees {len(draft)} draft sections")
        
        bb.contribute("reviewer", "review.comments",
                      {"on": "introduction",
                       "comment": "Good analogy. Consider also mentioning gap junctions for"
                                  " direct cell-to-cell communication as a parallel."})
        print(f"[Contribute] reviewer -> review.comments")
        
        # Writer sees review and revises
        reviews = bb.get_events("writer", since=time.time() - 10)
        print(f"[Events] writer has {len(reviews) if reviews else 0} new events")
        
        bb.contribute("writer", "draft.body",
                      {"section": "introduction_v2",
                       "text": "The synthetic membrane concept draws from biological systems:"
                               " cell membranes (selective permeability), gap junctions (direct"
                               " inter-cellular channels), and quorum sensing (population-level"
                               " coordination). These biological patterns inform our architecture."})
        print(f"[Contribute] writer -> draft.body (revised introduction)")
        
        # Resolve original draft section
        if draft:
            bb.resolve(draft[0]["entry_id"], "writer", "superseded by introduction_v2")
        
        print(f"\n[Final Board]: {json.dumps(bb.stats(), indent=2)}")
        print(f"\n[Event Stream]:")
        for ev in bb.get_event_stream(limit=10):
            print(f"  {ev['created']:.0f} | {ev['event_type']} | {ev['agent_id']} -> {ev['section']}")
        
        bb.close()
        print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
