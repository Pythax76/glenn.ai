import os, sqlite3

# We’ll try both locations so it works with your current scaffold or older layout
DB_CANDIDATES = [
    os.path.join("data", "glenn_memory.db"),  # preferred (scaffold)
    "glenn_memory.db",                        # legacy root
]

def _find_db():
    for p in DB_CANDIDATES:
        if os.path.exists(p):
            return p
    return None

def _fetch_last(conn, n=5, persona=None):
    q = "SELECT id, timestamp, user_input, persona, response FROM memory_log"
    args = []
    if persona:
        q += " WHERE persona = ?"
        args.append(persona)
    q += " ORDER BY id DESC LIMIT ?"
    args.append(n)
    cur = conn.execute(q, tuple(args))
    return cur.fetchall()

def run(n="5", persona=None, **kwargs):
    """
    recall.last:
      n=<int>            -> how many rows to show (default 5)
      persona=<name>     -> filter by persona (optional)

    Examples:
      recall.last
      recall.last n=10
      recall.last persona=Echo
    """
    db_path = _find_db()
    if not db_path:
        return "recall.last: no glenn_memory.db found in ./data or repo root."

    try:
        n_int = int(n)
    except ValueError:
        n_int = 5

    try:
        conn = sqlite3.connect(db_path)
    except Exception as e:
        return f"recall.last: failed to open DB: {e}"

    try:
        rows = _fetch_last(conn, n=n_int, persona=persona)
    except sqlite3.OperationalError as e:
        # Probably missing table
        return f"recall.last: memory_log table not found in {db_path} ({e})"
    finally:
        conn.close()

    if not rows:
        return f"recall.last: no entries found (db={db_path}, persona={persona or 'any'})"

    print(f"recall.last: showing {len(rows)} entr{'y' if len(rows)==1 else 'ies'} (db={db_path}, persona={persona or 'any'})")
    for (rid, ts, user_input, pers, resp) in rows:
        print(f"  [{rid}] {ts} | {pers}")
        print(f"      > {user_input}")
        if resp is not None and str(resp).strip():
            # Keep response single-line-ish for terminal readability
            snippet = str(resp).replace('\n', ' ')[:200]
            print(f"      < {snippet}")
    return "OK"
