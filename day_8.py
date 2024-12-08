from itertools import combinations

def count_antinodes(antenna):
    height = len(antenna)
    width = len(antenna[0])

    antenna = "".join(antenna)
    freqs = {f for f in antenna.replace(".", "")}
    antinodes = set()

    for freq in freqs:
        indices = [i for i in range(len(antenna)) if antenna[i] == freq]
        for a, b in combinations(indices, 2):
            # b > a because of how indices is constructed
            ant1 = 2 * a - b
            ant2 = 2 * b - a
            a_x, a_y = a % width, a // width
            b_x, b_y = b % width, b // width

            # check the antinodes are still within the bounds of the grid
            if 0 <= 2 * a_x - b_x < width and 0 <= 2 * a_y - b_y < height:
                antinodes.add(ant1)
            if 0 <= 2 * b_x - a_x < width and 0 <= 2 * b_y - a_y < height:
                antinodes.add(ant2)
    return len(antinodes)

def count_antinodes_2(antenna):
    height = len(antenna)
    width = len(antenna[0])

    antenna = "".join(antenna)
    freqs = {f for f in antenna.replace(".", "")}
    antinodes = set()

    for freq in freqs:
        indices = [i for i in range(len(antenna)) if antenna[i] == freq]
        for a, b in combinations(indices, 2):
            # b > a because of how indices is constructed
            a_x, a_y = a % width, a // width
            b_x, b_y = b % width, b // width

            ant1_x, ant1_y = a_x, a_y
            ant2_x, ant2_y = b_x, b_y

            while 0 <= ant1_x < width and 0 <= ant1_y < height:
                antinodes.add(ant1_x + width * ant1_y)
                ant1_x -= b_x - a_x
                ant1_y -= b_y - a_y

            while 0 <= ant2_x < width and 0 <= ant2_y < height:
                antinodes.add(ant2_x + width * ant2_y)
                ant2_x += b_x - a_x
                ant2_y += b_y - a_y

    return len(antinodes)


if __name__ == "__main__":
    with open("inputs/day_8.txt") as f:
        input = [l[:-1] for l in f.readlines()]
        total = count_antinodes(input)
        print(total, "< number of antinodes")
        total_2 = count_antinodes_2(input) # 1142 too high
        print(total_2, "< part 2")