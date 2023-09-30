import heapq
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


def astar_search(grid, robot, boxes, storages):
    # Define a priority queue to store states based on the Manhattan Heuristic and path cost
    priority_queue = [(ManhattanHeuristic.manhattan_heuristic(boxes, storages), 0, grid, robot, boxes, [])]
    visited_states = set()

    while priority_queue:
        _, path_cost, current_grid, current_robot, current_boxes, path = heapq.heappop(priority_queue)

        if GenerateSuccessors.is_goal(current_boxes, storages):
            return path

        current_state_hash = (tuple(map(tuple, current_grid)), tuple(current_robot), tuple(current_boxes))
        if current_state_hash in visited_states:
            continue

        visited_states.add(current_state_hash)

        # Iterate over all possible moves
        for i, robot_pos in enumerate(current_robot):
            for direction in directions:
                successor = GenerateSuccessors.check_successor(current_grid, robot_pos, current_boxes, direction, actions[0])

                if successor:
                    # Make a move
                    new_grid, new_robot, new_boxes, _ = GenerateSuccessors.parse_grid(successor)

                    # Calculate the Manhattan Heuristic for the successor
                    heuristic = ManhattanHeuristic.manhattan_heuristic(new_boxes, storages)

                    # Add the successor state to the priority queue based on the heuristic and path cost
                    heapq.heappush(priority_queue, (heuristic + path_cost + 1, path_cost + 1, new_grid, new_robot, new_boxes, path + [successor]))

    # No solution found
    return None


def as_executive(file_name):
    start = datetime.datetime.now()

    grid, robot, boxes, storages = GenerateSuccessors.parse_puzzle(file_name)
    solution_path = astar_search(grid, robot, boxes, storages)

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

    print(f'A* Algorithm Runtime: {end - start}')