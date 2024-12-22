from itertools import permutations, product
from functools import cache


def calc_distance(combo):
    # counts the number of total buttons of the parent robot presses for a combo
    # this is equal to total distance traveled plus the numer of total buttons pressed
    dir_positions = {"^": 1 + 0j, "A": 2 + 0j,
                     "<": 0 + 1j, "v": 1 + 1j, ">": 2 + 1j}

    t_dist = 0
    pos = dir_positions["A"]
    for b in combo:
        dist = dir_positions[b] - pos
        t_dist += abs(dist.imag) + abs(dist.real) + 1
        pos = dir_positions[b]

    return t_dist


def find_opt_rob1(curr, target):
    # finds the optimal moves for the first robot to take
    num_positions = {"7": 0 + 0j, "8": 1 + 0j, "9": 2 + 0j,
                     "4": 0 + 1j, "5": 1 + 1j, "6": 2 + 1j,
                     "1": 0 + 2j, "2": 1 + 2j, "3": 2 + 2j,
                     "0": 1 + 3j, "A": 2 + 3j}

    dist = num_positions[target] - num_positions[curr]

    combos = ""
    if dist.real > 0:
        combos += ">" * int(dist.real)
    elif dist.real < 0:
        combos += "<" * int(-dist.real)

    if dist.imag > 0:
        combos += "v" * int(dist.imag)
    elif dist.imag < 0:
        combos += "^" * int(-dist.imag)
    combos = set("".join(c) for c in permutations(combos))

    # throw out combos where the robot would go over the empty space
    if num_positions[curr].real == 0 and num_positions[target].imag == 3:
        illegible = "v" * int(dist.imag) + ">" * int(dist.real)
        combos.remove(illegible)
    elif num_positions[curr].imag == 3 and num_positions[target].real == 0:
        illegible = "<" * int(- dist.real) + "^" * int(-dist.imag)
        combos.remove(illegible)

    combos = {c + "A": calc_distance(c + "A") for c in combos}
    min_score = min(combos.values())
    # only return combos with the lowest distance

    return [c for c in combos if combos[c] == min_score]


def find_opt_rob2(curr, target):
    # finds the optimal moves for a directional robot to take
    # basically the same as above
    dir_positions = {"^": 1 + 0j, "A": 2 + 0j,
                     "<": 0 + 1j, "v": 1 + 1j, ">": 2 + 1j}

    dist = dir_positions[target] - dir_positions[curr]

    combos = ""

    if dist.real > 0:
        combos += ">" * int(dist.real)
    elif dist.real < 0:
        combos += "<" * int(-dist.real)

    if dist.imag > 0:
        combos += "v" * int(dist.imag)
    elif dist.imag < 0:
        combos += "^" * int(-dist.imag)
    combos = set("".join(c) for c in permutations(combos))

    if curr == "<" and dir_positions[target].imag == 0:
        illegible = "^" + ">" * int(dist.real)
        combos.remove(illegible)
    elif dir_positions[curr].imag == 0 and target == "<":
        illegible = "<" * int(-dist.real) + "v"
        combos.remove(illegible)

    combos = {c + "A": calc_distance(c + "A") for c in combos}
    min_score = min(combos.values())

    return [c for c in combos if combos[c] == min_score]


@cache
def calc_length(curr, target, robot_number):
    # calculates the number of moves the final robot (you)
    # will have to make to move the first directional robot from curr to target

    combos = find_opt_rob2(curr, target)
    if robot_number == 1:
        # final robot
        return len(combos[0])

    lengths = []

    for combo in combos:
        length = 0
        for i, c in enumerate(["A", *combo][:-1]):
            curr_c = c
            target_c = combo[i]
            length += calc_length(curr_c, target_c, robot_number - 1)
        lengths.append(length)

    return min(lengths)


def find_complexity(rob1_ins, int_robot_count):
    # first find the optimal combos from the first robot
    results = []
    for i, n in enumerate(["A", *rob1_ins][:-1]):
        curr = n
        target = rob1_ins[i]
        out = find_opt_rob1(curr, target)
        results.append(out)
    results = ["".join(l) for l in list(product(*results))]
    rob2_min = min([len(c) for c in results])
    rob2_opt = [c for c in results if len(c) == rob2_min]

    # now find the lengths of the combos coming off from that
    mins = []
    for combo in rob2_opt:
        sum = 0
        for i, c in enumerate(["A", *combo][:-1]):
            curr = c
            target = combo[i]
            sum += calc_length(curr, target, int_robot_count)
        mins.append(sum)
    numeric = int(rob1_ins[:-1].lstrip("0"))
    return numeric * min(mins)


def calc_complexities_2(codes, int_robot_count):
    return sum([find_complexity(c, int_robot_count) for c in codes])


if __name__ == "__main__":
    with open("inputs/day_21.txt") as f:
        input = [c.replace("\n", "") for c in f.readlines()]
        print(calc_complexities_2(input, 2))
        print(calc_complexities_2(input, 25))
