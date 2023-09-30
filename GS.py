import heapq


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


def greedy_search(grid, robot, boxes, storages):
    # Define a priority queue to store states based on the Manhattan Heuristic
    priority_queue = [(ManhattanHeuristic.manhattan_heuristic(boxes, storages), grid, robot, boxes, [])]

    while priority_queue:
        _, current_grid, current_robot, current_boxes, path = heapq.heappop(priority_queue)

        if GenerateSuccessors.is_goal(current_boxes, storages):
            return path

        # Iterate over all possible moves
        for i, robot_pos in enumerate(current_robot):
            for direction in directions:
                successor = GenerateSuccessors.check_successor(current_grid, robot_pos, current_boxes, direction, actions[0])

                if successor:
                    # Make a move
                    new_grid, new_robot, new_boxes, _ = GenerateSuccessors.parse_grid(successor)

                    # Calculate the Manhattan Heuristic for the successor
                    heuristic = ManhattanHeuristic.manhattan_heuristic(new_boxes, storages)

                    # Add the successor state to the priority queue based on the heuristic
                    heapq.heappush(priority_queue, (heuristic, new_grid, new_robot, new_boxes, path + [successor]))

    # No solution found
    return None


def gs_executive(puzzle_file):
    grid, robot, boxes, storages = GenerateSuccessors.parse_puzzle(puzzle_file)
    solution_path = greedy_search(grid, robot, boxes, storages)

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


