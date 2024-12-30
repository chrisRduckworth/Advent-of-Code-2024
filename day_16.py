import heapq
import math
from copy import deepcopy


def find_lowest_score(maze):
    # classic application of Dijkstra's algorithm
    width = len(maze[0])
    height = len(maze)
    flattened = "".join(["".join(l) for l in maze])

    # using heapq here because it's super useful and makes life 100000 times easier
    # each entry in the heap is (score, index, direction)
    # have to use index as position because can't compare complex numbers
    heap = [(0, 1 + (height - 2) * height, 1)]
    distances = {1 + (height - 2) * height: 0}

    for i, c in enumerate(flattened):
        # give everything an infinite distance
        if c == "." or c == "E":
            distances[i] = math.inf

    visited = set()

    while len(visited) < len(distances):
        # grab the vertex with the lowest distance
        vertex = heapq.heappop(heap)
        score, pos, dir = vertex
        c_pos = complex(*divmod(pos, width)[::-1])
        for dir_mult in [1, 1j, -1j]:
            # don't need [-1] as we would never go backwards
            new_dir = dir * dir_mult
            new_pos = c_pos + new_dir
            index = int(new_pos.real + width * new_pos.imag)
            new_score = score + (1 if dir_mult == 1 else 1001)
            if index not in visited and flattened[index] != "#" and new_score < distances[index]:
                # we've found a shorter distance
                distances[index] = new_score
                heapq.heappush(heap, (new_score, index, new_dir))

        visited.add(pos)

    return distances[2 * width - 2]


def find_best_seat(maze):
    width = len(maze[0])
    height = len(maze)
    maze_d = {}
    for y, l in enumerate(maze):
        for x, c in enumerate(l):
            maze_d[x + 1j * y] = c

    start = [k for k, v in maze_d.items() if v == "S"][0]
    end = [k for k, v in maze_d.items() if v == "E"][0]

    distances = {}
    for p in maze_d:
        distances[(p, 1)] = math.inf
        distances[(p, -1)] = math.inf
        distances[(p, 1j)] = math.inf
        distances[(p, -1j)] = math.inf
    distances[(start, 1)] = 0

    parents = {}

    # use a djikstras but keep going until the we hit a distance greater than the distance to final node

    # have to represent directions as an integer for heapq
    i_dirs = {1: 1, -1: -1, 2: 1j, 3: -1j}
    rev_i_dirs = {1: 1, -1: -1, 1j: 2, -1j: 3}

    heap = [(0, int(start.real + start.imag * height), 1)]

    while True:
        score, index, i_dir = heapq.heappop(heap)

        if score > min(distances[(end, 1)], distances[(end, -1)], distances[(end, 1j)], distances[(end, -1j)]):
            # we've gone further than the fastest route, so are done searching
            break

        dir = i_dirs[i_dir]
        pos = complex(*divmod(index, width)[::-1])

        # go to surrounding nodes
        for dir_mult in [1, 1j, -1j]:
            new_dir = dir * dir_mult
            new_score = score + (1 if dir_mult == 1 else 1000)
            new_pos = -1
            if dir_mult == 1:
                # go straight
                new_pos = pos + new_dir
            else:
                # turn
                new_pos = pos

            if maze_d[new_pos] != "#":
                if new_score < distances[(new_pos, new_dir)]:
                    # shorter route found
                    # update distance
                    distances[(new_pos, new_dir)] = new_score
                    # replace parents
                    parents[(new_pos, new_dir)] = {(pos, dir)}
                    i_new_pos = int(new_pos.real + new_pos.imag * width)
                    i_new_dir = rev_i_dirs[new_dir]
                    # add to queue
                    heapq.heappush(heap, (new_score, i_new_pos, i_new_dir))
                elif new_score == distances[(new_pos, new_dir)]:
                    # same distance, add to parents
                    parents[(new_pos, new_dir)].add((pos, dir))

    ends = [n for n in distances if n[0] == end]
    optimal_distance = min([distances[n] for n in ends])
    optimals = [n for n in ends if distances[n] == optimal_distance]

    def change_maze(node):
        if node not in parents:
            # finished
            maze_d[node[0]] = "O"
            return
        for parent in parents[node]:
            maze_d[parent[0]] = "O"
            change_maze(parent)

    for n in optimals:
        change_maze(n)

    return len({d for d, v in maze_d.items() if v == "O" or v == "E"})


if __name__ == "__main__":
    with open("inputs/day_16.txt") as f:
        input = f.readlines()
        maze = [list(l[:-1]) for l in input]
        lowest_score = find_lowest_score(maze)
        print(lowest_score, "< part 1")
        best_seats = find_best_seat(maze)
        print(best_seats, "< part 2",)
