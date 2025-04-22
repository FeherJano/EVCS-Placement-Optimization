from demo import bids, cost_components, coverage_constraints, complex_groups, locations, participants, participant_interest
from decision_variables import generate_variable_indices
from objective import build_objective_vector
from constraints import build_constraints
from solver import solve_model

# --- Változók indexelése ---
z_vars, w_vars, total_vars = generate_variable_indices(bids, cost_components)

# --- Célfüggvény ---
c = build_objective_vector(bids, cost_components)
print(c)

# --- Megszorítások ---
A_eq, b_eq, A_ub, b_ub = build_constraints(
    locations, participants, participant_interest,
    bids, cost_components, coverage_constraints,
    complex_groups, z_vars, w_vars, total_vars
)


print("A vektor: ")
for i in A_ub:
    print(i)

print("b vektor: ", b_ub)
print("A_eq vektor: ")
for i in A_eq:
    print(i)
print("b_eq vektor: ", b_eq)


# --- Optimalizáció ---
result = solve_model(c, A_eq, b_eq, A_ub, b_ub, total_vars)

# --- Eredmények ---
print("\nOptimalizált célérték (max haszon):", -result.fun if result.success else "Hiba")
print("\nAktív változók:")

for (p, m, bundle), idx in z_vars.items():
    if result.x[idx] > 0.5:
        print(f"Elfogadott ajánlat: résztvevő={p}, ajánlat#{m}, bundle={bundle}")

for wk, idx in w_vars.items():
    if result.x[idx] > 0.5:
        print(f"Költség aktiválva: {wk} (érték: {cost_components[wk]})")