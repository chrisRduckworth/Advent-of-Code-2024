import re

def multiply(memory):
    # print(memory)
    # matches = re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', memory)
    # pairs = [[int(m.group(1)), int(m.group(2))]for m in matches]
    # total = sum([p[0] * p[1] for p in pairs])
    # return total
    # one line:
    return sum([int(m.group(1)) * int(m.group(2)) for m in re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', memory)])

def part2(memory):
    # split = re.split(r'do\(\)', memory)
    # vsplit = [re.split(r'don\'t\(\)', s)for s in split]
    # comb = ''.join([l[0] for l in vsplit])
    # t = multiply(comb)
    # return t
    # one line
    return multiply(''.join([l[0] for l in [re.split(r'don\'t\(\)', s)for s in re.split(r'do\(\)', memory)]]))


if __name__ == "__main__":
    with open("inputs/day_3.txt") as f:
        mem = f.read()
        total = multiply(mem)
        print(total, "< total")
        # test = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
        # m = multiply(test)
        total2 = part2(mem)
        print(total2, "< total2")
        # test2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        # m2 = part2(test2)
        # print(m2)
