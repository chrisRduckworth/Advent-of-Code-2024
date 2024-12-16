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
    # The graph is actually more complicated than it looks
    # it is 4x bigger - each node can have a different direction
    # so to find all possible optimal paths we perform a BFS
    # and keep track of the shortes track to each node
    # and which nodes get it there via the shortest way

    width = len(maze[0])
    flattened = "".join(["".join(l) for l in maze])
    start = complex(*divmod(flattened.find("S"), width)[::-1])
    end = complex(*divmod(flattened.find("E"), width)[::-1])

    distances = {(start, 1): 0}
    parents = {}

    # if new score == distance, add it to the list of parents
    # if its less, update the score and replace the list

    queue = [(start, 1)]

    while len(queue) > 0:
        pos, dir = queue.pop()

        for dir_mult in [1, 1j, -1j]:
            new_dir = dir * dir_mult
            new_score = distances[(pos, dir)] + (1 if dir_mult == 1 else 1000)
            new_pos = -1
            if dir_mult == 1:
                # straight_ahead
                new_pos = pos + new_dir
            else:
                # turning
                new_pos = pos

            node = (new_pos, new_dir)

            if maze[int(node[0].imag)][int(node[0].real)] != "#":
                if node not in distances or new_score < distances[node]:
                    # unvisited, or a shorter route found
                    distances[node] = new_score
                    parents[node] = {(pos, dir)}
                    queue.append(node)
                elif new_score == distances[node]:
                    # same distance, so add to parents
                    parents[node].add((pos, dir))

    # to count the number of seats, turn every cell which is traveled to an O
    # and count those
    copy_maze = deepcopy(maze)

    def change_maze(node):
        x, y = int(node[0].real), int(node[0].imag)
        if node not in parents:
            # finished
            copy_maze[y][x] = "O"
            return
        for parent in parents[node]:
            p_x, p_y = int(parent[0].real), int(parent[0].imag)
            copy_maze[p_y][p_x] = "O"
            change_maze(parent)

    ends = [n for n in distances if n[0] == end]
    optimal_distance = min([distances[n] for n in ends])
    optimals = [n for n in ends if distances[n] == optimal_distance]

    for n in optimals:
        change_maze(n)

    return sum([l.count("O") for l in copy_maze]) + 1


if __name__ == "__main__":
    with open("inputs/day_16.txt") as f:
        input = f.readlines()
        maze = [list(l[:-1]) for l in input]
        lowest_score = find_lowest_score(maze)
        print(lowest_score, "< part 1")
        best_seats = find_best_seat(maze)
        print(best_seats, "< part 2")
