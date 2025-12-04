from typing import Optional
from time import perf_counter_ns


def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start) / 1e6:.2f}ms")
        return res

    return wrap


@timeit
def read_input(file_path) -> Optional[list[str]]:
    try:
        with open(file_path, "r") as f:
            return f.read().split()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@timeit
def part1(grid: list[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])

    accessible = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != "@":
                continue

            # count adjacent
            count = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if (
                        not (di == 0 and dj == 0)
                        and 0 <= i + di < rows
                        and 0 <= j + dj < cols
                        and grid[i + di][j + dj] == "@"
                    ):
                        count += 1

            if count < 4:
                accessible += 1

    return accessible


@timeit
def part2(grid: list[str]) -> int:
    # Use set instead for speed
    occupied = set()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "@":
                occupied.add((i, j))
    initial_size = len(occupied)

    needs_rescan = True
    while needs_rescan:
        needs_rescan = False
        for i, j in deepcopy(occupied):
            count = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if not (di == 0 and dj == 0) and (i + di, j + dj) in occupied:
                        count += 1
            if count < 4:
                occupied.remove((i, j))
                needs_rescan = True

    return initial_size - len(occupied)


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
