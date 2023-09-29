import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

EMPTY = ' '
OBSTACLE = 'O'
ROBOT = 'R'
BOX = 'B'
STORAGE = 'S'
COMPLETE = 'C'

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

moves = [up, down, left, right]


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


def is_goal(grid, boxes):
    return all(grid[y][x] == STORAGE for x, y in boxes)


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
    if grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] == OBSTACLE:
        print('Invalid Pull: Robot -> Obstacle')
        return False

    else:
        return True


def push(grid, robot_pos, box_pos, direction):

    if is_valid_push(grid, robot_pos, box_pos, direction):
        x, y = robot_pos
        new_grid = [row[:] for row in grid]

        # Calculate the new positions after the push
        new_robot_pos = (x + direction[0], y + direction[1])
        new_box_pos = (x + 2 * direction[0], y + 2 * direction[1])

        # Update the grid
        new_grid[y][x] = EMPTY
        new_grid[new_robot_pos[1]][new_robot_pos[0]] = ROBOT
        new_grid[new_box_pos[1]][new_box_pos[0]] = BOX
        print('Valid Push')
        return new_grid

    else:
        print('Push Invalid')
        return grid


def pull(grid, robot_pos, box_pos, direction):
    if is_valid_pull(grid, robot_pos, box_pos, direction):
        x, y = robot_pos
        new_grid = [row[:] for row in grid]

        # Calculate the new positions after the push
        new_robot_pos = (x + direction[0], y + direction[1])
        new_box_pos = (x + direction[0] - 1, y + direction[1])

        # Update the grid
        new_grid[y][x] = EMPTY
        new_grid[box_pos[1]][box_pos[0]] = EMPTY
        new_grid[new_robot_pos[1]][new_robot_pos[0]] = ROBOT
        new_grid[new_box_pos[1]][new_box_pos[0]] = BOX
        print('Valid Pull')
        return new_grid
    else:
        print('Invalid Pull')
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


def check_successor(grid, robot_loc, box_loc, direction):
    if is_valid_move(grid, robot_loc, direction):
        return move(grid, robot_loc, direction)
    if is_valid_push(grid, robot_loc, box_loc, direction):
        return push(grid, robot_loc, box_loc, direction)
    if is_valid_pull(grid, robot_loc, box_loc, direction):
        return pull(grid, robot_loc, box_loc, direction)

    else:
        return None


def generate_successors(grid, robot, boxes):
    x, y = robot
    successors = []

    for move in moves:
        print(move)
        successor = check_successor(grid, robot, boxes, move)
        if successor:
            successors.append(successor)
            # print('asdf')
            # print(pd.DataFrame(successor))

    print(pd.DataFrame(successors))


def bfs_executive():
    grid, robot, boxes, storages = parse_puzzle('pukoban_tiny.txt')
    print(pd.DataFrame(grid))

    # print(is_valid_pull(grid, robot[0], boxes[0], right))
    # print(is_valid_push(grid, robot[0], boxes[0], left))
    # print(is_valid_move(grid, robot[0], right))

    generate_successors(grid, robot[0], boxes)
    # grid_2, robot_2 = pull(grid, robot[0], boxes[0], right)
    # print('\nasdf')
    # print(pd.DataFrame(grid_2))
    # print(robot_2)
    #
    # grid_2, robot_2 = pull(grid_2, robot_2, boxes[0], right)
    # print('\nasdf')
    # print(pd.DataFrame(grid_2))
    # print(robot_2)
