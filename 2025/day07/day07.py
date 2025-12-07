from time import perf_counter_ns
from collections import deque
from functools import cache


def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start) / 1e6:.2f}ms")
        return res

    return wrap


@timeit
def read_input(file_path: str) -> str | None:
    try:
        with open(file_path, "r") as f:
            return f.read()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@timeit
def part1(input: str) -> int:
    grid = list(map(list, input.strip().split()))
    rows = len(grid)
    cols = len(grid[0])

    source = (0, 0)
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == "S":
                source = (x, y)
                break

    splits = 0
    beams = set([source[0]])

    for y in range(source[1] + 1, rows):
        next_beams: set[int] = set()

        for x in beams:
            if grid[y][x] == "^":
                splits += 1
                if x - 1 >= 0:
                    next_beams.add(x - 1)
                if x + 1 <= cols:
                    next_beams.add(x + 1)
            else:
                next_beams.add(x)

        beams = next_beams
        if not beams:
            break

    return splits


@timeit
def part2(input: str) -> int:
    grid = list(map(list, input.strip().split()))
    rows = len(grid)
    cols = len(grid[0])

    source = (0, 0)
    splitters: set[tuple[int, int]] = set()
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == "S":
                source = (x, y)
            elif grid[y][x] == "^":
                splitters.add((x, y))

    # At every split, there are 2 paths. We simply need to cache the number of paths at each
    # split and reuse our solution. We then propagate everything back up to the root.
    @cache
    def dfs(x: int, y: int) -> int:
        # reached the end
        if y >= rows:
            return 1

        # out of bounds
        if y < 0 or x < 0 or x >= cols:
            return 0

        if (x, y) in splitters:
            return dfs(x - 1, y) + dfs(x + 1, y)
        else:
            return dfs(x, y + 1)

    return dfs(source[0], source[1])


@timeit
def part2_dp(input: str) -> int:
    grid = list(map(list, input.strip().split()))
    rows = len(grid)
    cols = len(grid[0])

    source = (0, 0)
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == "S":
                source = (x, y)

    # Chuen Yang's DP solution!
    # DP, we propagate the number of paths down rather than propagate up with DFS
    dp = [[0] * cols for _ in range(rows)]
    dp[source[1]][source[0]] = 1

    for row in range(1, rows):
        for col in range(cols):
            dp[row][col] = dp[row - 1][col]

            # If there is a splitter at (row-1, col-1), it is the right split
            if col + 1 < cols and grid[row - 1][col + 1] == "^":
                dp[row][col] += dp[row - 1][col + 1]
            # If there is a splitter at (row-1, col+1), it is the left split
            if col - 1 >= 0 and grid[row - 1][col - 1] == "^":
                dp[row][col] += dp[row - 1][col - 1]
            # If there is a splitter at (row-1, col), no routes.
            if grid[row - 1][col] == "^":
                dp[row][col] = 0
    return sum(dp[rows - 1][col] for col in range(cols))


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
    print(part2_dp(input))
