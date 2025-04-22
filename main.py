from demo_big import (
    bids,
    cost_components,
    coverage_constraints,
    complex_groups,
    locations,
    participants,
    participant_interest,
    location_names,
    participant_info
)
from decision_variables import generate_variable_indices
from objective import build_objective_vector
from constraints import build_constraints
from solver import solve_model

# --- Döntési változók indexelése ---
z_vars, w_vars, total_vars = generate_variable_indices(bids, cost_components)

# --- Célfüggvény összeállítása ---
c = build_objective_vector(bids, cost_components)
print("Célfüggvény (c):", c)

# --- Megszorítások összeállítása ---
A_eq, b_eq, A_ub, b_ub = build_constraints(
    locations, participants, participant_interest,
    bids, cost_components, coverage_constraints,
     complex_groups, z_vars, w_vars, total_vars
)

# --- Optimalizálás ---
result = solve_model(c, A_eq, b_eq, A_ub, b_ub, total_vars)

#print(len(A_eq), len(A_ub), len(b_ub))

# --- Eredmények kiírása ---
print("\nOptimalizált célérték (max haszon):", -result.fun if result.success else "Hiba")

# Elfogadott ajánlatok (résztvevők és hozzájárulás)
print("\nElfogadott ajánlatok és résztvevői hozzájárulás:")
total_contribution = 0
for (p, m, bundle), idx in z_vars.items():
    if result.x[idx] > 0.5:
        name = participant_info[p][0]
        value = bids[(p, m, bundle)]
        total_contribution += value
        bundle_named = [location_names[loc] for loc in bundle]
        print(f"  {name} (ID: {p}) – ajánlat#{m}, helyszínek: {bundle_named}, érték: {value}M Ft")

# Aktivált költség komponensek – helyszínek
print("\nTöltőállomások telepítési helyei és költségei:")
total_cost = 0
for wk, idx in w_vars.items():
    if wk.startswith("w") and wk[1:].isdigit() and result.x[idx] > 0.5:
        loc_id = f"L{wk[1:]}"
        loc_name = location_names.get(loc_id, "Ismeretlen")
        cost = cost_components[wk]
        total_cost += cost
        print(f"  {loc_name} (ID: {loc_id}) – {cost}M Ft")

# Hálózati bővítés
print("\nHálózati bővítések (komplex költségek):")
network_mapping = {"w11": "1-es körzet", "w12": "2-es körzet", "w13": "3-as körzet"}
total_network = 0
for wk in ["w11", "w12", "w13"]:
    if wk in w_vars and result.x[w_vars[wk]] > 0.5:
        district = network_mapping[wk]
        cost = cost_components[wk]
        total_network += cost
        print(f"  {district} – hálózatbővítés költsége: {cost}M Ft")

# Összegzések
print(f"\nÖsszesített telepítési költség: {(total_cost)}M  Ft")
print(f"Résztvevői összes hozzájárulás: {total_contribution:.2f}M Ft")
actual_cost_millions = result.fun
print(f"Tényleges megvalósulás költsége: {actual_cost_millions:.2f} M Ft")
