import datetime

import GenerateSuccessors

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


def is_cul_de_sac(grid, box_loc):
    """
    Check if a box location is in a cul-de-sac.
    :param grid: Pukoban Game Grid
    :param box_loc: Box location to be checked
    :return: True if the box is in a cul-de-sac, False otherwise
    """
    # Create a set to keep track of visited cells
    visited = set()

    def dfs(x, y):
        """
        Depth-first search to explore the area around the box location.
        :param x: x-coordinate
        :param y: y-coordinate
        :return: True if the box is in a cul-de-sac, False otherwise
        """
        # Base case: If the current cell is an obstacle or has already been visited, return False
        if (x, y) in visited or grid[y][x] == OBSTACLE:
            return False

        # Add the current cell to the visited set
        visited.add((x, y))

        # Check adjacent cells
        cul_de_sac = True
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy

            # If the adjacent cell is empty, it's not a cul-de-sac
            if grid[new_y][new_x] == EMPTY:
                cul_de_sac = False

            # If the adjacent cell is a box, recursively check if it's in a cul-de-sac
            elif grid[new_y][new_x] == BOX:
                cul_de_sac &= dfs(new_x, new_y)

        return cul_de_sac

    # Start DFS from the box location
    x, y = box_loc
    return dfs(x, y)


def generate_cul_de_sac_heuristic(grid, boxes):
    """
    Generate a cul-de-sac heuristic for the given puzzle state.
    :param grid: Pukoban Game Grid
    :param boxes: List of box locations
    :return: Cul-de-sac heuristic value
    """
    cul_de_sac_count = 0

    for box_loc in boxes:
        if is_cul_de_sac(grid, box_loc):
            cul_de_sac_count += 1

    return cul_de_sac_count


def cds_executive(file_name):
    start = datetime.datetime.now()

    grid, robot, boxes, storages = GenerateSuccessors.parse_puzzle(file_name)
    cds_heuristic = generate_cul_de_sac_heuristic(grid, boxes)

    print(cds_heuristic)

    end = datetime.datetime.now()

    print(f'A* Algorithm Runtime: {end - start}')