from copy import deepcopy


def find_cost(garden, letter):
    # finds the total cost from a letter

    copy_garden = deepcopy(garden)
    width = len(copy_garden[0])

    cost = 0

    # find the regions, calculate their area and perimeter via flood fill
    # then add to the cost
    # once a region has been found, we replace it with "."s and find the
    # next region
    # (because in the input there are many disconnected regions with the same letter)
    while letter in "".join(["".join(l) for l in copy_garden]):

        start_coord = "".join(["".join(l) for l in copy_garden]).find(letter)
        start_coord = complex(start_coord % width, start_coord // width)

        region = set()
        perimeter = 0
        area = 0
        queue = {start_coord}

        while len(queue) > 0:
            loc = queue.pop()
            # we're in the region, so area += 1
            area += 1

            for d in [1, -1, 1j, -1j]:
                new_loc = loc + d
                if new_loc in region:
                    continue
                if copy_garden[int(new_loc.imag)][int(new_loc.real)] == letter:
                    queue.add(new_loc)
                else:
                    # the adjacent cell is not in the region
                    # i.e. it's a boundary
                    # so the perimeter increases
                    perimeter += 1

            region.add(loc)

        for loc in region:
            copy_garden[int(loc.imag)][int(loc.real)] = "."

        cost += area * perimeter

    return cost


def find_total_cost(garden):
    letters = set("".join(["".join(l) for l in garden]))
    letters.remove(".")
    return sum([find_cost(garden, letter) for letter in letters])


def calc_edges(garden, letter):
    # returns a dictionary with the top left corner of each region
    # with letter, the set of cells that region contains, and its
    # number of edges

    # This technically does not work if there is a region inside another region
    # inside another region and the 1st and 3rd share the same letter
    # The input does not have this edge case (I checked)

    copy_garden = deepcopy(garden)
    height = len(copy_garden)
    width = len(copy_garden[0])

    regions = {}

    # Number of edges == number of corners
    # We find the edges by doing a "left hand against the wall" algorithm
    # and whenever we turn, we have hit a corner so increment edges by 1

    # And we keep track of the edges and their direction for later

    while letter in "".join(["".join(l) for l in copy_garden]):

        start_coord = "".join(["".join(l) for l in copy_garden]).find(letter)
        start_coord = complex(start_coord % width, start_coord // width)

        edges = set()
        dir = 1
        coord = start_coord
        edge_count = 0
        while not (coord == start_coord and dir == 1) or len(edges) == 0:

            # try to turn left:
            left_cell = coord + dir*-1j
            if copy_garden[int(left_cell.imag)][int(left_cell.real)] == letter:
                # we can turn left
                coord = left_cell
                dir = dir * -1j
                edge_count += 1
                continue

            # We can't go left
            # attempt to go straight
            forward_cell = coord + dir
            if copy_garden[int(forward_cell.imag)][int(forward_cell.real)] == letter:
                # we can go forwards
                edges.add((coord, dir))
                coord = forward_cell
                continue

            # we can't go left or straight
            # so we turn right
            edges.add((coord, dir))
            dir = dir * 1j
            edge_count += 1

        # Now we have a set of edges and the direction they point in
        # We will fill in the region by drawing horzontal rays and keeping
        # track of if we are inside are not

        # We are now inside if:
        #   We were previously outside
        #   The cell we just ENTERED Is on the edge with direcion up (1j)
        # We are now outside if:
        #   We were previously outside
        #   The cell we just LEFT is on the edge with direction down (-1j)
        # Otherwise we haven't changed

        cells = set()

        min_x = int(min([e[0].real for e in edges]))
        max_x = int(max([e[0].real for e in edges]))
        min_y = int(min([e[0].imag for e in edges]))
        max_y = int(max([e[0].imag for e in edges]))

        for y in range(min_y, max_y + 1):
            inside = False
            for x in range(min_x - 1, max_x + 1):
                if inside:
                    if (complex(x-1, y), 1j) in edges:
                        # we are now outside
                        inside = False
                    else:
                        cells.add(complex(x, y))
                else:
                    if (complex(x, y), -1j) in edges:
                        # we are now inside
                        inside = True
                        cells.add(complex(x, y))

        regions[start_coord] = [cells, edge_count]

        # Replace the found region with .s and check for more
        for loc in cells:
            copy_garden[int(loc.imag)][int(loc.real)] = "."

    return regions


def find_total_cost_2(garden):
    filled_regions = {}
    letters = set("".join(["".join(l) for l in garden]))
    letters.remove(".")
    for l in letters:
        regions = calc_edges(garden, l)
        filled_regions.update(regions)
    total_cost = 0
    # we now have a dicionary of the shapes and their edges
    # but these are filled in
    # so to calculate the area and edges, we check if their are
    # regions inside them
    # These regions subtract from the area but add to the edges
    for loc, region in filled_regions.items():
        area = len(region[0])
        edges = region[1]
        to_check = deepcopy(region[0])
        to_check.discard(loc)
        for c in to_check:
            if c in filled_regions:
                subregion = filled_regions[c]
                area -= len(subregion[0])
                edges += subregion[1]
        total_cost += area * edges
    return total_cost


def pad_garden(garden):
    garden = garden.splitlines()
    height = len(garden)
    width = len(garden[0])
    garden.insert(0, "." * width)
    garden.append("." * width)
    return [[".", *list(l), "."] for l in garden]


if __name__ == "__main__":
    with open("inputs/day_12.txt") as f:
        input = f.read()
        garden = pad_garden(input)
        cost = find_total_cost(garden)
        print(cost, "< part 1")
        cost_2 = find_total_cost_2(garden)
        print(cost, "< part 2")
