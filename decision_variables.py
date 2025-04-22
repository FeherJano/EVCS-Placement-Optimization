from typing import Dict, Tuple, List

def generate_variable_indices(bids: Dict[Tuple[str, int, Tuple[str, ...]], float], cost_components: Dict[str, float]):
    """
    Generálja az összes bináris döntési változó indexelését:
    z_j^m: ajánlat indikátor
    w_k: költség indikátor
    """
    sorted_bids = sorted(bids.items(), key=lambda x: (x[0][0], x[0][1]))
    z_vars = {bid_key: i for i, (bid_key, _) in enumerate(sorted_bids)}

    offset = len(z_vars)
    ordered_w = sorted(cost_components.keys(), key=lambda k: (int(k[1:]) if k[1:].isdigit() else float('inf')))
    w_vars = {wk: offset + i for i, wk in enumerate(ordered_w)}

    total_vars = len(z_vars) + len(w_vars)
    return z_vars, w_vars, total_vars
