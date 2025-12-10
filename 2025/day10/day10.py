from time import perf_counter_ns
from functools import cache
from scipy.optimize import linprog


def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start) / 1e6:.2f}ms")
        return res

    return wrap


@timeit
def read_input(
    file_path: str,
) -> list[tuple[int, list[int], list[int]]] | None:
    try:
        with open(file_path, "r") as f:
            res: list[tuple[int, list[int], list[int]]] = []
            for line in f:
                left, right = line.split("]")
                lights: int = 0
                for i, ch in enumerate(left[1:]):
                    if ch == "#":
                        lights |= 1 << i

                combos_str, joltages_str = right.split("{")
                combos: list[int] = [
                    sum(1 << int(idx) for idx in b_set_str.split(","))
                    for b_set_str in combos_str.replace("(", "")
                    .replace(")", "")
                    .strip()
                    .split(" ")
                ]
                joltages: list[int] = [
                    int(j) for j in joltages_str.strip()[:-1].split(",")
                ]

                res.append((lights, combos, joltages))

            return res

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def compute_fewest_button_presses(
    lights: int,
    combos: list[int],
    len_combos: int,
    combo_idx: int,
    presses: int,
    state: int,
) -> float:
    # every button set can be selected or not selected
    if state == lights:
        return presses  # no smaller answers are possible from this path onwards

    if combo_idx >= len_combos:
        return float("inf")

    pressed_state = state ^ combos[combo_idx]  # XOR

    a = compute_fewest_button_presses(
        lights, combos, len_combos, combo_idx + 1, presses + 1, pressed_state
    )
    b = compute_fewest_button_presses(
        lights, combos, len_combos, combo_idx + 1, presses, state
    )
    return min(a, b)


@timeit
def part1(input: list[tuple[int, list[int], list[int]]]) -> int:
    res = 0
    for lights, combos, _ in input:
        curr = compute_fewest_button_presses(lights, combos, len(combos), 0, 0, 0)
        res += curr if curr != float("inf") else 0
    return int(res)


@timeit
def part2(input: list[tuple[int, list[int], list[int]]]) -> int:
    """
    Brute force not feasible here, search space is massive.

    We can construct the problem as linear equations then solve it.

    For example, if we have:

        Button 0: (0, 2)
        Button 1: (0, 3)
        Joltage: {3, 0, 4, 7}

        We can form the following equations:
            Let x_i be the number of times button i is pressed
            Joltage 0: x_0 + x_1 = 3
            Joltage 1: 0
            Joltage 2: x_0 = 4
            Joltage 3: x_1 = 7
    """
    res = 0

    for _, combos, joltages in input:
        lhs: list[list[int]] = []  # list of [x0, x1, x2, ..., x_i]
        rhs: list[int] = []  # list of joltage solutions
        for i, jolt in enumerate(joltages):
            eqn: list[int] = [1 if combo & (1 << i) else 0 for combo in combos]
            lhs.append(eqn)
            rhs.append(jolt)

        to_minimize = [1] * len(combos)
        solution = linprog(to_minimize, A_eq=lhs, b_eq=rhs, integrality=1)
        res += sum(solution.x)

    return int(res)


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
