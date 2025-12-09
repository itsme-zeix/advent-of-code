from time import perf_counter_ns
from bisect import bisect_left, bisect_right


def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start) / 1e6:.2f}ms")
        return res

    return wrap


@timeit
def read_input(file_path: str) -> list[tuple[int, int]] | None:
    try:
        with open(file_path, "r") as f:
            out: list[tuple[int, int]] = []
            for line in f:
                a, b = map(int, line.split(",", 2))
                out.append((a, b))
            return out

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def compute_area(x1: int, y1: int, x2: int, y2: int) -> int:
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


@timeit
def part1(nodes: list[tuple[int, int]]) -> int:
    best = 0
    n = len(nodes)

    # Embarrasingly parallel
    for i in range(n):
        a1, b1 = nodes[i]
        for j in range(i + 1, n):
            a2, b2 = nodes[j]
            best = max(best, compute_area(a1, b1, a2, b2))
    return best


# def is_in_polygon(vert_edges: list[tuple[int, int, int]], x: int, y: int) -> bool:
#     # "Draw" a horizontal line on the right of the point and see if it intersects with an edge.
#     # Eliminate edges on the left of the point. Bisect_right to avoid the edge itself
#     start = bisect_right(vert_edges, x, key=lambda e: e[0])
#     intersects = 0
#     for _, y1, y2 in vert_edges[start:]:
#         if y1 < y < y2:
#             intersects += 1
#     return intersects % 2 == 1


def is_valid_rectangle(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    vert_edges: list[tuple[int, int, int]],
    hori_edges: list[tuple[int, int, int]],
    vert_x: list[int],
    hori_y: list[int],
) -> bool:
    # Check if points inside polygon (commented as already handled by the below edge checks)
    # if not is_in_polygon(vert_edges, x1, y2) or not is_in_polygon(vert_edges, x2, y1):
    #     return False

    # Check if edges intersect with polygon edges
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    min_x = min(x1, x2)
    max_x = max(x1, x2)

    # Horizontal polygon edge
    # strictly interior (as long as interior is overlapping, can return false)
    l_hori = bisect_right(hori_y, min_y)
    r_hori = bisect_left(hori_y, max_y)
    for i in range(l_hori, r_hori):
        _, ex1, ex2 = hori_edges[i]
        if ex1 < max_x and ex2 > min_x:
            return False

    # Vertical polygon edge
    l_vert = bisect_right(vert_x, min_x)
    r_vert = bisect_left(vert_x, max_x)
    for i in range(l_vert, r_vert):
        _, ey1, ey2 = vert_edges[i]
        if ey1 < max_y and ey2 > min_y:
            return False

    return True


@timeit
def part2(nodes: list[tuple[int, int]]) -> int:
    # We compute the rect's edges and check that they do not intersect with the polygon's edges.
    best = 0
    n = len(nodes)
    vert_edges: list[tuple[int, int, int]] = []  # x, min_y, max_y
    hori_edges: list[tuple[int, int, int]] = []  # y, min_x, max_x

    for i in range(n):
        x1, y1 = nodes[i]
        x2, y2 = nodes[(i + 1) % n]  # include the edge btwn first and last point
        if x1 == x2:
            vert_edges.append((x1, min(y1, y2), max(y1, y2)))
        else:  # y1 == y2
            hori_edges.append((y1, min(x1, x2), max(x1, x2)))

    vert_edges.sort()
    hori_edges.sort()
    vert_x = [e[0] for e in vert_edges]  # reduce lambda usage later (for speed)
    hori_y = [e[0] for e in hori_edges]

    for i in range(n):
        x1, y1 = nodes[i]
        for j in range(i + 1, n):
            x2, y2 = nodes[j]

            # Cheap computation to early exit if we can't beat the score
            area = compute_area(x1, y1, x2, y2)
            if area <= best:
                continue

            if is_valid_rectangle(
                x1, y1, x2, y2, vert_edges, hori_edges, vert_x, hori_y
            ):
                best = max(best, area)

    return best


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
