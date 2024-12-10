def create_map(input):
    # turns the array of strings into a grid with padded edges
    grid = [["X", *[int(c) for c in l], "X"] for l in input]
    grid.insert(0, ["X"] * len(grid[0]))
    grid.append(["X"] * len(grid[0]))
    return grid

def print_grid(grid):
    for l in grid:
        print("".join(str(c) for c in l))

def find_trailheads(grid):
    # returns a list of the indices of starting positions
    trailheads = []
    for y, row in enumerate(grid):
        for x, height in enumerate(row):
            if height == 0:
                trailheads.append((x, y))

    return trailheads

def count_hikes(grid, trailhead):
    # use a breadth-first search to find
    # ending nodes
    # nines = set()
    hikes = 0
    visited = set()
    queue = [trailhead]
    while len(queue) > 0:
        x, y = queue.pop(0)
        curr_height = grid[y][x]

        if "({0}, {1})".format(x, y) in visited:
            # because sometimes we can end up in the 
            # same cell from several directions
            # i could use a difference data type for queue here
            # if i was smart
            continue

        if curr_height == 9:
            # end of the trail
            # nines.add("({0}, {1})".format(x, y))
            hikes += 1
            visited.add("({0}, {1})".format(x, y))
            continue

        # add adjacent cells if:
        # they haven't been visited
        # and they are one higher than the current cell
        adjacent = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for dx, dy in adjacent:
            posx, posy = x + dx, y + dy
            cell = grid[posy][posx]
            if "({0}, {1})".format(posx, posy) not in visited:
                if cell == curr_height + 1:
                    queue.append([posx, posy])
        visited.add("({0}, {1})".format(x, y))

    return hikes

def part_1(grid):
    trailheads = find_trailheads(grid)
    total_score = sum([count_hikes(grid, h) for h in trailheads])
    return total_score

def count_unique_hikes(grid, trailhead):
    # use a breadth-first search to find
    # ending nodes
    hikes = 0
    visited = set()
    queue = [trailhead]
    while len(queue) > 0:
        x, y = queue.pop(0)
        curr_height = grid[y][x]

        if curr_height == 9:
            hikes += 1
            continue

        # add adjacent cells if:
        # they haven't been visited
        # and they are one higher than the current cell
        adjacent = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for dx, dy in adjacent:
            posx, posy = x + dx, y + dy
            cell = grid[posy][posx]
            if "({0}, {1})".format(posx, posy) not in visited:
                if cell == curr_height + 1:
                    queue.append([posx, posy])
        visited.add("({0}, {1})".format(x, y))

    return hikes

def part_2(grid):
    trailheads = find_trailheads(grid)
    total_score = sum([count_unique_hikes(grid, h) for h in trailheads])
    return total_score


if __name__ == "__main__":
    with open("inputs/day_10.txt") as f:
        input = [l.rstrip() for l in f.readlines()]
        grid = create_map(input)
        score = part_1(grid)
        print(score, "< part 1")
        score2 = part_2(grid)
        print(score2, "< part 2")

