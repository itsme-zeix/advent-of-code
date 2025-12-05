from time import perf_counter_ns
from bisect import bisect_right


def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start) / 1e6:.2f}ms")
        return res

    return wrap


@timeit
def read_input(file_path: str) -> tuple[list[tuple[int, int]], list[int]] | None:
    try:
        with open(file_path, "r") as f:
            ranges_str, ids_str = f.read().split("\n\n", 1)
            ranges: list[tuple[int, int]] = []
            for r in ranges_str.split():
                start_str, end_str = r.split("-", 1)
                ranges.append((int(start_str), int(end_str)))
            ids = list(map(int, ids_str.split()))
            return ranges, ids
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def sort_and_merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    intervals.sort()
    new_intervals = [intervals[0]]
    for i in range(1, len(intervals)):
        l1, r1 = new_intervals[-1]
        l2, r2 = intervals[i]
        if r1 < l2:  # no overlap
            new_intervals.append(intervals[i])
        else:
            new_intervals[-1] = (l1, max(r1, r2))
    return new_intervals


@timeit
def part1(input: tuple[list[tuple[int, int]], list[int]]) -> int:
    intervals, ids = input
    intervals = sort_and_merge_intervals(intervals)

    res = 0
    starts = [a for a, _ in intervals]
    for id in ids:
        i = bisect_right(starts, id) - 1
        if i >= 0 and id <= intervals[i][1]:
            res += 1
    return res


@timeit
def part2(input: tuple[list[tuple[int, int]], list[int]]) -> int:
    intervals, _ = input
    intervals = sort_and_merge_intervals(intervals)

    res = 0
    for a, b in intervals:
        res += b - a + 1
    return res


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
