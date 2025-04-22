import numpy as np
from typing import Dict, Tuple, List

def build_objective_vector(
    bids: Dict[Tuple[str, int, Tuple[str, ...]], float],
    cost_components: Dict[str, float]
) -> np.ndarray:
    """
    Összeállítja a célfüggvény vektorát (haszon maximalizálás: I - C).
    Az LP megoldó minimalizál, ezért -I + C formában adjuk meg.
    Az indexelés: [z_1^1 ... z_n^m, w1, w2, ..., wk]
    """
    # Ajánlati bevételek (negatív előjellel)
    sorted_bids = sorted(bids.items(), key=lambda x: (x[0][0], x[0][1]))
    z_part = np.array([-value for (_, value) in sorted_bids])

    # Költségek (pozitív előjellel, cost_components sorrendje szerint)
    ordered_cost_keys = sorted(cost_components.keys(), key=lambda k: (int(k[1:]) if k[1:].isdigit() else float('inf')))
    w_part = np.array([cost_components.get(k, 0) for k in ordered_cost_keys])

    # Összefűzés
    c = np.concatenate([z_part, w_part])
    return c