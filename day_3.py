import re


def multiply(memory):
    matches = re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', memory)
    pairs = [[int(m.group(1)), int(m.group(2))]for m in matches]
    total = sum([p[0] * p[1] for p in pairs])
    return total
    # one line, just for fun:
    # return sum([int(m.group(1)) * int(m.group(2)) for m in re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', memory)])


def part2(memory):
    split = re.split(r'do\(\)', memory)
    vsplit = [re.split(r'don\'t\(\)', s)for s in split]
    comb = ''.join([l[0] for l in vsplit])
    t = multiply(comb)
    return t
    # one line, just for fun:
    # return multiply(''.join([l[0] for l in [re.split(r'don\'t\(\)', s)for s in re.split(r'do\(\)', memory)]]))


if __name__ == "__main__":
    with open("inputs/day_3.txt") as f:
        mem = f.read()
        total = multiply(mem)
        print(total, "< total")
        total2 = part2(mem)
        print(total2, "< total2")
