import sqlite3
def list_all(conn): return [dict(r) for r in conn.execute("SELECT * FROM rooms ORDER BY id").fetchall()]
def get(conn, rid):
    row = conn.execute("SELECT * FROM rooms WHERE id=?", (rid,)).fetchone()
    return dict(row) if row else None
def set_damp(conn, rid, damp):
    cur = conn.execute("UPDATE rooms SET damp=? WHERE id=?", (1 if damp else 0, rid))
    conn.commit(); return cur.rowcount > 0
