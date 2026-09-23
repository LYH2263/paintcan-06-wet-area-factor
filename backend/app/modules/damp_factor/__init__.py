"""damp_factor: 潮湿区系数模块。

房间标记为潮湿区后，墙面净面积先乘本系数，再按涂布率换升数。
非潮湿区、或系数缺省/不可解析时按 1 处理（与未启用本模块一致）。
系数 <= 0 视为非法：抛 ValueError，由上层整单拒绝且不落库。
"""

DEFAULT_FACTOR = 1.0


def resolve_factor(damp, configured) -> float:
    """本次估漆实际使用的系数。非潮湿区恒为 1；缺省/非法文本回退 1。"""
    if not damp:
        return DEFAULT_FACTOR
    try:
        return float(configured)
    except (TypeError, ValueError):
        return DEFAULT_FACTOR


def adjust_net(net_m2: float, factor: float) -> float:
    """净面积折算。系数 <= 0 抛 ValueError（整单拒绝）。"""
    f = float(factor)
    if f <= 0:
        raise ValueError("damp factor must be positive")
    return round(float(net_m2) * f, 2)
