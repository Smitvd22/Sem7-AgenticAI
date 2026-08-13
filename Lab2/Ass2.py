import collections
import heapq

def find_start_goal(grid):
    start = goal = None
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'G':
                goal = (r, c)
    return start, goal

def get_neighbors(grid, r, c):
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] not in ('#', 'P'):
            neighbors.append((nr, nc))
    return neighbors

# ---------------------------------------------------------
# Base Algorithm: Breadth-First Search (BFS)
# ---------------------------------------------------------
def solve_bfs(grid, start_pos=None):
    start, goal = find_start_goal(grid)
    if start_pos:
        start = start_pos
        
    if not start or not goal:
        return None

    queue = collections.deque([(start, [])])
    visited = set([start])
    
    while queue:
        curr, path = queue.popleft()
        if curr == goal:
            return path
            
        r, c = curr
        for nr, nc in get_neighbors(grid, r, c):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return None

def execute_plan(grid, start, plan):
    print("Executing BFS plan...")
    curr = start
    for step in plan:
        print(f"Moving to {step}")
        curr = step
    if grid[curr[0]][curr[1]] == 'G':
        print("Goal reached successfully!")
    else:
        print("Plan failed.")

# ---------------------------------------------------------
# Exercise 1: Uniform Cost Search (UCS)
# ---------------------------------------------------------
def solve_ucs(grid, terrain_costs, start_pos=None):
    start, goal = find_start_goal(grid)
    if start_pos:
        start = start_pos
        
    if not start or not goal:
        return None
        
    pq = [(0, start, [])] 
    visited = {} 
    
    while pq:
        cost, curr, path = heapq.heappop(pq)
        
        if curr in visited and visited[curr] <= cost:
            continue
        visited[curr] = cost
        
        if curr == goal:
            return path
            
        r, c = curr
        for nr, nc in get_neighbors(grid, r, c):
            move_cost = terrain_costs[nr][nc]
            if (nr, nc) not in visited or visited[(nr, nc)] > cost + move_cost:
                heapq.heappush(pq, (cost + move_cost, (nr, nc), path + [(nr, nc)]))
    return None

# ---------------------------------------------------------
# Exercise 2: Re-planning on Failure
# ---------------------------------------------------------
def execute_with_replanning(grid, start):
    print("\n--- Exercise 2: Re-planning ---")
    grid_copy = [list(row) for row in grid]
    _, goal = find_start_goal(grid)
    curr = start
    
    plan = solve_bfs(grid_copy, curr)
    if not plan:
        print("No path to goal.")
        return
        
    print(f"Initial plan: {plan}")
    
    # Introduce an unexpected obstacle midway in the path to force replanning
    if len(plan) > 1:
        obstacle_pos = plan[1]
        print(f"[Simulating environment change] Blocking cell {obstacle_pos}")
        grid_copy[obstacle_pos[0]][obstacle_pos[1]] = '#'

    while curr != goal:
        # Check if the next step in our current plan is valid
        if not plan or grid_copy[plan[0][0]][plan[0][1]] == '#':
            print(f"Path blocked or empty at {curr}. Replanning...")
            plan = solve_bfs(grid_copy, curr)
            if not plan:
                print("Goal is unreachable due to new obstacles.")
                return
            print(f"New plan: {plan}")
            
        next_step = plan.pop(0)
        print(f"Moving to {next_step}")
        curr = next_step
        
    print("Goal reached successfully despite obstacles!")

# ---------------------------------------------------------
# Exercise 3: Hybrid Agent (Reactive + Deliberative)
# ---------------------------------------------------------
def solve_hybrid(grid):
    # Reactive rule: never step into a cell adjacent to a pit ('P')
    
    print("\n--- Exercise 3: Hybrid Agent ---")
    grid_safe = [list(row) for row in grid]
    
    # 1. Reactive filtering: Mark danger zones
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'P':
                # Mark adjacent cells as unsafe (treat as '#')
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid_safe[nr][nc] not in ('S', 'G', 'P', '#'):
                        grid_safe[nr][nc] = '#' # Block it
    
    # 2. Deliberative planning on the filtered safe grid
    plan = solve_bfs(grid_safe)
    if plan:
        print(f"Safe plan found: {plan}")
    else:
        print("No safe path found avoiding pits.")
    return plan

# ---------------------------------------------------------
# Main test block
# ---------------------------------------------------------
if __name__ == '__main__':
    world_grid = [
        ['S', '.', '.', '#', '.'],
        ['.', '#', '.', '#', '.'],
        ['.', '#', '.', '.', '.'],
        ['.', '.', '.', '#', 'G']
    ]
    
    print("--- Base Algorithm: BFS ---")
    start, _ = find_start_goal(world_grid)
    bfs_plan = solve_bfs(world_grid)
    print(f"BFS Plan: {bfs_plan}")
    if bfs_plan:
        execute_plan(world_grid, start, bfs_plan)

    print("\n--- Exercise 1: UCS ---")
    terrain = [
        [1, 1, 5, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 5, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    ucs_plan = solve_ucs(world_grid, terrain)
    print(f"UCS Plan: {ucs_plan}")

    execute_with_replanning(world_grid, start)
    
    world_grid_with_pits = [
        ['S', '.', '.', '.', '.'],
        ['.', 'P', '.', '#', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '#', '.', 'G']
    ]
    solve_hybrid(world_grid_with_pits)

# ---------------------------------------------------------
# Viva Questions Answers
# ---------------------------------------------------------
"""
1. Contrast reactive, deliberative and hybrid agent architectures.
Answer:
- Reactive agents make decisions solely based on the current percept (sense-act loop). They don't maintain an internal model or plan ahead, making them fast but incapable of long-term planning.
- Deliberative agents maintain an internal world model, plan a complete path to the goal by searching through possible states, and then execute the plan (sense-plan-act). They are good at long-term goals but slower and fail if the environment changes mid-plan.
- Hybrid agents combine both approaches. They use deliberative planning for long-term goals but have reactive rules to handle immediate hazards or dynamic changes, balancing efficiency and adaptability.

2. Why does BFS guarantee the shortest path here, and when would A* be preferred?
Answer:
- BFS guarantees the shortest path (in terms of number of steps) in an unweighted grid because it explores all nodes at the present depth before moving on to the nodes at the next depth level.
- A* would be preferred in larger grids or when the search space is huge, because A* uses a heuristic to guide the search towards the goal, expanding far fewer nodes than BFS while still guaranteeing an optimal path. It is also preferred when edges have varying costs.

3. What assumption of deliberative planning does re-planning address?
Answer:
- Deliberative planning assumes that the agent's internal model is perfectly accurate and that the world is static (does not change during plan execution). Re-planning addresses the breakdown of this assumption by allowing the agent to detect failures or dynamic obstacles during execution and compute a new plan from its current state.
"""

