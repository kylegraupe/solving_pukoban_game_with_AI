import pandas as pd
from collections import deque

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

EMPTY = ' '
OBSTACLE = 'O'
ROBOT = 'R'
BOX = 'B'
STORAGE = 'S'

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

directions = [up, down, left, right]
actions = [1, 2, 3]


def parse_puzzle(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    grid = [list(line) for line in lines]
    robot = []
    boxes = []
    storages = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == ROBOT:
                robot.append((x, y))
            elif cell == BOX:
                boxes.append((x, y))
            elif cell == STORAGE:
                storages.append((x, y))

    return grid, robot, boxes, storages


def parse_grid(grid):

    robot = []
    boxes = []
    storages = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == ROBOT:
                robot.append((x, y))
            elif cell == BOX:
                boxes.append((x, y))
            elif cell == STORAGE:
                storages.append((x, y))

    return grid, robot, boxes, storages


def is_goal(boxes, storages):
    if set(storages) == set(boxes):
        return True
    return False


def adjacent_boxes(grid, robot_loc):
    adjacent_box_locations = []
    x, y = robot_loc

    for move in directions:
        new_x, new_y = x + move[0], y + move[1]

        # Check if the new position contains a box
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid) and grid[new_y][new_x] == BOX:
            adjacent_box_locations.append((new_x, new_y))

    return adjacent_box_locations


def is_valid_push(grid, robot_loc, box_loc, direction):

    if grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] == OBSTACLE:
        print('Invalid Push: Robot -> Obstacle')
        return False

    if grid[box_loc[1] + direction[1]][box_loc[0] + direction[0]] == OBSTACLE:
        print('Invalid Push: Box -> Obstacle')
        return False

    if grid[box_loc[1] + direction[1]][box_loc[0] + direction[0]] == BOX:
        print('Invalid Push: Box -> Box in Way')
        return False

    if grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] != BOX:
        print('Invalid Push: No Box in Direction')
        return False

    else:
        return True


def is_valid_pull(grid, robot_loc, box_loc, direction):
    if grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] == OBSTACLE:
        print('Invalid Pull: Robot -> Obstacle')
        return False

    if grid[robot_loc[1] - direction[1]][robot_loc[0] - direction[0]] != BOX:
        print('Invalid Pull: No Box To Pull')
        return False

    else:
        return True


def is_valid_move(grid, robot_loc, direction):
    if grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] == OBSTACLE or \
            grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] == BOX:
        print('Invalid Move: Robot -> Obstacle')
        return False

    else:
        return True


def push(grid, robot_pos, box_pos, direction):
    if is_valid_push(grid, robot_pos, box_pos, direction):
        x, y = robot_pos
        a, b = box_pos
        new_grid = [row[:] for row in grid]
        if new_grid[y + direction[1]][x + direction[0]] != OBSTACLE and \
                new_grid[b + direction[1]][a + direction[0]] != OBSTACLE:
            # Calculate the new positions after the push
            new_robot_pos = (x + direction[0], y + direction[1])
            new_box_x = a + direction[0]
            new_box_y = b + direction[1]

            # Check if the new position for the box is not an obstacle
            if 0 <= new_box_x < len(new_grid[0]) and 0 <= new_box_y < len(new_grid) and new_grid[new_box_y][new_box_x] != OBSTACLE:
                new_grid[new_box_y][new_box_x] = BOX
        else:
            # Handle the case where the new position for the box is an obstacle
            print('Invalid Push: Box -> Obstacle')
            return grid

        # Update the grid
        new_grid[y][x] = EMPTY
        new_grid[new_robot_pos[1]][new_robot_pos[0]] = ROBOT
        print('Valid Push')
        return new_grid
    else:
        print('Push Invalid')
        return grid


def pull(grid, robot_loc, box_loc, direction):
    if is_valid_pull(grid, robot_loc, box_loc, direction):

        x, y = robot_loc
        a, b = box_loc
        new_grid = [row[:] for row in grid]

        if new_grid[y + direction[1]][x + direction[0]] != OBSTACLE and \
            new_grid[b + direction[1]][a + direction[0]] != OBSTACLE:

            # Calculate the new positions after the pull
            new_robot_pos = (x + direction[0], y + direction[1])
            new_box_pos = (a + direction[0], b + direction[1])  # Corrected calculation for the new box position
            # Update the grid

            new_grid[y][x] = EMPTY
            new_grid[b][a] = EMPTY
            new_grid[new_robot_pos[1]][new_robot_pos[0]] = ROBOT
            new_grid[new_box_pos[1]][new_box_pos[0]] = BOX
            print('+Valid Pull')
            return new_grid
        else:
            print('-Invalid Pull')
            return grid
    else:
        print('=Invalid Pull')
        return grid


