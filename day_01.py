def find_distance(ids):
    id_list = [s.split() for s in ids]
    list_one = [int(x[0]) for x in id_list]
    list_two = [int(x[1]) for x in id_list]
    list_one.sort()
    list_two.sort()
    sum = 0
    for i in range(0, len(list_one)):
        sum += abs(list_one[i] - list_two[i])

    return sum


def sim_score(ids):
    id_list = [s.split() for s in ids]
    list_one = [int(x[0]) for x in id_list]
    list_two = [int(x[1]) for x in id_list]

    counts = {}

    for x in list_one:
        if (x in counts):
            pass
        else:
            counts[x] = sum([1 for y in list_two if x == y])

    sim = sum([x * counts[x] for x in list_one])
    return sim


if __name__ == "__main__":
    with open("inputs/day_01.txt") as f:
        ids = f.readlines()
        dist = find_distance(ids)
        print(dist, "< dist")
        sim = sim_score(ids)
        print(sim, "< sim")
