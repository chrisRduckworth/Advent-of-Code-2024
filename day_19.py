from functools import cache


def is_possible(towels, pattern):
    if pattern in towels:
        return True

    for towel in towels:
        if pattern.startswith(towel):
            if is_possible(towels, pattern[len(towel):]):
                return True

    return False


def part_1(towels, patterns):
    count = 0
    for pattern in patterns:
        if is_possible(towels, pattern):
            count += 1
    return count


def part_2(towels, patterns):
    sum = 0

    # define the function here so we can use @cache
    # otherwise it tries to cache towels which isn't necessary
    @cache
    def count_possible(pattern):
        count = 0
        for towel in towels:
            if pattern == towel:
                count += 1
            elif pattern.startswith(towel):
                count += count_possible(pattern[len(towel):])
        return count

    for pattern in patterns:
        sum += count_possible(pattern)
    return sum


if __name__ == "__main__":
    with open("inputs/day_19.txt") as f:
        input = f.readlines()
        towels = set(input[0][:-1].split(", "))
        patterns = [p.replace("\n", "") for p in input[2:]]
        no_towels = part_1(towels, patterns)
        print(no_towels, "< part 1")
        possible_combos = part_2(towels, patterns)
        print(possible_combos, "< part 2")
