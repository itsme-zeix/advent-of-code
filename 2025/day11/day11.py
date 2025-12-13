from time import perf_counter_ns
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
def read_input(file_path: str) -> dict[str, list[str]] | None:
    try:
        with open(file_path, "r") as f:
            path_map: dict[str, list[str]] = {}
            lines = f.read().split("\n")
            for line in lines:
                if not line:
                    continue
                src, dsts = line.strip().split(":")
                path_map[src] = dsts.strip().split()
            return path_map

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error: {e}")


@timeit
def part1(path_map: dict[str, list[str]]) -> int:
    @cache
    def dfs(curr: str) -> int:
        if curr == "out":
            return 1
        res = 0
        for nxt in path_map.get(curr, []):
            res += dfs(nxt)
        return res

    return dfs("you")


@timeit
def part2(path_map: dict[str, list[str]]) -> int:
    @cache
    def dfs(curr: str, fft_found: bool, dac_found: bool) -> int:
        if curr == "out":
            return fft_found and dac_found

        res = 0
        for nxt in path_map.get(curr, []):
            res += dfs(nxt, fft_found or nxt == "fft", dac_found or nxt == "dac")
        return res

    return dfs("svr", False, False)


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
