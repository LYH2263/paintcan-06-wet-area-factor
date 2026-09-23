import json
from app.db import connect
from app.engines.estimate import estimate_room
from app.repositories import openings, rooms, runs, settings

class PaintService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_rooms(self): return rooms.list_all(self._c)
    def room_detail(self, rid):
        r = rooms.get(self._c, rid)
        if not r: return None
        return {"room": r, "openings": openings.for_room(self._c, rid)}
    def set_damp(self, rid, damp):
        return self.room_detail(rid) if rooms.set_damp(self._c, rid, damp) else None
    def settings(self): return settings.get_map(self._c)
    def update_setting(self, key, value):
        settings.set_value(self._c, key, value)
        return self.settings()
    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def run_detail(self, rid):
        row = runs.get(self._c, rid)
        if not row: return None
        return {"id": row["id"], "kind": row["kind"], "room_id": row["room_id"],
                "created_at": row["created_at"],
                "input": json.loads(row["input_json"]), "result": json.loads(row["result_json"])}
    def estimate(self, room_id, persist, coats=None, coverage=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings.coverage_coats(self._c)
        cov = float(coverage or cov)
        ct = int(coats or ct)
        damp = bool(r.get("damp"))
        factor = settings.damp_factor(self._c)
        ops = [{"w": o["w"], "h": o["h"]} for o in detail["openings"]]
        # 系数 <= 0 时 estimate_room 抛 ValueError，先于落库 → 整单拒绝不写记录
        result = estimate_room(r["length"], r["width"], r["height"], ops, cov, ct,
                               damp=damp, damp_factor=factor)
        rid = runs.insert(self._c, "estimate",
            {"room_id": room_id, "coats": ct, "coverage": cov,
             "damp": result["damp"], "damp_factor": result["damp_factor"]},
            result, room_id) if persist else None
        return {"run_id": rid, "room_id": room_id, **result}
    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
