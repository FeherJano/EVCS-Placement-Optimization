from demo_big import locations, participant_interest, bids, cost_components
from itertools import combinations

# Helyspecifikus költségek
y_cost_map = {loc: cost_components[f"w{loc[1:]}"] for loc in locations}

# Komplex költségek feltételei
complex_groups = [
    (["L1", "L2", "L3", "L4"], "w11"),
    (["L5", "L6", "L7"], "w12"),
    (["L8", "L9", "L10"], "w13"),
]

def is_complex_active(active_locs):
    active_set = set(active_locs)
    activated = []
    for group, w_key in complex_groups:
        if len(active_set.intersection(group)) >= 2:
            activated.append(w_key)
    return activated

print("--- RÉSZLETES ESETELEMZÉS (NAGY MODELL) ---\n")

for r in range(1, len(locations)+1):
    for combo in combinations(locations, r):
        active_set = set(combo)

        total_income = 0.0
        accepted_bids = []

        for p in participant_interest:
            interest_set = set(participant_interest[p])
            relevant_active = active_set.intersection(interest_set)

            best_bid = None
            best_value = -1

            for (pp, m, bundle), value in bids.items():
                if pp != p:
                    continue
                if set(bundle) == relevant_active:
                    if len(bundle) > len(best_bid[2]) if best_bid else -1:
                        best_bid = (pp, m, bundle, value)
                        best_value = value

            if best_bid:
                accepted_bids.append(best_bid)
                total_income += best_value

        # Költségek
        location_cost = sum(y_cost_map[loc] for loc in combo)
        active_complex_keys = is_complex_active(combo)
        extra_cost = sum(cost_components[k] for k in active_complex_keys)
        total_cost = location_cost + extra_cost

        profit = total_income - total_cost

        print(f"Aktív helyszínek: {combo}")
        print(f"  Bevételek összesen: {total_income}")
        for (p, m, bundle, value) in accepted_bids:
            print(f"    Elfogadott: {p} - ajánlat#{m} - {bundle} - érték: {value}")
        print(f"  Költség összesen: {total_cost} (helyszínek: {location_cost}, extra: {extra_cost})")
        print(f"  Nettó haszon: {profit}")
        print("-")