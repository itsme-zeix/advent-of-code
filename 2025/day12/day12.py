from time import perf_counter_ns
from math import prod


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
) -> tuple[list[tuple[str, int]], list[tuple[str, list[int]]]] | None:
    try:
        with open(file_path, "r") as f:
            presents_and_regions = f.read().split("\n\n")
            presents: list[tuple[str, int]] = []  # present str, area
            regions: list[tuple[str, list[int]]] = []
            n = len(presents_and_regions)

            for i in range(n):
                # parse region data
                if i == (n - 1):
                    region_str_lines = presents_and_regions[i].strip().split("\n")
                    for r in region_str_lines:
                        region_id, present_counts = r.split(": ")
                        regions.append(
                            (region_id, [int(x) for x in present_counts.split(" ")])
                        )
                    continue

                # parse present data
                _, present_str = presents_and_regions[i].split(":\n")
                area = sum([1 if ch == "#" else 0 for ch in present_str])
                presents.append((present_str, area))

            return (presents, regions)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error: {e}")


@timeit
def part1(input: tuple[list[tuple[str, int]], list[tuple[str, list[int]]]]) -> str:
    presents, regions = input

    # Reject cases where there is definitely not enough area to fit all presents
    impossible_to_fit = 0
    for region_id, region_data in regions:
        region_area = prod(map(int, region_id.split("x")))

        total_present_area = sum(
            [
                presents[present_id][1] * count
                for present_id, count in enumerate(region_data)
            ]
        )

        if total_present_area > region_area:
            impossible_to_fit += 1

    # Accept cases where we can definitely fit all presents (sufficient 3x3 squares)
    definitely_fits = 0
    for region_id, region_data in regions:
        length, width = map(int, region_id.split("x"))

        squares_available = (length // 3) * (width // 3)
        squares_needed = sum(region_data)
        if squares_available >= squares_needed:
            definitely_fits += 1

    print(f"Total no. of regions: {len(regions)}")
    print(f"No. of regions that definitely fits all presents: {definitely_fits}")
    print(f"No. of regions that is impossible to fit all presents: {impossible_to_fit}")

    # Basically, the results above show that they gave a nice input where the regions either
    # trivially fits all presents or it is impossible to fit all the presents.
    # A real scenario would have a much more complex and slow solution.
    return "Check the above prinout for the solution!"


@timeit
def part2(input: tuple[list[tuple[str, int]], list[tuple[str, list[int]]]]) -> str:
    return "Done with AOC 2025!"


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
