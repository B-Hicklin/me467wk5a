from z3 import Bool, Bools, Or, And, Not, Solver, unsat
import hazardous_warehouse_env
import hazardous_warehouse_viz


P, Q = Bools('P Q')
s = Solver()
s.add(P == Q)    # Biconditional --- native, no CNF needed
s.add(P)
print(s.check())  # sat
print(s.model())   # [Q = True, P = True]

def z3_entails(solver, query):
    """Check whether the solver's current assertions entail query."""
    solver.push()
    solver.add(Not(query))
    result = solver.check() == unsat
    solver.pop()
    return result

print(z3_entails(s, Q))