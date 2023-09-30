from collections import deque
import pandas as pd
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


def bfs_2(start_df, test_storages):
    """
    This function is my attempt at implementing the Breadth First Search (BFS) algorithm.
    :param start_df: Initial game grid
    :param test_storages: Storage locations for game completion.
    :return: Path of successful game completion or None
    """

    visited = set()  # Use a set for faster membership checking
    queue = deque([(start_df, [])])

    while queue:
        current_grid, path = queue.popleft()
        current_grid, current_robot, current_boxes, current_storages = GenerateSuccessors.parse_grid(current_grid)

        if GenerateSuccessors.is_goal(current_boxes, test_storages):
            print(f'Path: {path}')
            return path

        # Convert the current_df to a tuple of tuples for hashing
        current_state_tuple = tuple(map(tuple, current_grid))

        visited.add(current_state_tuple)

        for i in current_robot:
            for j in range(len(GenerateSuccessors.adjacent_boxes(current_grid, i))):
                for successor_df in GenerateSuccessors.generate_successors(current_grid, current_robot, current_boxes[j]):
                    successor_state_tuple = tuple(map(tuple, successor_df))

                    if successor_state_tuple not in visited:
                        queue.append((successor_df, path + [successor_df]))

        print("Manhattan Distance Check:")
        print(ManhattanHeuristic.manhattan_heuristic(current_boxes, current_storages))


    print('visited')
    print([pd.DataFrame(i) for i in visited])


def bfs_executive(file_name):
    """
    Breadth First Search executive to be called in main.py
    :param file_name: Path to text file containing Pukoban Game Grid
    :return: None
    """

    start = datetime.datetime.now()

    puzzle_file = file_name
    grid, robot, boxes, storages = GenerateSuccessors.parse_puzzle(puzzle_file)

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

    end = datetime.datetime.now()

    print(f'BFS Algorithm Runtime: {end - start}')

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