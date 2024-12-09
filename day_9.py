from itertools import chain


def compact_map(map):
    map_arr = []
    for i, d in enumerate(map):
        if i % 2 == 0:
            # it's a file
            # input contains no 0s at even positions (convenient)
            # using // here to turn it into an int
            map_arr.append([i // 2] * int(d))
        else:
            if int(d) > 0:
                map_arr.append([-1] * int(d))

    flat = list(chain.from_iterable(map_arr))
    i = 0
    out = []

    while i < len(flat):
        e = flat[i]
        if e != -1:
            out.append(e)
        else:
            out.append(flat.pop())
            while flat[-1] == -1:
                flat.pop()
        i += 1

    return out


def calc_checksum(blocks):
    return sum([i * x for i, x in enumerate(blocks) if x > 0])


def defrag_map(map):
    # This can definitely be optimised - currently O(n^2)
    # I think using some sort of map to keep track of lengths?
    # basically a faster way to find the first available space
    # for the file

    # But I have stuff to do today
    # Runs in about 6 seconds

    map_arr = []
    for i, d in enumerate(map):
        if i % 2 == 0:
            map_arr.append([i // 2] * int(d))
        else:
            if int(d) > 0:
                map_arr.append([-1] * int(d))

    i = -1

    while abs(i) <= len(map_arr):
        # work through the array backwards
        f1 = map_arr[i]
        if f1[0] != -1:
            for j, f2 in enumerate(map_arr[:i]):
                # find a space big enough to fit
                if f2[0] == -1:
                    if len(f1) == len(f2):
                        # fully replace the -1s
                        map_arr[j] = f1
                        map_arr[i] = [-1] * len(f1)
                        break
                    if len(f1) < len(f2):
                        # partially replace the -1s
                        map_arr[j] = f1
                        map_arr.insert(j+1, [-1] * (len(f2) - len(f1)))
                        map_arr[i] = [-1] * len(f1)
                        break
        i -= 1

    return list(chain.from_iterable(map_arr))


if __name__ == "__main__":
    with open("inputs/day_9.txt") as f:
        map = f.read()
        compacted = compact_map(map)
        csum = calc_checksum(compacted)
        print(csum, "< part 1")
        defragged = defrag_map(map)
        csum2 = calc_checksum(defragged)
        print(csum2, "< part 2")
