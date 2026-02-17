from z3 import Bool, Bools, Or, And, Not, unsat
from z3 import Solver
from collections import deque
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

def plan_path(start, goal_set, known_safe, width, height):
    """BFS from start to any cell in goal_set, moving only through known_safe."""
    queue = deque([(start, [start])])
    seen = {start}
    while queue:
        (cx, cy), path = queue.popleft()
        if (cx, cy) in goal_set:
            return path
        for nx, ny in get_adjacent(cx, cy, width, height):
            if (nx, ny) not in seen and (nx, ny) in known_safe:
                seen.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None  # No path found

def turns_between(current, target):
    """Return the shortest sequence of turn actions from current to target direction."""
    if current == target:
        return []
    # Count steps in each direction and choose the shorter one.
    ...

