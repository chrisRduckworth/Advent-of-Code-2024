import re


def calc_tokens(button_1, button_2, prize):
    a_1, a_2 = button_1
    b_1, b_2 = button_2
    c_1, c_2 = prize

    # the "optimal price" part of this is meaningless
    # we actually just have two linear equations to solve

    # A*button_1_x + B*button_2_x = prize_x
    # A*button_1_y + B*button_2_y = prize_y

    # And solve for A and B using Cramer's Rule

    # JOOOOOHN KRAMEERRRRR

    denom = a_1 * b_2 - a_2 * b_1

    if denom == 0:
        # They never touch
        return 0

    num_x = c_1 * b_2 - b_1 * c_2
    num_y = a_1 * c_2 - a_2 * c_1

    a_count = num_x / denom
    b_count = num_y / denom
    if not (a_count.is_integer() and b_count.is_integer()):
        # non-integer solution
        return 0

    if a_count < 0 or b_count < 0:
        # negative solution
        return 0

    return 3 * a_count + b_count


def create_inputs(input):
    seperate = input.split("\n\n")
    output = []
    for l in seperate:
        xs = re.findall(r'(?<=X\+)\d+', l)
        ys = re.findall(r'(?<=Y\+)\d+', l)
        prize = re.findall(r'(?<==)\d+', l)
        button_a = (int(xs[0]), int(ys[0]))
        button_b = (int(xs[1]), int(ys[1]))
        prize = (int(prize[0]), int(prize[1]))
        output.append((button_a, button_b, prize))

    return output


def create_inputs_2(input):
    seperate = input.split("\n\n")
    output = []
    for l in seperate:
        xs = re.findall(r'(?<=X\+)\d+', l)
        ys = re.findall(r'(?<=Y\+)\d+', l)
        prize = re.findall(r'(?<==)\d+', l)
        button_a = (int(xs[0]), int(ys[0]))
        button_b = (int(xs[1]), int(ys[1]))
        prize = (10000000000000 + int(prize[0]),
                 10000000000000 + int(prize[1]))
        output.append((button_a, button_b, prize))

    return output


def calc_total_tokens(machines):
    return sum([calc_tokens(*machine) for machine in machines])


if __name__ == "__main__":
    with open("inputs/day_13.txt") as f:
        input = f.read()
        machines = create_inputs(input)
        total = calc_total_tokens(machines)
        print(total, "< total tokens")
        machines_2 = create_inputs_2(input)
        total_2 = calc_total_tokens(machines_2)
        print(total_2, "< part 2")
