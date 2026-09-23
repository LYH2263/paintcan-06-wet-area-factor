import pytest
from app import seed
from app.services.paint_service import PaintService

@pytest.fixture()
def svc(tmp_path, monkeypatch):
    monkeypatch.setattr("app.db.DB_PATH", tmp_path / "t.db")
    seed.init_db()
    with PaintService() as s:
        yield s

def test_persist_pins_damp_factor_area_liters(svc):
    svc.update_setting("damp_factor", "1.5")
    svc.set_damp(1, True)
    r = svc.estimate(1, True)
    assert r["run_id"]
    assert r["damp"] is True and r["damp_factor"] == 1.5
    d = svc.run_detail(r["run_id"])
    assert d["result"]["damp"] is True
    assert d["result"]["damp_factor"] == 1.5
    assert d["result"]["adj_net_m2"] == r["adj_net_m2"]
    assert d["result"]["liters"] == r["liters"]

def test_default_factor_change_keeps_old_runs(svc):
    svc.update_setting("damp_factor", "1.5")
    svc.set_damp(1, True)
    rid = svc.estimate(1, True)["run_id"]
    before = svc.run_detail(rid)["result"]
    svc.update_setting("damp_factor", "2.5")
    after = svc.run_detail(rid)["result"]
    assert after["liters"] == before["liters"]
    assert after["damp_factor"] == 1.5

def test_nonpositive_factor_rejects_and_writes_nothing(svc):
    svc.set_damp(1, True)
    svc.update_setting("damp_factor", "0")
    n = len(svc.history())
    with pytest.raises(ValueError):
        svc.estimate(1, True)
    assert len(svc.history()) == n

def test_persist_false_writes_nothing(svc):
    svc.set_damp(1, True)
    svc.update_setting("damp_factor", "1.5")
    n = len(svc.history())
    r = svc.estimate(1, False)
    assert r["run_id"] is None
    assert r["damp_factor"] == 1.5
    assert len(svc.history()) == n

def test_set_damp_unknown_room(svc):
    assert svc.set_damp(999, True) is None

def test_run_detail_unknown(svc):
    assert svc.run_detail(999) is None
