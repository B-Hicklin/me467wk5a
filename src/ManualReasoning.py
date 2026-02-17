from z3 import Bool, Bools, Or, And, Not, unsat
from z3 import Solver
import hazardous_warehouse_env
import hazardous_warehouse_viz

def z3_entails(solver, query):
    """Check whether the solver's current assertions entail query."""
    solver.push()
    solver.add(Not(query))
    result = solver.check() == unsat
    solver.pop()
    return result

def damaged(x, y):
    return Bool(f'D_{x}_{y}')
def forklift_at(x, y):
    return Bool(f'F_{x}_{y}')
def creaking_at(x, y):
    return Bool(f'C_{x}_{y}')
def rumbling_at(x, y):
    return Bool(f'R_{x}_{y}')
def safe(x, y):
    return Bool(f'S_{x}_{y}')

def get_adjacent(x, y, width=4, height=4):
    result = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 1 <= nx <= width and 1 <= ny <= height:
            result.append((nx, ny))
    return result

def build_warehouse_kb(width=4, height=4):
    solver = Solver()
    # The starting square is safe.
    solver.add(Not(damaged(1, 1)))
    solver.add(Not(forklift_at(1, 1)))
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            adj = get_adjacent(x, y, width, height)
            # Creaking iff damaged adjacent
            solver.add(creaking_at(x, y) == Or([damaged(a, b) for a, b in adj]))
            # Rumbling iff forklift adjacent
            solver.add(rumbling_at(x, y) == Or([forklift_at(a, b) for a, b in adj]))
            # Safety rule
            solver.add(
                safe(x, y) == And(Not(damaged(x, y)), Not(forklift_at(x, y)))
            )
    return solver

def tell_percepts(solver, percept, x, y):
    """TELL the solver the percepts observed at (x, y)."""
    if percept.creaking:
        solver.add(creaking_at(x, y))
    else:
        solver.add(Not(creaking_at(x, y)))
    if percept.rumbling:
        solver.add(rumbling_at(x, y))
    else:
        solver.add(Not(rumbling_at(x, y)))

kb = build_warehouse_kb()

tell_percepts(kb, 
hazardous_warehouse_env.Percept(creaking=False, rumbling=False, beacon=False, bump=False, beep=False),
1, 1)

print(z3_entails(kb, safe(1, 1)))
print(z3_entails(kb, safe(2, 1)))
print(z3_entails(kb, safe(1, 2)))

tell_percepts(kb, 
hazardous_warehouse_env.Percept(creaking=True, rumbling=False, beacon=False, bump=False, beep=False),
2, 1)

print(f"safe(3,1): {z3_entails(kb, safe(3, 1))}")
print(f"not safe(3,1): {z3_entails(kb, Not(safe(3, 1)))}")
print(f"safe(2,2): {z3_entails(kb, safe(2, 2))}")

tell_percepts(kb, 
hazardous_warehouse_env.Percept(creaking=False, rumbling=True, beacon=False, bump=False, beep=False),
1, 2)

print(f"safe(2,2): {z3_entails(kb, safe(2, 2))}")
print(f"safe(3,1): {z3_entails(kb, safe(3, 1))}")
print(f"not safe(3,1): {z3_entails(kb, Not(safe(3, 1)))}")
print(f"safe(1,3): {z3_entails(kb, safe(1, 3))}")
print(f"not safe(1,3): {z3_entails(kb, Not(safe(1, 3)))}")