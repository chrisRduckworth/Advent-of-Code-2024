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

if __name__ == "__main__":
    with open("inputs/day_5.txt") as f:
        [instructions, updates] = f.read().split("\n\n")
        instructions = [[int(x) for x in i.split("|")] for i in instructions.split("\n")]
        updates = [[int(x) for x in u.split(",")] for u in updates.split("\n")]
        total = sum_middle(instructions, updates)
        print(total)