def move(grid, robot_loc, direction):
    if is_valid_move(grid, robot_loc, direction):
        x, y = robot_loc

        new_grid = [row[:] for row in grid]
        new_robot_pos = (x + direction[0], y + direction[1])

        new_grid[y][x] = EMPTY
        new_grid[new_robot_pos[1]][new_robot_pos[0]] = ROBOT
        print('Valid Vacant Move:')
        return new_grid
    else:
        print('Invalid Move')
        return grid


def check_successor(grid, robot_loc, box_loc, direction, action):
    if action == 1:
        if is_valid_move(grid, robot_loc, direction):
            return move(grid, robot_loc, direction)
    if action == 2:
        if is_valid_push(grid, robot_loc, box_loc, direction):
            return push(grid, robot_loc, box_loc, direction)
    if action == 3:
        if is_valid_pull(grid, robot_loc, box_loc, direction):
            return pull(grid, robot_loc, box_loc, direction)

    else:
        return None


def generate_successors(grid, robot, boxes):
    successors = []

    # for i in range(len(robot)):
    #     for j in directions:
    #         print(move)
    #         successor = check_successor(grid, robot[i], boxes, j)
    #         if successor:
    #             successors.append(successor)
    #
    # print(pd.DataFrame(successors))

    for i in range(len(robot)):
        for action in actions:
            for direction in directions:
                successor = check_successor(grid, robot[i], boxes, direction, action)
                if successor:
                    successors.append(successor)

    return successors


def bfs_2(start_df, test_storages):
    visited = set()  # Use a set for faster membership checking
    queue = deque([(start_df, [])])

    while queue:
        current_grid, path = queue.popleft()
        current_grid, current_robot, current_boxes, current_storages = parse_grid(current_grid)

        if is_goal(current_boxes, test_storages):
            print(f'Path: {path}')
            return path

        # Convert the current_df to a tuple of tuples for hashing
        current_state_tuple = tuple(map(tuple, current_grid))

        visited.add(current_state_tuple)

        for i in current_robot:
            for j in range(len(adjacent_boxes(current_grid, i))):
                for successor_df in generate_successors(current_grid, current_robot, current_boxes[j]):
                    successor_state_tuple = tuple(map(tuple, successor_df))

                    if successor_state_tuple not in visited:
                        queue.append((successor_df, path + [successor_df]))


    print('visited')
    print([pd.DataFrame(i) for i in visited])


def dfs(grid, robot, boxes, storages):
    # Check if the current state is a goal state
    if is_goal(boxes, storages):
        return []

    # Iterate over all possible moves
    for i, robot_pos in enumerate(robot):
        for direction in directions:
            successor = check_successor(grid, robot_pos, boxes, direction, actions[0])

            if successor:
                # Make a move
                new_grid, new_robot, new_boxes, _ = parse_grid(successor)

                # Recursively explore the new state
                path = dfs(new_grid, new_robot, new_boxes, storages)

                if path is not None:
                    return [successor] + path

    # No solution found from this state
    return None


def bfs_executive():
    puzzle_file = 'pukoban_medium.txt'
    grid, robot, boxes, storages = parse_puzzle(puzzle_file)

    # print(bfs_2(grid, storages))

    # print(dfs(grid, robot, boxes, storages))

    solution_path = bfs_2(grid, storages)
    print(solution_path)
    if solution_path:
        print("Solution found:")
        for step, state in enumerate(solution_path):
            grid = state
            print(f"Step {step + 1}:")
            for row in grid:
                print("".join(row))
            print("\n")
    else:
        print("No solution found.")

    # print(is_valid_pull(grid, robot[0], boxes[0], right))
    # print(is_valid_push(grid, robot[0], boxes[0], left))
    # print(is_valid_move(grid, robot[0], right))

    # adj = adjacent_boxes(grid, robot[0])
    # for i in adj:
    #     successors = generate_successors(grid, robot, i)
    #
    # print([pd.DataFrame(i) for i in successors])
    #
    # grid_1, robot_1, boxes_1, storages_1 = parse_grid(successors[1].values.tolist())
    # print(is_goal(successors[1].values.tolist(), boxes_1, storages))

    # grid_2 = pull(grid, robot[0], boxes[0], right)
    # print('\nasdf')
    # print(pd.DataFrame(grid_2))

    # grid_2, robot_2 = pull(grid_2, robot_2, boxes[0], right)
    # print('\nasdf')
    # print(pd.DataFrame(grid_2))
    # print(robot_2)
