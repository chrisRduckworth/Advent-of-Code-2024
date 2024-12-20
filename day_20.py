def create_route(maze):
    start, end = 0, 0
    for y, r in enumerate(maze):
        for x, c in enumerate(r):
            if c == "S":
                start = x + y * 1j
                maze[y][x] = "."
            elif c == "E":
                end = x + y * 1j
                maze[y][x] = "."

    prev = start
    dist = 0
    route = {}
    pos = 0

    for d in [1, -1, 1j, -1j]:
        pos = start + d
        if maze[int(pos.imag)][int(pos.real)] == ".":
            route[start] = 0
            break

    while pos != end:
        for d in [1, -1, 1j, -1j]:
            n_pos = pos + d
            if maze[int(n_pos.imag)][int(n_pos.real)] == "." and n_pos != prev:
                prev = pos
                pos = n_pos
                route[prev] = dist + 1
                dist += 1
                continue
    route[end] = dist + 1
    return route


def check_cheats(maze, route, threshold):
    # for each spot in the route, check the cells reachable throuhg a cheat
    # if you've moved forward by further than 2, it's a valid cheat
    cheats = []
    for pos in route:
        for d1 in [1, -1, 1j, -1j]:
            s_pos = pos + d1
            if maze[int(s_pos.imag)][int(s_pos.real)] == "#":
                for d2 in [1, -1, 1j, -1j]:
                    e_pos = s_pos + d2
                    if e_pos.imag < len(maze) and e_pos.real < len(maze[0]):
                        if maze[int(e_pos.imag)][int(e_pos.real)] == ".":
                            start_dist = route[pos]
                            end_dist = route[e_pos]
                            time_saved = end_dist - (start_dist + 2)
                            if time_saved > 0:
                                cheats.append(time_saved)

    return len([c for c in cheats if c >= threshold])


def part_1(maze):
    route = create_route(maze)
    no_cheats = check_cheats(maze, route, 100)
    return no_cheats


def check_cheats_20(maze, route, threshold):
    cheats = []
    # the cells reachable within 20 steps form a diamond
    # (i.e. taxicab distance)
    # so check each of those to see if it's faster
    width = len(maze[0])
    height = len(maze)
    for pos in route:
        for dy in range(-20, 21):
            for dx in range(abs(dy) - 20, 20 - abs(dy) + 1):
                new_pos = pos + dx + dy*1j
                if 0 <= new_pos.real < width and 0 <= new_pos.imag < height:
                    if maze[int(new_pos.imag)][int(new_pos.real)] == ".":
                        start_dist = route[pos]
                        end_dist = route[new_pos]
                        time_saved = end_dist - \
                            (start_dist + abs(dy) + abs(dx))
                        if time_saved >= threshold:
                            cheats.append(time_saved)
    return len(cheats)


def part_2(maze):
    route = create_route(maze)
    no_cheats = check_cheats_20(maze, route, 100)
    return no_cheats


if __name__ == "__main__":
    with open("inputs/day_20.txt") as f:
        input = f.readlines()
        maze = [list(l.replace("\n", "")) for l in input]
        cheats = part_1(maze)
        print(cheats, "< part 1")
        maze = [list(l.replace("\n", "")) for l in input]
        out = part_2(maze)
        print(out, "< part 2")
