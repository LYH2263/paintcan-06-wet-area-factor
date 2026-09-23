import json, sqlite3
from datetime import datetime, timezone
def insert(conn, kind, payload, result, room_id=None):
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute("INSERT INTO calc_runs(kind,room_id,input_json,result_json,created_at) VALUES (?,?,?,?,?)",
        (kind, room_id, json.dumps(payload, ensure_ascii=False), json.dumps(result, ensure_ascii=False), now))
    conn.commit(); return int(cur.lastrowid)
def list_recent(conn, limit=50):
    return [dict(r) for r in conn.execute("SELECT * FROM calc_runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]
def get(conn, run_id):
    row = conn.execute("SELECT * FROM calc_runs WHERE id=?", (run_id,)).fetchone()
    if not row:
        return None
    d = dict(row)
    # 历史按编号取出：解析钉选当时的入参与结果（系数、升数已固化在记录里）
    d["input"] = json.loads(d.pop("input_json") or "{}")
    d["result"] = json.loads(d.pop("result_json") or "{}")
    return d
