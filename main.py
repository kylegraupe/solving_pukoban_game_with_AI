import BFS  # Breadth First Search
import DFS  # Depth First Search
import GS  # Greedy Search
import AStar  # A* Search


def execute_application():
    """
    Use this function to run the desired search algorithm.

    Each algorithm has an executive function which will execute the search on the input text file.

    :return:
    """

    # UNCOMMENT THE SEARCH YOU WOULD LIKE TO RUN

    BFS.bfs_executive('pukoban_tiny.txt')
    # BFS.bfs_executive('pukoban_medium.txt')
    # BFS.bfs_executive('pukoban_large.txt')

    DFS.dfs_executive('pukoban_tiny.txt')
    # DFS.dfs_executive('pukoban_medium.txt')
    # DFS.dfs_executive('pukoban_large.txt')

    # GS.gs_executive('pukoban_tiny.txt')
    # GS.gs_executive('pukoban_medium.txt')
    # GS.gs_executive('pukoban_large.txt')

    AStar.as_executive('pukoban_tiny.txt')
    # AStar.as_executive('pukoban_medium.txt')
    # AStar.as_executive('pukoban_large.txt')


if __name__ == '__main__':
    execute_application()
