import re
from functools import cmp_to_key

def calc_robot_position(start, vel, seconds, height, width):
    start_x, start_y = start
    vel_x, vel_y = vel
    x = (start_x + seconds * vel_x) % width
    y = (start_y + seconds * vel_y) % height
    return (x, y)

def count_robots_quad(positions, height, width):
    mid_width = (width - 1) // 2
    mid_height = (height - 1) // 2

    top_left = [r for r in positions if r[0] < mid_width and r[1] < mid_height]
    top_right = [r for r in positions if r[0] > mid_width and r[1] < mid_height]
    bottom_left = [r for r in positions if r[0] < mid_width and r[1] > mid_height]
    bottom_right = [r for r in positions if r[0] > mid_width and r[1] > mid_height]

    return len(top_left) * len(top_right) * len(bottom_left) * len(bottom_right)

def all_robot_positions(robots, seconds, height, width):
    positions = []
    for robot in robots:
        pos = calc_robot_position(*robot, seconds, height, width)
        positions.append(pos)
    safety_rating = count_robots_quad(positions, height, width)

    return safety_rating

def positions_only(robots, seconds, height, width):
    positions = []
    for robot in robots:
        pos = calc_robot_position(*robot, seconds, height, width)
        positions.append(pos)

    return positions

def print_tree(robots, height, width):
    # just print out the lowest scoring setups and check manually

    # meh

    # this is such a poorly defined and vague problem I didn't even 
    # know what to look for or where to begin

    # I looked on the subreddit and saw people checking manually and that
    # seemed as good an idea as any

    def cmp_function(a, b):
        return a[0] - b[0]
    scores = []
    for i in range(height*width):
        positions = positions_only(robots, i, height, width)
        rating = count_robots_quad(positions, height, width)
        scores.append((rating, i, positions))
    scores.sort(key=cmp_to_key(cmp_function))
    for i in range(20):
        output = [["." for x in range(width)] for y in range(height)]
        for r in scores[i][2]:
            output[r[1]][r[0]] = "#"
        out_str = "\n".join(["".join(l) for l in output])
        print(out_str)
        print(scores[i][1], "< seconds")
        print("\n\n\n\n")


if __name__ == "__main__":
    with open("inputs/day_14.txt") as f:
        input = f.readlines()
        robots = [re.search(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', l) for l in input]
        robots = [m.groups() for m in robots]
        robots = [((int(t[0]), int(t[1])), (int(t[2]), int(t[3]))) for t in robots]
        safety_rating = all_robot_positions(robots, 100, 103, 101)
        print(safety_rating, "< part 1")
        print_tree(robots, 103, 101)
        


