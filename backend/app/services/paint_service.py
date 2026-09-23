from app.db import connect
from app.engines.estimate import estimate_room
from app.modules.wet_area import DEFAULT_WET_FACTOR
from app.repositories import openings, rooms, runs, settings

class WetFactorError(ValueError):
    """潮湿系数非法（<=0），整单拒绝。"""

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
    def settings(self): return settings.get_map(self._c)
    def set_setting(self, key, value): return settings.set_value(self._c, key, value)
    def set_room_wet(self, rid, wet): return rooms.set_wet(self._c, rid, wet)
    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def run_detail(self, run_id): return runs.get(self._c, run_id)
    def estimate(self, room_id, persist, coats=None, coverage=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings.coverage_coats(self._c)
        cov = float(coverage or cov)
        ct = int(coats or ct)
        wet = bool(r.get("wet", 0))
        # 潮湿区用设置页默认系数；非潮湿区系数缺省为 1，升数与改造前一致
        if wet:
            try:
                factor = settings.wet_factor(self._c)
            except (TypeError, ValueError):
                raise WetFactorError("wet factor must be a positive number")
        else:
            factor = DEFAULT_WET_FACTOR
        # 系数 <= 0 整单拒绝：先于任何写库操作，不产生 calc_runs 记录
        if factor <= 0:
            raise WetFactorError("wet factor must be positive")
        ops = [{"w": o["w"], "h": o["h"]} for o in detail["openings"]]
        result = estimate_room(r["length"], r["width"], r["height"], ops, cov, ct, wet, factor)
        # persist 时钉选：是否潮湿、所用系数、折算后净面积与升数随记录固化
        payload = {
            "room_id": room_id, "coats": ct, "coverage": cov,
            "wet": wet, "wet_factor": result["wet_factor"],
        }
        rid = runs.insert(self._c, "estimate", payload, result, room_id) if persist else None
        return {"run_id": rid, "room_id": room_id, **result}
    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
