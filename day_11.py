from math import log10, floor
from functools import cache

# Initially I attempted to write my own memoization in here
# I'm pretty sure it would have worked and been faster, 
# but it was complicated and I ran out of time. 

# Hence why I switched to @cache at 10:30pm

@cache
def calc_rocks(n, blinks):
    # returns a dictionary containing each numbered rock
    # and how many times they appear
    # after blinking at n blinks times

    if blinks == 0:
        return {n: 1}
  
    rocks = []

    if n == 0:
        rocks = [1]
    elif (floor(log10(n)) + 1) % 2 == 0:
        # that's just a fancy way to calculate the number of digits without converting to a string
        # which apparently is slow
        length = floor(log10(n)) + 1
        right_half = int(n % (10 ** (length/2)))
        left_half = floor(n / (10**(length/2)))
        rocks = [left_half, right_half]
    else:
        rocks = [n * 2024]

    result = {}
    for rock in rocks:
        rock_res = calc_rocks(rock, blinks - 1)
        # add these rocks to the result
        for r in rock_res:
            if r in result:
                result[r] += rock_res[r]
            else:
                result[r] = rock_res[r]

    return result

def count_rocks(rocks, blinks):
    final_rocks = []
    for rock in rocks:
        final_rocks.append(calc_rocks(rock, blinks))
    return sum([sum(list(rocks.values())) for rocks in final_rocks])

if __name__ == "__main__":
    with open("inputs/day_11.txt") as f:
        input = f.read()
        rocks = [int(s) for s in input.split(" ")]
        rock_count = count_rocks(rocks, 25)
        print(rock_count, "< rock count")
        rock_count_2 = count_rocks(rocks, 75)
        print(rock_count_2, "< rock count 2")
