from bidding import generate_bids
# --- Helyszínek (ID + név) ---
location_names = {
    "L1": "Mártonvásári lehajtó",
    "L2": "Váli völgyi pihenő",
    "L3": "Pázmánd lehajtó",
    "L4": "Velencei-tó",
    "L5": "Pákozd pihenőhely",
    "L6": "Agárd M7-es kihajtó",
    "L7": "Székesfehérvár Alba ipari zóna",
    "L8": "Székesfehérvár Auchan",
    "L9": "Szabadbattyán lehajtó",
    "L10": "Polgárdi lehajtó"
}

# Résztvevők neve és mérete (önkormányzatok: lakosság, cégek: napi forgalom)
participant_info = {
    "P1": ("Tordas Önkormányzat", 'o', 2000),
    "P2": ("Kajászó Önkormányzat", 'o', 1000),
    "P3": ("Martonvásár Önkormányzat", 'o', 5500),
    "P4": ("Baracska Önkormányzat", 'o', 3000),
    "P5": ("Pázmánd Önkormányzat", 'o', 2400),
    "P6": ("Kápolnásnyék Önkormányzat", 'o', 3500),
    "P7": ("Nadap Önkormányzat", 'o', 800),
    "P8": ("Sukoró Önkormányzat", 'o', 1600),
    "P9": ("Velence Önkormányzat", 'o', 7000),
    "P10": ("Gárdony Önkormányzat", 'o', 9600),
    "P11": ("Pákozd Önkormányzat", 'o', 2800),
    "P12": ("Kisfalud Önkormányzat", 'o', 1500),
    "P13": ("Székesfehérvár Önkormányzat", 'o', 97000),
    "P14": ("Sárszentmihály Önkormányzat", 'o', 2100),
    "P15": ("Szabadbattyán Önkormányzat", 'o', 4300),
    "P16": ("Úrhida Önkormányzat", 'o', 1700),
    "P17": ("Tác Önkormányzat", 'o', 2100),
    "P18": ("Kőszárhegy Önkormányzat", 'o', 1200),
    "P19": ("Polgárdi Önkormányzat", 'o', 7000),
    "P20": ("Jenő Önkormányzat", 'o', 1600),
    "P21": ("Füle Önkormányzat", 'o', 1100),
    "P22": ("OMV", 'v', 2000),
    "P23": ("MOL", 'v', 3000),
    "P24": ("StopOil", 'v', 1200),
    "P25": ("Shell benzinkút", 'v', 2200),
    "P26": ("M7 Bistro", 'v', 1500),
    "P27": ("McDonald's", 'v', 3500),
    "P28": ("Auchan", 'v', 8000),
    "P29": ("Decathlon", 'v', 6000),
    "P30": ("KFC", 'v', 4000)
}


# Helyszínek listája
locations = [f"L{i}" for i in range(1, 11)]

# Résztvevők listája
participants = [f"P{i}" for i in range(1, 31)]

# Érdeklődési mátrix a táblázat alapján
interest_matrix = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # P1
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # P2
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # P3
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # P4
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # P5
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # P6
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # P7
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # P8
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # P9
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],  # P10
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # P11
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],  # P12
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],  # P13
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],  # P14
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # P15
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # P16
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # P17
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # P18
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # P19
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # P20
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # P21
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # P22
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1],  # P23
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # P24
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # P25
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # P26
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # P27
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # P28
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # P29
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],  # P30
]

# Résztvevők érdeklődése
participant_interest = {
    participants[i]: [locations[j] for j in range(10) if interest_matrix[i][j] == 1]
    for i in range(30)
}

# Költség-komponensek
cost_components = {
    "w1": 40,
    "w2": 15,
    "w3": 40,
    "w4": 80,
    "w5": 80,
    "w6": 80,
    "w7": 15,
    "w8": 15,
    "w9": 40,
    "w10": 40,
    "w11": 20,  # Komplex költség komponensek
    "w12": 30,
    "w13": 20
}

complex_groups = [
    (["L1", "L2", "L3", "L4"], "w11"),
    (["L5", "L6", "L7"], "w12"),
    (["L8", "L9", "L10"], "w13"),
]

# Lefedettségi csoport (az összes helyszínre egy minimális aktív helyszám)
coverage_constraints = [
    (["L1", "L2", "L3", "L4", "L5"], 1),
    (["L2", "L3", "L4", "L5", "L6"], 1),
    (["L3", "L4", "L5", "L6", "L7"], 1),
    (["L4", "L5", "L6", "L7", "L8"], 1),
    (["L5", "L6", "L7", "L8", "L9"], 1),
    (["L6", "L7", "L8", "L9", "L10"], 1),
]

# Lefedettségi csoport (az összes helyszínre egy minimális aktív helyszám)
coverage_constraints_fix_complex_cost = [
    (["L1", "L2", "L3", "L4", "L5"], 1),
    (["L2", "L3", "L4", "L5", "L6"], 1),
    (["L3", "L4", "L5", "L6", "L7"], 1),
    (["L4", "L5", "L6", "L7", "L8"], 1),
    (["L5", "L6", "L7", "L8", "L9"], 1),
    (["L6", "L7", "L8", "L9", "L10"], 1),
    (["L1", "L2", "L3"], 2),
    (["L5", "L6", "L7"], 2),
    (["L8", "L9", "L10"], 2)
]


bids = generate_bids(
    participant_interests=participant_interest,
    participant_heuristics=participant_info
)
