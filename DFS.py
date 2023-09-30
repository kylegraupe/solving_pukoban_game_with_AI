import datetime

import GenerateSuccessors
import ManhattanHeuristic


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


# def dfs_3(grid, robot, boxes, storages):
#     stack = [(grid, robot, boxes, [])]
#
#     while stack:
#         current_grid, current_robot, current_boxes, path = stack.pop()
#
#         if GenerateSuccessors.is_goal(current_boxes, storages):
#             return path
#
#         # Iterate over all possible moves
#         for i, robot_pos in enumerate(current_robot):
#             for direction in directions:
#                 successor = GenerateSuccessors.check_successor(current_grid, robot_pos, current_boxes, direction, actions[0])
#
#                 if successor:
#                     # Make a move
#                     new_grid, new_robot, new_boxes, _ = GenerateSuccessors.parse_grid(successor)
#
#                     # Add the new state to the stack
#                     stack.append((new_grid, new_robot, new_boxes, path + [successor]))
#
#         print('Manhattan Distance Check:')
#         print(ManhattanHeuristic.manhattan_heuristic(new_boxes, storages))
#     # No solution found from this state
#     return None

def dfs_depth_limited(grid, robot, boxes, storages, max_depth):
    """
    This function is my attempt at implementing the DFS algorithm with a depth limit for recursion.
    :param grid: Pukoban Game Grid
    :param robot: Robot locations
    :param boxes: Box locations
    :param storages: Storage locations
    :param max_depth: Max recursion depth
    :return: Solution path or None
    """
    stack = [(grid, robot, boxes, [])]

    while stack:
        current_grid, current_robot, current_boxes, path = stack.pop()

        if GenerateSuccessors.is_goal(current_boxes, storages):
            return path

        # Check if the maximum depth has been reached
        if len(path) >= max_depth:
            continue

        # Iterate over all possible moves
        for i, robot_pos in enumerate(current_robot):
            for direction in directions:
                successor = GenerateSuccessors.check_successor(current_grid, robot_pos, current_boxes, direction, actions[0])

                if successor:
                    # Make a move
                    new_grid, new_robot, new_boxes, _ = GenerateSuccessors.parse_grid(successor)

                    # Add the new state to the stack
                    stack.append((new_grid, new_robot, new_boxes, path + [successor]))

        print('Manhattan Distance Check:')
        print(ManhattanHeuristic.manhattan_heuristic(current_boxes, storages))

    # No solution found within the depth limit
    return None


def dfs_executive(file_path):
    """
    Executes DFS algorithm
    :param file_path: Pukoban Game Grid text file.
    :return: Terminal output
    """

    start = datetime.datetime.now()

    # Parse the puzzle from the file
    grid, robot, boxes, storages = GenerateSuccessors.parse_puzzle(file_path)

    # Call the DFS function with the initial state
    solution_path = dfs_depth_limited(grid, robot, boxes, storages, 5)

    if solution_path:
        print("Solution Found:")
        for step, state in enumerate(solution_path):
            print(f"Step {step + 1}:")
            for row in state:
                print("".join(row))
            print("\n")

        print(f"Total Steps: {len(solution_path) - 1}")
    else:
        print("No solution found.")

    end = datetime.datetime.now()

    print(f'DFS Algorithm Runtime: {end - start}')