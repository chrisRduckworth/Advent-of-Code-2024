def create_grid(size):
    grid = [["#"] * (size + 2), ["#"] * (size + 2)]
    for i in range(size):
        grid.insert(1, ["#", *["."] * size, "#"])
    return grid


def add_obstructions(grid, obs):
    for x, y in obs:
        grid[y + 1][x + 1] = "#"


def calc_steps(grid):
    height = len(grid)
    width = len(grid[0])
    start = 1 + 1j
    visited = set()
    queue = [(0, start)]
    while len(queue) > 0:
        dist, pos = queue.pop(0)
        if pos in visited:
            continue
        for d in [1, -1, 1j, -1j]:
            new_pos = pos + d
            if new_pos == width - 2 + (height - 2) * 1j:
                return dist + 1
            if grid[int(new_pos.imag)][int(new_pos.real)] == "." and new_pos not in visited:
                queue.append((dist + 1, new_pos))
        visited.add(pos)
    return 0


def part_2(grid, obs):
    for o in obs:
        grid[o[1] + 1][o[0] + 1] = "#"
        steps = calc_steps(grid)
        if steps == 0:
            return o


if __name__ == "__main__":
    with open("inputs/day_18.txt") as f:
        input = f.readlines()
        mem = [[int(x) for x in l.replace("\n", "").split(",")] for l in input]
        grid = create_grid(71)
        add_obstructions(grid, mem[:1024])
        steps = calc_steps(grid)
        print(steps, "< part 1")
        first_obs = part_2(grid, mem[1024:])
        print(first_obs, "< part 2")
