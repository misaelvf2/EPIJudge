import collections
import copy
import functools
from typing import List

from collections import namedtuple, deque

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

WHITE, BLACK = range(2)

Coordinate = collections.namedtuple("Coordinate", ("x", "y"))

Dfs_Result = namedtuple("Dfs_Result", ["found", "path"])


def search_maze_bfs(
    maze: List[List[int]], s: Coordinate, e: Coordinate
) -> List[Coordinate]:
    # Graph search with BFS.
    # The only tricky part in comparison to the DFS
    # approach is knowing how to build the path after finding
    # the goal.
    # To do that, we use a dictionary to keep track of predecessors.
    # Then it's just a matter of recursing down the predecessors until
    # we make it back to the start node.
    # Time: O(n * m), we potentially have to visit every node.
    # Space: O(n * m)
    directions = [(0, -1), (-1, 0), (0, +1), (+1, 0)]
    predecessors = {}
    queue = deque([s])

    found = False
    while queue and not found:
        current = queue.pop()
        for direction in directions:
            next = Coordinate(x=current.x + direction[0], y=current.y + direction[1])
            if next == e:
                predecessors[next] = current
                found = True
                break
            if can_move(maze, next):
                predecessors[next] = current
                maze[current.x][current.y] = BLACK
                queue.append(next)

    if not found:
        return []

    path = []
    current = e
    while current != s:
        path.append(current)
        current = predecessors[current]
    path.append(current)
    return list(reversed(path))


def search_maze_custom_type_dfs(
    maze: List[List[int]], s: Coordinate, e: Coordinate
) -> List[Coordinate]:
    # Graph search with DFS.
    # Keep recursing until we reach the end coordinate,
    # taking care to remain within bounds and to avoid
    # the black squares. Also keep track of visited squares
    # to avoid recursing infinitely.
    # Use a custom object to keep track of the path,
    # as well as simplify the type logic.
    # Time: O(n * m), where n = maze width and m = maze height.
    # We have to visit every node in the worst case.
    # Space: O(n * m), because we keep track of every visited node,
    # and we have to visit *all* nodes in the worst case.
    directions = [(0, -1), (-1, 0), (0, +1), (+1, 0)]

    def dfs(current: Coordinate) -> Dfs_Result:
        if current == e:
            return Dfs_Result(found=True, path=[current])
        maze[current.x][current.y] = BLACK
        for direction in directions:
            next = Coordinate(x=current.x + direction[0], y=current.y + direction[1])
            if can_move(maze, next):
                found, path = dfs(next)
                if found:
                    return Dfs_Result(found=True, path=path + [current])
        return Dfs_Result(found=False, path=None)

    found, path = dfs(s)
    return list(reversed(path)) if found else []


def can_move(maze: List[List[int]], cords: Coordinate) -> bool:
    if (
        0 <= cords.x < len(maze)
        and 0 <= cords.y < len(maze[cords.x])
        and maze[cords.x][cords.y] == WHITE
    ):
        return True
    return False


def path_element_is_feasible(maze, prev, cur):
    if not (
        (0 <= cur.x < len(maze))
        and (0 <= cur.y < len(maze[cur.x]))
        and maze[cur.x][cur.y] == WHITE
    ):
        return False
    return (
        cur == (prev.x + 1, prev.y)
        or cur == (prev.x - 1, prev.y)
        or cur == (prev.x, prev.y + 1)
        or cur == (prev.x, prev.y - 1)
    )


def search_maze_epi(
    maze: List[List[int]], s: Coordinate, e: Coordinate
) -> List[Coordinate]:
    # Uses DFS, but keeps track of the path differently.
    # This essentially uses a backtracking approach, optimistically
    # adding nodes to the path as soon as we recurse over them, and then
    # backtracking after it is guaranteed they do not lead to the goal.
    # They also express complexity in terms of the graph representation.
    # Time: O(|V| + |E|), same as DFS over any regular graph.
    # Space: O(|V| + |E|)

    # Perform DFS to find a feasible path.
    def search_maze_helper(cur):
        # Checks cur is within maze and is a white pixel.
        if not (
            0 <= cur.x < len(maze)
            and 0 <= cur.y < len(maze[cur.x])
            and maze[cur.x][cur.y] == WHITE
        ):
            return False
        path.append(cur)
        maze[cur.x][cur.y] = BLACK
        if cur == e:
            return True

        if any(
            map(
                search_maze_helper,
                map(
                    Coordinate,
                    (cur.x - 1, cur.x + 1, cur.x, cur.x),
                    (cur.y, cur.y, cur.y - 1, cur.y + 1),
                ),
            )
        ):
            return True
        # Cannot find path, remove the entry added in path.append(cur).
        del path[-1]
        return False

    path: List[Coordinate] = []
    search_maze_helper(s)
    return path


def _search_maze(
    maze: List[List[int]], s: Coordinate, e: Coordinate
) -> List[Coordinate]:
    # Same idea as the DFS from above, but we track the path
    # using mutable state in the outer function.
    # This simplifies the function signature on the inner dfs function,
    # and makes the code a bit nicer to look at.
    # Time: O(n * m)
    # Space: O(n * m)
    directions = [Coordinate(x, y) for (x, y) in [(0, -1), (-1, 0), (0, +1), (+1, 0)]]
    path = []

    def dfs(current: Coordinate) -> bool:
        if current == e:
            path.append(current)
            return True
        maze[current.x][current.y] = BLACK
        for direction in directions:
            ahead = Coordinate(x=current.x + direction.x, y=current.y + direction.y)
            if can_move(maze, ahead):
                found = dfs(ahead)
                if found:
                    path.append(current)
                    return True
        return False

    found = dfs(s)
    return list(reversed(path)) if found else []


@enable_executor_hook
def search_maze_wrapper(executor, maze, s, e):
    s = Coordinate(*s)
    e = Coordinate(*e)
    cp = copy.deepcopy(maze)

    path = executor.run(functools.partial(search_maze, cp, s, e))

    if not path:
        return s == e

    if path[0] != s or path[-1] != e:
        raise TestFailure("Path doesn't lay between start and end points")

    for i in range(1, len(path)):
        if not path_element_is_feasible(maze, path[i - 1], path[i]):
            raise TestFailure("Path contains invalid segments")

    return True


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "search_maze.py", "search_maze.tsv", search_maze_wrapper
        )
    )
