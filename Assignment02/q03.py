import time
from ortools.sat.python import cp_model

def read_puzzles(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if len(line.strip()) == 81]

puzzles = read_puzzles("sudoku_input.txt")

def print_solution(solution):
    for r in range(9):
        print(' '.join(str(solution[r * 9 + c]) for c in range(9)))
    print()

def string_to_grid(puzzle):
    return [[int(puzzle[r * 9 + c]) if puzzle[r * 9 + c] != '0' else 0 for c in range(9)] for r in range(9)]

# Backtracking + AC3
def cell_index(row, col):
    return row * 9 + col

def compute_peers():
    all_peers = [[] for _ in range(81)]
    for row in range(9):
        for col in range(9):
            idx = cell_index(row, col)
            row_peers = [cell_index(row, c) for c in range(9) if c != col]
            col_peers = [cell_index(r, col) for r in range(9) if r != row]
            block_row, block_col = row // 3 * 3, col // 3 * 3
            block_peers = [
                cell_index(block_row + r, block_col + c)
                for r in range(3) for c in range(3)
                if cell_index(block_row + r, block_col + c) != idx
            ]
            all_peers[idx] = list(set(row_peers + col_peers + block_peers))
    return all_peers

PEERS = compute_peers()

def ac3_algorithm(domains):
    arc_queue = [(var, peer) for var in range(81) for peer in PEERS[var]]
    while arc_queue:
        var_i, var_j = arc_queue.pop(0)
        if remove_inconsistent_values(domains, var_i, var_j):
            if not domains[var_i]:
                return False
            for var_k in PEERS[var_i]:
                if var_k != var_j:
                    arc_queue.append((var_k, var_i))
    return True

def remove_inconsistent_values(domains, var_i, var_j):
    changed = False
    current_domain = domains[var_i][:]
    for val in current_domain:
        if all(val == other_val for other_val in domains[var_j]):
            domains[var_i].remove(val)
            changed = True
    return changed

def backtrack_search(domains):
    if all(len(domains[i]) == 1 for i in range(81)):
        return [int(domains[i][0]) for i in range(81)]

    _, var = min((len(domains[i]), i) for i in range(81) if len(domains[i]) > 1)
    
    for candidate in domains[var]:
        copied_domains = [d[:] for d in domains]
        copied_domains[var] = [candidate]
        if ac3_algorithm(copied_domains):
            solution = backtrack_search(copied_domains)
            if solution:
                return solution
    return None

def solve_sudoku_ac3(puzzle_string):
    domain_list = [[c] if c in '123456789' else list('123456789') for c in puzzle_string]
    if not ac3_algorithm(domain_list):
        return None
    return backtrack_search(domain_list)

# OR Tools
def solve_sudoku_ortools(grid):
    model = cp_model.CpModel()
    cells = {}
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                cells[(i, j)] = model.NewIntVar(1, 9, f'cell_{i}_{j}')
            else:
                cells[(i, j)] = model.NewIntVar(grid[i][j], grid[i][j], f'cell_{i}_{j}')

    for i in range(9):
        model.AddAllDifferent([cells[(i, j)] for j in range(9)])
        model.AddAllDifferent([cells[(j, i)] for j in range(9)])

    for block_i in range(3):
        for block_j in range(3):
            block = [cells[(block_i * 3 + i, block_j * 3 + j)] for i in range(3) for j in range(3)]
            model.AddAllDifferent(block)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return [solver.Value(cells[(i, j)]) for i in range(9) for j in range(9)]
    return None

# GPT
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    block_r, block_c = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[block_r + i][block_c + j] == num:
                return False
    return True

def solve_sudoku_backtracking(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku_backtracking(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def flatten(board):
    return [cell for row in board for cell in row]

for idx, puzzle in enumerate(puzzles[:1]): 
    print(f"\n--- Puzzle #{idx + 1} ---")

    # 1. AC3 + Backtracking
    start = time.time()
    solution1 = solve_sudoku_ac3(puzzle)
    end = time.time()
    print(f"1. AC3+Backtracking Time: {end - start:.4f}s")
    print_solution(solution1)

    # 2. OR-Tools
    start = time.time()
    grid = string_to_grid(puzzle)
    solution2 = solve_sudoku_ortools(grid)
    end = time.time()
    print(f"2. OR-Tools Time: {end - start:.4f}s")
    print_solution(solution2)

    # 3. Classic Backtracking
    start = time.time()
    grid = string_to_grid(puzzle)
    solve_sudoku_backtracking(grid)
    solution3 = flatten(grid)
    end = time.time()
    print(f"3. Classic Backtracking Time: {end - start:.4f}s")
    print_solution(solution3)
