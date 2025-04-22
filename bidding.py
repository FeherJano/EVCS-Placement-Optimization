from itertools import combinations
from typing import Dict, List, Tuple

def map_population_to_bid(population: int, min_pop: int = 500, max_pop: int = 100000, min_bid: float = 1.0, max_bid: float = 20.0) -> float:
    """
    Lineáris skálázás a lakosságszámból licit értékre.
    """
    m = (max_bid - min_bid) / (max_pop - min_pop)
    b = min_bid - m * min_pop
    return m * population + b

def calculate_bid(participant_heur: Tuple[str, str, int], bundle_size: int) -> float:
    """
    Ajánlat érték számítása a résztvevő típusától és bundle méretétől függően.
    """
    _, participant_type, scale_value = participant_heur
    base_bid = map_population_to_bid(scale_value)

    if participant_type == 'o':  # önkormányzat
        bid = base_bid * (0.5 ** (bundle_size - 1))
    elif participant_type == 'v':  # vállalat
        bid = base_bid * (2.5 ** (bundle_size - 1))
    else:
        raise ValueError("Ismeretlen résztvevő típus: csak 'o' vagy 'v' lehet.")

    return round(bid, 2)


def generate_bids(
    participant_interests: Dict[str, List[str]],
    participant_heuristics: Dict[str, Tuple[str, str, int]]
) -> Dict[Tuple[str, int, Tuple[str, ...]], float]:
    """
    Résztvevő-alapú licit generálása:
    Visszatérési forma:
    {
        (P1, 1, ("L1",)): 1.2,
        (P1, 2, ("L1", "L2")): 0.8,
        ...
    }
    """
    all_bids = {}

    for participant, locations in participant_interests.items():
        heuristics = participant_heuristics[participant]
        bundle_index = 1

        for r in range(1, len(locations) + 1):
            for bundle in combinations(sorted(locations), r):
                bid_value = calculate_bid(heuristics, len(bundle))
                all_bids[(participant, bundle_index, bundle)] = bid_value
                bundle_index += 1

    return all_bids