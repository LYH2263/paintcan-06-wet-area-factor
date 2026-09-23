"""潮湿区系数模块。

房间标记为潮湿区后，墙面净面积先乘以潮湿系数（如卫浴 1.15），
再按涂布率换算升数。非潮湿区或系数缺省（1.0）时结果与无此模块一致。
"""

DEFAULT_WET_FACTOR = 1.0


def apply_wet_factor(net_m2: float, factor: float) -> dict:
    """净面积乘以潮湿系数，返回折算后净面积。系数必须为正。"""
    factor = float(factor)
    if factor <= 0:
        raise ValueError("wet factor must be positive")
    net_m2 = float(net_m2)
    if factor == 1.0:
        effective = net_m2
    else:
        effective = round(net_m2 * factor, 2)
    return {"effective_m2": effective, "wet_factor": factor}
