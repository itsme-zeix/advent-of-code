from time import perf_counter_ns


def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start) / 1000000:.2f}ms")
        return res

    return wrap


@timeit
def read_input(file_path: str) -> list[tuple[str, int]] | None:
    try:
        with open(file_path, "r") as f:
            lines = f.read().split()
            return [(op[0], int(op[1:])) for op in lines]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@timeit
def part1(input: list[tuple[str, int]]) -> int:
    state = 50
    res = 0

    for dir, dist in input:
        if dir == "L":
            state = (state - dist) % 100
        elif dir == "R":
            state = (state + dist) % 100

        if state == 0:
            res += 1

    return res


@timeit
def part2(input: list[tuple[str, int]]) -> int:
    state = 50
    res = 0

    for dir, dist in input:
        full_rotations = dist // 100
        dist %= 100
        res += full_rotations

        if dir == "L":
            if state > 0 and dist >= state:
                res += 1
            state = (state - dist) % 100
        elif dir == "R":
            if state > 0 and dist >= (100 - state):
                res += 1
            state = (state + dist) % 100

    return res


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input
    print(f"part 1: {part1(input)}")
    print(f"part 2: {part2(input)}")
