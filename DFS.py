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


def dfs(initial_state):
    visited = set()
    stack = [(initial_state, [])]

    while stack:
        current_state, path = stack.pop()
        grid, _, _ = current_state

        if is_goal(grid, current_state[2]):
            return path

        visited.add(tuple(map(tuple, grid)))

        successors = get_successors(*current_state)
        for successor in successors:
            if tuple(map(tuple, successor[0])) not in visited:
                stack.append((successor, path + [successor]))
            print(current_state)
    return None


def print_solution(solution_path, initial_grid):
    grid = [row[:] for row in initial_grid]

    for state in solution_path:
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == ROBOT:
                    robot_x, robot_y = x, y
                    grid[y][x] = EMPTY

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == BOX:
                    box_x, box_y = x, y

        grid[robot_y][robot_x] = ROBOT
        grid[box_y][box_x] = BOX

        for row in grid:
            print("".join(row))
        print("\n")


def execute_dfs(file_name):  # Replace 'pukoban.txt' with the path to your puzzle file
    puzzle_file = file_name
    initial_grid, initial_robot, initial_boxes = parse_puzzle(puzzle_file)
    initial_state = (initial_grid, initial_robot, initial_boxes)

    solution_path = dfs(initial_state)

    if solution_path:
        print("Solution found:")
        print_solution(solution_path, initial_grid)
    else:
        print("No solution found.")
