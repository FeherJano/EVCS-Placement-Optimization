# --- DEMO MODELL: 3 HELYSZÍN, 2 SZEREPLŐ, KONKRÉT ÉRTÉKEKKEL ---

# Helyszínek listája
locations = ["L1", "L2", "L3"]

# Résztvevők listája
participants = ["P1", "P2"]

# Résztvevők érdeklődése (mely helyszínek érdeklik őket)
participant_interest = {
    "P1": ["L1", "L2"],
    "P2": ["L1", "L2", "L3"]
}

# Minden résztvevő által tett ajánlat, a hozzá tartozó helyszínkombinációval és értékével
# Formátum: (résztvevő, ajánlat index, bundle helyszínek) → ajánlati érték
bids = {
    ("P1", 1, ("L1",)): 1.6,
    ("P1", 2, ("L2",)): 1.6,
    ("P1", 3, ("L1", "L2")): 0.8,

    ("P2", 1, ("L1",)): 1.2,
    ("P2", 2, ("L2",)): 1.2,
    ("P2", 3, ("L3",)): 1.2,
    ("P2", 4, ("L1", "L2")): 0.6,
    ("P2", 5, ("L1", "L3")): 3.6,
    ("P2", 6, ("L2", "L3")): 0.6,
    ("P2", 7, ("L1", "L2", "L3")): 0.3,
}

# Költség-komponensek: költség ID → költség értéke (MFt)
cost_components = {
    "w1": 40,  # L1
    "w2": 15,  # L2
    "w3": 40,  # L3
    "w4": 20   # hálózatbővítés ha legalább 2 hely aktív
}

complex_groups = [
    (["L1", "L2", "L3"], "w4")
]

# Lefedettségi csoportok (pl. hálózati csoport): minden csoport egy lista helyszínekkel, és minimum aktív darabszám
coverage_constraints = [
    (["L1", "L2", "L3"], 2)
]

# Másodlagos költségkomponens feltétele (pl. w4 aktiválódik ha legalább 2 hely aktív L1-L2-L3 közül)
def secondary_cost_trigger(active_y_vars):
    return (sum(active_y_vars[loc] for loc in ["L1", "L2", "L3"]) - 1.5) / 2
