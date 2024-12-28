from functools import cmp_to_key


def sum_middle(instructions, updates):
    less_than = {}

    for [x, y] in instructions:
        if x in less_than:
            less_than[x].add(y)
        else:
            less_than[x] = {y}

    sum = 0

    for u in updates:
        if all(u[i] in less_than and u[i+1] in less_than[u[i]] for i in range(len(u) - 1)):
            sum += u[len(u)//2]

    return sum


def fix_incorrect(instructions, updates):
    less_than = {}

    for [x, y] in instructions:
        if x in less_than:
            less_than[x].add(y)
        else:
            less_than[x] = {y}

    incorrect = []

    for u in updates:
        if not all(u[i] in less_than and u[i+1] in less_than[u[i]] for i in range(len(u) - 1)):
            incorrect.append(u)

    def sort_fn(a, b):
        if a in less_than and b in less_than[a]:
            return -1
        else:
            return 1

    fixed = [sorted(u, key=cmp_to_key(sort_fn)) for u in incorrect]

    return sum(u[len(u)//2] for u in fixed)


if __name__ == "__main__":
    with open("inputs/day_05.txt") as f:
        [instructions, updates] = f.read().split("\n\n")
        instructions = [[int(x) for x in i.split("|")]
                        for i in instructions.split("\n")]
        updates = [[int(x) for x in u.split(",")] for u in updates.split("\n")]
        total = sum_middle(instructions, updates)
        print(total, "< part 1")
        total_2 = fix_incorrect(instructions, updates)
        print(total_2, "< part 2")
