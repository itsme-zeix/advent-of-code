from time import perf_counter_ns
from collections import Counter
from math import prod
import numpy as np

"""
# Without numpy:
# python3.14 free threaded:
part1: 476.56ms
part2: 468.12ms

# pypy3
part1: 664.71ms
part2: 674.41ms

---

# With numpy for vectorized edge calculations:
# python3.14 free threaded
part1: 54.28ms
part2: 53.66ms
"""


def timeit(f):
    def wrap(*args, **kwargs):
        start = perf_counter_ns()
        res = f(*args, **kwargs)
        end = perf_counter_ns()
        print(f"Function {f.__name__} took {(end - start) / 1e6:.2f}ms")
        return res

    return wrap


@timeit
def read_input(file_path: str) -> list[tuple[int, int, int]] | None:
    try:
        with open(file_path, "r") as f:
            out: list[tuple[int, int, int]] = []
            for line in f:
                a, b, c = map(int, line.split(",", 2))
                out.append((a, b, c))
            return out

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_sorted_edges(nodes: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    edges: list[tuple[int, int, int]] = []  # (distance, id1, id2)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            dx = nodes[i][0] - nodes[j][0]
            dy = nodes[i][1] - nodes[j][1]
            dz = nodes[i][2] - nodes[j][2]
            distance = dx**2 + dy**2 + dz**2
            edges.append((distance, i, j))
    edges.sort()
    return edges


def get_sorted_edges_numpy(nodes: list[tuple[int, int, int]]) -> np.ndarray:
    coords = np.array(nodes)
    n = len(nodes)

    i_idx, j_idx = np.triu_indices(n, k=1)

    diff = coords[i_idx] - coords[j_idx]
    distances = np.einsum("ij,ij->i", diff, diff)

    order = np.argsort(distances)
    return np.column_stack((distances[order], i_idx[order], j_idx[order]))


def find_parent(circuits: list[int], x: int) -> int:
    # path compression
    if circuits[x] != x:
        circuits[x] = find_parent(circuits, circuits[x])
    return circuits[x]


@timeit
def part1(nodes: list[tuple[int, int, int]]) -> int:
    # pretty easy, we could get dist of every coordinate from each other, sort, then go through
    # them. union find to map to set/parent.
    edges = get_sorted_edges_numpy(nodes)  # (distance, id1, id2)
    circuits = list(range(len(nodes)))

    for _, id1, id2 in edges[:1000]:
        parent1, parent2 = find_parent(circuits, id1), find_parent(circuits, id2)

        # already in the same circuit
        if parent1 == parent2:
            continue

        # smaller parent represents circuit
        if parent1 < parent2:
            circuits[parent2] = parent1
        else:
            circuits[parent1] = parent2

    roots = [find_parent(circuits, i) for i in range(len(nodes))]
    count = Counter(roots)
    largest_three = sorted(count.values(), reverse=True)[:3]
    return prod(largest_three)


@timeit
def part2(nodes: list[tuple[int, int, int]]) -> int:
    edges = get_sorted_edges_numpy(nodes)  # (distance, id1, id2)
    circuits = list(range(len(nodes)))
    num_components = len(nodes)
    last_two_id = (0, 0)

    for _, id1, id2 in edges:
        parent1, parent2 = find_parent(circuits, id1), find_parent(circuits, id2)

        # already in the same circuit
        if parent1 == parent2:
            continue

        # smaller parent represents circuit
        num_components -= 1
        last_two_id = (id1, id2)
        if parent1 < parent2:
            circuits[parent2] = parent1
        else:
            circuits[parent1] = parent2

        if num_components == 1:
            break

    x_coords = [nodes[id][0] for id in last_two_id]
    return prod(x_coords)


if __name__ == "__main__":
    input = read_input("input.txt")
    assert input

    print(part1(input))
    print(part2(input))
