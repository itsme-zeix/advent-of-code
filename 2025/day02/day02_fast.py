from time import monotonic_ns
from math import isqrt


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


@timeit
def part1(input: list[tuple[int, int]]) -> int:
    total_sum = 0

    # Instead of iterating through every number, we generate periodic ones.
    # A number of length L is periodic with period S = L/2 if it's a multiple of M = 10^S + 1.
    for range_start, range_end in input:
        min_digits = len(str(range_start))
        max_digits = len(str(range_end))

        for num_digits in range(min_digits, max_digits + 1):
            if num_digits % 2 != 0:
                continue
            seed_length = num_digits // 2
            multiplier = 10**seed_length + 1

            # Find range of seeds such that range_start <= seed * multiplier <= range_end
            # and the resulting number has exactly num_digits.
            valid_min = max(range_start, 10 ** (num_digits - 1))
            valid_max = min(range_end, 10**num_digits - 1)

            seed_start = (valid_min + multiplier - 1) // multiplier
            seed_end = valid_max // multiplier

            for seed in range(seed_start, seed_end + 1):
                total_sum += seed * multiplier

    return total_sum


def get_all_divisors(n: int) -> list[int]:
    divisors = []
    for i in range(1, isqrt(n) + 1):
        if n % i != 0:
            continue

        divisors.append(i)

        # If i is not the square root, add the corresponding pair (n/i)
        if i * i != n:
            divisors.append(n // i)

    return divisors


@timeit
def part2(input: list[tuple[int, int]]) -> int:
    total_sum = 0

    # Generate periodic numbers for all divisors seed_length < num_digits.
    for range_start, range_end in input:
        periodic_in_range = set()
        min_digits = len(str(range_start))
        max_digits = len(str(range_end))

        for num_digits in range(min_digits, max_digits + 1):
            divisors = get_all_divisors(num_digits)
            for seed_length in divisors:
                if seed_length == num_digits:
                    continue

                # Multiplier for period seed_length and length num_digits
                multiplier = (10**num_digits - 1) // (10**seed_length - 1)

                valid_min = max(range_start, 10 ** (num_digits - 1))
                valid_max = min(range_end, 10**num_digits - 1)

                seed_start = (valid_min + multiplier - 1) // multiplier
                seed_end = valid_max // multiplier

                for seed in range(seed_start, seed_end + 1):
                    periodic_in_range.add(seed * multiplier)

        total_sum += sum(periodic_in_range)

    return total_sum


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    # Sequential
    print(part1(input))
    print(part2(input))
