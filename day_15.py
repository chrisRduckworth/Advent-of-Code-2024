from itertools import chain
from functools import cmp_to_key
import re


def get_slice(warehouse, pos, dir):
    # creates a string of the same row/column
    # in the direction dir from positions pos
    line = []
    if dir == 1:
        line = warehouse[int(pos.imag)][int(pos.real) + 1:]
    elif dir == -1:
        line = warehouse[int(pos.imag)][int(pos.real) - 1::-1]
    elif dir == 1j:
        line = [l[int(pos.real)] for l in warehouse[int(pos.imag) + 1:]]
    elif dir == -1j:
        line = [l[int(pos.real)] for l in warehouse[int(pos.imag) - 1::-1]]
    return "".join(line)


def find_last_pos(warehouse, movements):
    width = len(warehouse[0])
    height = len(warehouse)
    # hey look at this neat way of making the pos using divmod
    pos = complex(*divmod("".join(["".join(l)
                  for l in warehouse]).find("@"), width)[::-1])
    for move in movements:
        dir = 0
        match move:
            case "v": dir = 1j
            case "^": dir = -1j
            case ">": dir = 1
            case "<": dir = -1
        rest_of_line = get_slice(warehouse, pos, dir)
        # we can move if there are any Os followed by a dot
        # which we check using regex:
        can_move = re.match(r'^(O*)\.', rest_of_line)
        if can_move:
            num_os = len(can_move.group(1))
            # move @
            warehouse[int(pos.imag)][int(pos.real)] = "."
            new_pos = pos + dir
            warehouse[int(new_pos.imag)][int(new_pos.real)] = "@"
            # move Os
            for i in range(num_os):
                o_pos = new_pos + dir * (i + 1)
                warehouse[int(o_pos.imag)][int(o_pos.real)] = "O"
            pos = new_pos

    return warehouse


def calc_GPS_coord(warehouse):
    sum = 0
    for y, l in enumerate(warehouse):
        for x, c in enumerate(l):
            if c == "O":
                sum += 100 * y + x
    return sum


def part_one(warehouse, movements):
    # first move everything in the warehouse
    warehouse = find_last_pos(warehouse, movements)
    # then calculate the score
    total_GPS = calc_GPS_coord(warehouse)
    return total_GPS


def find_last_pos_2(warehouse, movements):
    # Exactly the same approach as part 1 for horizontal moves
    # but for vertical we check recursively if there is a box
    # until either everything can move or we hit a #

    width = len(warehouse[0])
    height = len(warehouse)
    pos = complex(*divmod("".join(["".join(l)
                  for l in warehouse]).find("@"), width)[::-1])

    for move in movements:
        dir = 0
        match move:
            case "v": dir = 1j
            case "^": dir = -1j
            case ">": dir = 1
            case "<": dir = -1

        if dir == 1 or dir == -1:
            rest_of_line = get_slice(warehouse, pos, dir)
            can_move = re.match(r'^((\[\])*|(\]\[)*)\.', rest_of_line)
            if can_move:
                num_boxes = len(can_move.group(1))
                # move @
                warehouse[int(pos.imag)][int(pos.real)] = "."
                new_pos = pos + dir
                warehouse[int(new_pos.imag)][int(new_pos.real)] = "@"
                # move []s
                for i in range(num_boxes):
                    if dir == 1:
                        char = "[" if i % 2 == 0 else "]"
                    else:
                        char = "]" if i % 2 == 0 else "["
                    box_pos = new_pos + dir * (i + 1)
                    warehouse[int(box_pos.imag)][int(box_pos.real)] = char
                pos = new_pos
        else:
            new_pos = pos + dir
            # get the simple cases out of the way
            if warehouse[int(new_pos.imag)][int(new_pos.real)] == ".":
                warehouse[int(pos.imag)][int(pos.real)] = "."
                warehouse[int(new_pos.imag)][int(new_pos.real)] = "@"
                pos = new_pos
            elif warehouse[int(new_pos.imag)][int(new_pos.real)] == "#":
                # do nothing
                pass
            else:
                # box time
                is_movable = True
                new_pos_char = warehouse[int(new_pos.imag)][int(new_pos.real)]
                to_move = set(
                    [new_pos, new_pos - 1 if new_pos_char == "]" else new_pos + 1])
                # to move is a set of all the boxes to move once finished
                queue = set(
                    [new_pos, new_pos - 1 if new_pos_char == "]" else new_pos + 1])
                # queue is a set of boxes to check if they can be moved
                while len(queue) > 0:
                    cell = queue.pop()

                    next_cell = cell + dir
                    next_cell_char = warehouse[int(
                        next_cell.imag)][int(next_cell.real)]

                    # check if the nex cell can't move
                    if next_cell_char == "#":
                        is_movable = False
                        break

                    if next_cell_char == "[":  # ]
                        queue.add(next_cell)
                        queue.add(next_cell + 1)
                    elif next_cell_char == "]":
                        queue.add(next_cell)
                        queue.add(next_cell - 1)

                    # do nothing if it's a . beause theres nothing new to move

                    to_move.add(cell)

                # This can be optimized slightly by checking if the box above is exactly lined up with the current one
                # but it's so minor it's not worth it

                if is_movable:
                    # sort to_move in reverse order and move each cell
                    def cmp_function(a, b):
                        if dir == 1j:
                            return b.imag - a.imag
                        if dir == -1j:
                            return a.imag - b.imag

                    to_move = list(to_move)
                    to_move.sort(key=cmp_to_key(cmp_function))

                    # move the []s
                    for cell in to_move:
                        warehouse[int((cell + dir).imag)][int(cell.real)
                                                          ] = warehouse[int(cell.imag)][int(cell.real)]
                        warehouse[int(cell.imag)][int(cell.real)] = "."
                    # move the @
                    warehouse[int(pos.imag)][int(pos.real)] = "."
                    warehouse[int(new_pos.imag)][int(new_pos.real)] = "@"
                    pos = new_pos

    return warehouse


def calc_GPS_2(warehouse):
    sum = 0
    for y, l in enumerate(warehouse):
        for x, c in enumerate(l):
            if c == "[":
                sum += 100 * y + x
    return sum


def part_two(warehouse, movements):
    warehouse = find_last_pos_2(warehouse, movements)
    total_GPS = calc_GPS_2(warehouse)
    return total_GPS


if __name__ == "__main__":
    with open("inputs/day_15.txt") as f:
        input = f.read()
        warehouse, movements = input.split("\n\n")
        warehouse = [list(l) for l in warehouse.splitlines()]
        movements = list(chain.from_iterable(movements.splitlines()))
        total_GPS = part_one(warehouse, movements)
        print(total_GPS, "< part 1")

        warehouse, movements = input.split("\n\n")
        warehouse = warehouse.replace("#", "##").replace(
            "O", "[]").replace(".", "..").replace("@", "@.")
        warehouse = [list(l) for l in warehouse.splitlines()]
        movements = list(chain.from_iterable(movements.splitlines()))
        total_2 = part_two(warehouse, movements)
        print(total_2, "< part 2")
