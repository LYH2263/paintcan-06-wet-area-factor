from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules.wet_area import DEFAULT_WET_FACTOR, apply_wet_factor

def estimate_room(length, width, height, openings, coverage, coats,
                  wet=False, wet_factor=DEFAULT_WET_FACTOR):
    area = wall_area(length, width, height, openings)
    wet = bool(wet)
    # 非潮湿区不乘系数（按 1.0 处理），保证与无此模块时同房同参结果一致
    factor = float(wet_factor) if wet else DEFAULT_WET_FACTOR
    adjusted = apply_wet_factor(area["net_m2"], factor)
    vol = paint_liters(adjusted["effective_m2"], coverage, coats)
    return {
        **area,
        "wet": wet,
        "wet_factor": adjusted["wet_factor"],
        "effective_m2": adjusted["effective_m2"],
        **vol,
    }
