
def manhattan_heuristic(boxes, storages):
    """
    Calculates the Manhattan distance heuristic between boxes and storage locations.
    :param boxes: List of box locations
    :param storages: List of storage locations
    :return: Manhattan distance heuristic value
    """
    heuristic = 0

    for box in boxes:
        min_distance = float('inf')

        for storage in storages:
            distance = abs(box[0] - storage[0]) + abs(box[1] - storage[1])
            min_distance = min(min_distance, distance)

        heuristic += min_distance

    return heuristic
