import pytest
from app.engines.estimate import estimate_room
from app.modules.damp_factor import adjust_net, resolve_factor

OPS = [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}]  # 客厅开洞，净面积 46.41

def test_non_damp_ignores_factor():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2, damp=False, damp_factor=1.5)
    assert e["damp"] is False
    assert e["damp_factor"] == 1.0
    assert e["adj_net_m2"] == 46.41
    assert e["liters"] == 11.6  # 与改造前同房同参一致

def test_damp_default_factor_keeps_base_numbers():
    for missing in (None, "abc", "1"):
        e = estimate_room(5, 4, 2.8, OPS, 8, 2, damp=True, damp_factor=missing)
        assert e["damp_factor"] == 1.0
        assert e["adj_net_m2"] == 46.41
        assert e["liters"] == 11.6

def test_damp_factor_applied_before_coverage():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2, damp=True, damp_factor="1.5")
    assert e["damp"] is True
    assert e["damp_factor"] == 1.5
    assert e["adj_net_m2"] == round(46.41 * 1.5, 2)
    assert e["liters"] == round(round(46.41 * 1.5, 2) * 2 / 8, 2)

def test_damp_factor_two_exact():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2, damp=True, damp_factor=2)
    assert e["adj_net_m2"] == 92.82
    assert e["liters"] == round(92.82 * 2 / 8, 2)

@pytest.mark.parametrize("bad", [0, -0.5, "0", "-2"])
def test_nonpositive_factor_rejected(bad):
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPS, 8, 2, damp=True, damp_factor=bad)

def test_nonpositive_factor_ok_when_not_damp():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2, damp=False, damp_factor=0)
    assert e["liters"] == 11.6

def test_resolve_factor():
    assert resolve_factor(False, "1.3") == 1.0
    assert resolve_factor(True, None) == 1.0
    assert resolve_factor(True, "1.3") == 1.3

def test_adjust_net_rejects_nonpositive():
    with pytest.raises(ValueError):
        adjust_net(10, 0)
