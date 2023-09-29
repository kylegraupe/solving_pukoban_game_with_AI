from collections import deque

# Define constants for grid elements
EMPTY = ' '
OBSTACLE = 'O'
ROBOT = 'R'
BOX = 'B'
STORAGE = 'S'


def parse_puzzle(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    grid = [list(line) for line in lines]
    robot = None
    boxes = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == ROBOT:
                robot = (x, y)
            elif cell == BOX:
                boxes.append((x, y))

    return grid, robot, boxes


def is_goal(grid, boxes):
    return all(grid[y][x] == STORAGE for x, y in boxes)


def is_valid_move(grid, x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid) and grid[y][x] != OBSTACLE


def get_successors(grid, robot, boxes):
    x, y = robot
    successors = []

    def is_valid_successor(dx, dy):
        new_x, new_y = x + dx, y + dy
        new_robot = (new_x, new_y)
        new_boxes = boxes[:]

        if (new_x, new_y) in new_boxes:
            box_index = new_boxes.index((new_x, new_y))
            new_box_x, new_box_y = new_x + dx, new_y + dy

            if is_valid_move(grid, new_box_x, new_box_y) and (new_box_x, new_box_y) not in new_boxes:
                new_boxes[box_index] = (new_box_x, new_box_y)
            else:
                return None

        if is_valid_move(grid, new_x, new_y):
            new_grid = [row[:] for row in grid]
            new_grid[y][x] = EMPTY
            new_grid[new_y][new_x] = ROBOT
            for bx, by in new_boxes:
                new_grid[by][bx] = BOX

            return new_grid, new_robot, new_boxes

        return None

    for dxdy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        successor = is_valid_successor(*dxdy)
        if successor:
            successors.append(successor)

    return successors


def bfs(initial_state):
    visited = set()
    queue = deque([initial_state])

    while queue:
        current_state = queue.popleft()
        grid, _, _ = current_state

        if is_goal(grid, current_state[2]):
            return grid

        visited.add(tuple(map(tuple, grid)))

        successors = get_successors(*current_state)
        for successor in successors:
            if tuple(map(tuple, successor[0])) not in visited:
                queue.append(successor)

    return None


def print_solution(solution_grid):
    for row in solution_grid:
        print("".join(row))


def execute_bfs(file_name):
    puzzle_file = file_name
    initial_state = parse_puzzle(puzzle_file)

    solution_grid = bfs(initial_state)

    if solution_grid:
        print("Solution found:")
        print_solution(solution_grid)
    else:
        print("No solution found.")
