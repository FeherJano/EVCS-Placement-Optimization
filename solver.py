from scipy.optimize import linprog
import numpy as np

def solve_model(c, A_eq, b_eq, A_ub, b_ub, total_vars):
    ...

    """
    Megoldja az ILP feladatot (bináris változók), Highs módszerrel.
    """
    result = linprog(
        c=c,
        #A_eq=np.array(A_eq),
        #b_eq=np.array(b_eq),
        A_ub=np.array(A_ub),
        b_ub=np.array(b_ub),
        bounds=[(0, 1)] * total_vars,
        method="highs",
        integrality=np.ones(total_vars)
    )
    return result
