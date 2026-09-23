from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules.damp_factor import adjust_net, resolve_factor

def estimate_room(length, width, height, openings, coverage, coats, damp=False, damp_factor=None):
    area = wall_area(length, width, height, openings)
    factor = resolve_factor(damp, damp_factor)
    adj = adjust_net(area["net_m2"], factor)
    vol = paint_liters(adj, coverage, coats)
    return {**area, "damp": bool(damp), "damp_factor": factor, "adj_net_m2": adj, **vol}
