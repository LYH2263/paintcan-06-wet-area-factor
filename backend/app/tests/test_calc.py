import os
import pytest
from app.engines.estimate import estimate_room
from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules.wet_area import apply_wet_factor

OPENINGS = [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}]

def test_living_room_net():
    a = wall_area(5, 4, 2.8, OPENINGS)
    assert a["gross_m2"] == 50.4
    assert a["net_m2"] == 46.41

def test_liters_two_coats():
    v = paint_liters(46.41, 8, 2)
    assert v["liters"] == 11.6

def test_estimate_combined():
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2)
    assert e["liters"] == 11.6

def test_bad_coverage():
    with pytest.raises(ValueError):
        paint_liters(10, 0, 2)

def test_non_wet_matches_baseline():
    # 非潮湿区：与改造前同房同参完全一致
    base = estimate_room(5, 4, 2.8, OPENINGS, 8, 2)
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2, wet=False, wet_factor=1.15)
    assert e["wet"] is False
    assert e["wet_factor"] == 1.0
    assert e["effective_m2"] == base["net_m2"]
    assert e["liters"] == base["liters"] == 11.6

def test_wet_factor_one_matches_baseline():
    # 潮湿区但系数缺省为 1：升数同样与改造前一致
    base = estimate_room(5, 4, 2.8, OPENINGS, 8, 2)
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2, wet=True, wet_factor=1.0)
    assert e["effective_m2"] == base["net_m2"]
    assert e["liters"] == base["liters"]

def test_wet_factor_scales_effective_area_and_liters():
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2, wet=True, wet_factor=1.1)
    # 46.41 * 1.1 = 51.051 -> 51.05
    assert e["effective_m2"] == 51.05
    # 51.05 * 2 / 8 = 12.7625 -> 12.76
    assert e["liters"] == 12.76

def test_wet_factor_must_be_positive():
    with pytest.raises(ValueError):
        apply_wet_factor(46.41, 0)
    with pytest.raises(ValueError):
        apply_wet_factor(46.41, -1)
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPENINGS, 8, 2, wet=True, wet_factor=0)


@pytest.fixture()
def service(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    from app import seed
    from app.services.paint_service import PaintService, WetFactorError
    seed.init_db()
    yield PaintService, WetFactorError

def test_persist_pins_factor_and_liters(service):
    PaintService, _ = service
    with PaintService() as s:
        s.set_setting("wet_factor", "1.1")
        assert s.set_room_wet(1, True)["wet"] == 1
        r = s.estimate(1, persist=True)
        run_id = r["run_id"]
        assert run_id is not None
        pinned = s.run_detail(run_id)
        # 钉选是否潮湿、所用系数、折算净面积、升数
        assert pinned["input"]["wet"] is True
        assert pinned["input"]["wet_factor"] == 1.1
        assert pinned["result"]["effective_m2"] == r["effective_m2"]
        assert pinned["result"]["liters"] == r["liters"]

def test_non_persist_returns_but_writes_nothing(service):
    PaintService, _ = service
    with PaintService() as s:
        before = len(s.history(100))
        r = s.estimate(1, persist=False)
        assert r["run_id"] is None
        assert len(s.history(100)) == before

def test_non_positive_factor_rejects_without_record(service):
    PaintService, WetFactorError = service
    with PaintService() as s:
        s.set_room_wet(1, True)
        s.set_setting("wet_factor", "0")
        before = len(s.history(100))
        with pytest.raises(WetFactorError):
            s.estimate(1, persist=True)
        # 整单拒绝且不写记录
        assert len(s.history(100)) == before

def test_changing_default_factor_keeps_old_runs(service):
    PaintService, _ = service
    with PaintService() as s:
        s.set_room_wet(1, True)
        s.set_setting("wet_factor", "1.1")
        old = s.estimate(1, persist=True)
        old_liters, old_factor = old["liters"], old["wet_factor"]
        # 改默认系数后，旧条升数不得跟着变
        s.set_setting("wet_factor", "1.3")
        pinned = s.run_detail(old["run_id"])
        assert pinned["input"]["wet_factor"] == old_factor == 1.1
        assert pinned["result"]["liters"] == old_liters
        # 新估算使用新系数
        new = s.estimate(1, persist=True)
        assert new["wet_factor"] == 1.3
        assert new["liters"] != old_liters
