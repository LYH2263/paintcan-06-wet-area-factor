import sqlite3
def list_all(conn): return [dict(r) for r in conn.execute("SELECT * FROM rooms ORDER BY id").fetchall()]
def get(conn, rid):
    row = conn.execute("SELECT * FROM rooms WHERE id=?", (rid,)).fetchone()
    return dict(row) if row else None
def set_wet(conn, rid, wet):
    cur = conn.execute("UPDATE rooms SET wet=? WHERE id=?", (1 if wet else 0, rid))
    conn.commit()
    if cur.rowcount == 0:
        return None
    return get(conn, rid)
