from time import monotonic_ns


def timeit(f):
    def wrap(*args, **kwargs):
        start = monotonic_ns()
        res = f(*args, **kwargs)
        end = monotonic_ns()
        print(f"Function {f.__name__} took {(end - start) / 1e6:.2f}ms")
        return res

    return wrap


@timeit
def read_input(file_path: str) -> list[tuple[int, int]] | None:
    try:
        with open(file_path, "r") as f:
            ranges: list[str] = f.read().split(",")
            return [
                (int(a), int(b))
                for a, b in (r.split("-", 1) for r in ranges if "-" in r)
            ]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def is_invalid(id_str: str, substr_len: int) -> bool:
    for i in range(substr_len, len(id_str)):
        if id_str[i] != id_str[i % substr_len]:
            return False
    return True


@timeit
def part1(input: list[tuple[int, int]]) -> int:
    res = 0

    # Brute force across range. Embarassingly parallel.
    for left, right in input:
        for id_int in range(left, right + 1):
            id_str = str(id_int)
            id_len = len(id_str)

            # odd no. of digits is always valid
            if id_len % 2 != 0:
                continue

            substr_len = id_len // 2
            if is_invalid(id_str, substr_len):
                res += id_int
                continue
    return res


def get_all_divisors(n: int) -> list[int]:
    divisors = []
    for i in range(1, int(n**0.5) + 1):  # circuitpython math module doesn't have isqrt
        if n % i != 0:
            continue

        divisors.append(i)

        # If i is not the square root, add the corresponding pair (n/i)
        if i * i != n:
            divisors.append(n // i)

    return divisors


@timeit
def part2(input: list[tuple[int, int]]) -> int:
    res = 0

    # Brute force again. Embarassingly parallel again.
    for left, right in input:
        for id_int in range(left, right + 1):
            id_str = str(id_int)
            id_len = len(id_str)

            # Only check divisors of id_len
            for substr_len in get_all_divisors(id_len):
                if is_invalid(id_str, substr_len):
                    res += id_int
                    break
    return res


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    # Sequential
    print(part1(input))
    print(part2(input))
