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
def read_input(file_path: str) -> list[str] | None:
    try:
        with open(file_path, "r") as f:
            return f.read().split()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@timeit
def part1(input: list[str]) -> int:
    # O(NM^2)
    res = 0
    for line in input:
        n = len(line)
        best = 0
        for i in range(n):
            for j in range(i + 1, n):
                cand = int(line[i] + line[j])
                best = max(best, cand)
        res += best
    return res


@timeit
def part2(input: list[str]) -> int:
    # O(NM)
    res = 0
    for line in input:
        leftover_chars = len(line)
        stack = []

        for ch in line:
            while leftover_chars > 12 and stack and stack[-1] < ch:
                stack.pop()
                leftover_chars -= 1
            stack.append(ch)

        curr = "".join(stack[:12])
        res += int(curr)
    return res


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
