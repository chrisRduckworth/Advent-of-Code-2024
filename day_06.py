def create_dict(input):
    out = {}
    for y, l in enumerate(input):
        for x, c in enumerate(l):
            out[x + 1j * y] = c
    return out


def find_path(map):
    start = [k for k, v in map.items() if v == "^"][0]
    dir = -1j
    pos = start
    path = []
    while pos in map:
        if pos+dir in map and map[pos + dir] == "#":
            # turn
            dir *= 1j
        else:
            path.append((pos, dir))
            pos += dir
    return path


def part_1(input):
    map = create_dict(input)
    path = find_path(map)
    return len(set(s[0] for s in path))


def find_loops(map, path):
    # for each point on the path, replace it with an obstacle
    # and check if it has created a loop
    loops = set()
    path_t = {p[0]: len(path) - 1 - i for i, p in enumerate(reversed(path))}

    for pos, index in path_t.items():
        original_val = map[pos]
        map[pos] = "#"

        visited = set(path[:index])
        is_loop = False
        n_pos, n_dir = path[index - 1]

        while True:
            next_pos = n_pos + n_dir
            if next_pos not in map:
                # we've left, so no loop
                break
            elif map[next_pos] == "#":
                # turn
                n_dir *= 1j
            else:
                # straight forward
                n_pos = next_pos

            if (n_pos, n_dir) in visited:
                # found a loop
                is_loop = True
                break

            visited.add((n_pos, n_dir))

        if is_loop:
            # since each point on the path can be approached
            # from multiple direction, we use a set only including
            # the position
            loops.add(pos)

        map[pos] = original_val

    return loops


def part_2(input):
    map = create_dict(input)
    path = find_path(map)
    loops = find_loops(map, path)
    return len(loops)


if __name__ == "__main__":
    with open("inputs/day_06.txt") as f:
        input = [l.strip() for l in f.readlines()]
        positions = part_1(input)
        print(positions, "< part 1")
        loop_count = part_2(input)
        print(loop_count, "< part 2")
