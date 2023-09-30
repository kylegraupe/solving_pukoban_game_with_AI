import pandas as pd

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
    """
    This function takes in a text file as input and returns the Pukoban game puzzle
    :param file_path: Path to text file containing Pukoban game Grid
    :return: Game grid, robot locations, box locations, storage locations
    """

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
    """
    This function takes in a grid as an input to update robot, box, and storage locations.
    Used in the search algorithms.
    :param grid: Pukoban Game Grid
    :return: Pukoban Game Grid, robot locations, box locations, storage locations
    """

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
    """
    Tests to see if all boxes are in storage locations.
    :param boxes: List of tuples containing box locations
    :param storages: List of tuples containing storage locations
    :return: Boolean
    """

    if set(storages) == set(boxes):
        return True
    return False


def adjacent_boxes(grid, robot_loc):
    """
    This function returns the location of adjacent boxes to the robot input.
    :param grid: Pukoban Game Grid
    :param robot_loc: Location of a robot
    :return: Adjacent box locations
    """

    adjacent_box_locations = []
    x, y = robot_loc

    for move in directions:
        new_x, new_y = x + move[0], y + move[1]

        # Check if the new position contains a box
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid) and grid[new_y][new_x] == BOX:
            adjacent_box_locations.append((new_x, new_y))

    return adjacent_box_locations


def is_valid_push(grid, robot_loc, box_loc, direction):
    """
    This function checks to see if a push action is valid based on criteria.
    :param grid: Pukoban Game Grid
    :param robot_loc: Robot location
    :param box_loc: Box location
    :param direction: Direction of push
    :return: Boolean
    """
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
    """
    This function checks to see if a pull action is valid based on game criteria.
    :param grid: Pukoban Game Grid
    :param robot_loc: Robot location
    :param box_loc: Box location
    :param direction: Direction of pull
    :return: Boolean
    """
    if grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] == OBSTACLE:
        print('Invalid Pull: Robot -> Obstacle')
        return False

    if grid[robot_loc[1] - direction[1]][robot_loc[0] - direction[0]] != BOX:
        print('Invalid Pull: No Box To Pull')
        return False

    else:
        return True


def is_valid_move(grid, robot_loc, direction):
    """
    This function checks to see if a vacant move is valid. A vacant move is a robot moving to
    an empty space.
    :param grid: Pukoban Game Grid
    :param robot_loc: Robot location
    :param direction: Direction of move
    :return: Boolean
    """
    if grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] == OBSTACLE or \
            grid[robot_loc[1] + direction[1]][robot_loc[0] + direction[0]] == BOX:
        print('Invalid Move: Robot -> Obstacle')
        return False

    else:
        return True


def push(grid, robot_pos, box_pos, direction):
    """
    This function updates the game grid based on a valid push.
    :param grid: Pukoban Game Grid
    :param robot_pos: Robot location
    :param box_pos: Box location
    :param direction: Direction of push
    :return: Updated Pukoban Game Grid after valid push
    """
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
    """
    This function updates the Pukoban Game Grid based on a valid pull action.
    :param grid: Pukoban Game Grid
    :param robot_loc: Robot location
    :param box_loc: Box location
    :param direction: Direction of pull
    :return: Updated Pukoban Game Grid after valid pull
    """
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
    """
    This function updates the Pukoban Game Grid after a valid vacant move.
    :param grid: Pukoban Game Grid
    :param robot_loc: Robot location
    :param direction: Direction of move
    :return: Updated Pukoban Game Grid
    """
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
    """
    This function generates successor state game grids based on the action and direction given.
    :param grid: Pukoban Game Grid
    :param robot_loc: Robot location
    :param box_loc: Box location
    :param direction: Direction of action
    :param action: Action type (Push, Pull, Move)
    :return: Updates game grid based on action type.
    """
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
    """
    This function generates all successor states given an input state.
    :param grid: Pukoban Game Grid initial state
    :param robot: Robot location
    :param boxes: Box location
    :return: 2D list of successor states
    """
    successors = []

    for i in range(len(robot)):
        for action in actions:
            for direction in directions:
                successor = check_successor(grid, robot[i], boxes, direction, action)
                if successor:
                    successors.append(successor)

    return successors



