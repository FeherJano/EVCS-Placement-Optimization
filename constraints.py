import numpy as np
from typing import List, Dict, Tuple


def build_constraints(
        locations: List[str],
        participants: List[str],
        participant_interest: Dict[str, List[str]],
        bids: Dict[Tuple[str, int, Tuple[str, ...]], float],
        cost_components: Dict[str, float],
        coverage_constraints: List[Tuple[List[str], int]],
        complex_groups: List[Tuple[List[str], str]],
        z_vars: Dict[Tuple[str, int, Tuple[str, ...]], int],
        w_vars: Dict[str, int],
        total_vars: int
) -> Tuple[List[List[float]], List[float], List[List[float]], List[float]]:
    A = []
    b = []
    A_eq = []
    b_eq = []

    # --- Ajánlat elfogadási feltételek ---
    for (p, m, bundle) in bids:
        idx_z = z_vars[(p, m, bundle)]
        full_interest = set(participant_interest[p])
        bundle_set = set(bundle)

        row = [0.0] * total_vars
        row[idx_z] = len(full_interest)

        for loc in bundle_set:
            wk = f"w{loc[1:]}"
            if wk in w_vars:
                row[w_vars[wk]] -= 1.0

        for loc in full_interest - bundle_set:
            wk = f"w{loc[1:]}"
            if wk in w_vars:
                row[w_vars[wk]] += 1.0

        A.append(row)
        b.append(len(full_interest) - len(bundle))

    # --- Egy résztvevő legfeljebb egy ajánlatot nyerhet ---
    for p in participants:
        row = [0.0] * total_vars
        for (pp, m, bundle) in bids:
            if pp == p:
                row[z_vars[(pp, m, bundle)]] = 1.0
        A.append(row)  # nem A_eq
        b.append(1.0)  # max 1

    # --- Lefedettségi megszorítás ---
    for group, min_required in coverage_constraints:
        row = [0.0] * total_vars
        for loc in group:
            wk = f"w{loc[1:]}"  # <-- hibajavítás itt
            if wk in w_vars:
                row[w_vars[wk]] = -1.0
        A.append(row)
        b.append(-min_required)

    # --- Komplex költség komponens bekapcsolása ---
    for group_keys, trigger_key in complex_groups:
        row = [0.0] * total_vars
        for loc in group_keys:
            wk = f"w{loc[1:]}"
            if wk in w_vars:
                row[w_vars[wk]] = 1.0
        if trigger_key in w_vars:
            row[w_vars[trigger_key]] = -2.0
        A.append(row)
        b.append(1.0)


    #b = [1.0, 1.0, 0.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 0.0, -3, 1.0]

    return A_eq, b_eq, A, b