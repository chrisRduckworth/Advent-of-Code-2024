from itertools import chain


def run_program(registers, program):
    # just do what the problem says
    memory = {"A": registers[0], "B": registers[1], "C": registers[2]}
    output = []
    pointer = 0

    while pointer < len(program):
        opcode, l_operand = program[pointer]
        c_operand = -1
        match l_operand:
            case 4:
                c_operand = memory["A"]
            case 5:
                c_operand = memory["B"]
            case 6:
                c_operand = memory["C"]
            case 7:
                pass
            case _:
                c_operand = l_operand

        match opcode:
            case 0:
                memory["A"] = memory["A"] // (2 ** c_operand)
            case 1:
                memory["B"] = memory["B"] ^ l_operand
            case 2:
                memory["B"] = c_operand % 8
            case 3:
                if memory["A"] != 0:
                    pointer = l_operand
                else:
                    pointer += 1
            case 4:
                memory["B"] = memory["B"] ^ memory["C"]
            case 5:
                output.append(c_operand % 8)
            case 6:
                memory["B"] = memory["A"] // (2 ** c_operand)
            case 7:
                memory["C"] = memory["A"] // (2 ** c_operand)

        if opcode != 3:
            pointer += 1

    return output


def calc_prev(A_n_minus_k, o_n_minus_k):
    # Let A_n be the value of the register A after the n-th jump
    # Then the output and the n+1-th jump is runprogram([A_n, 0, 0], program)
    # So we can check the solutions against what we need (i.e. to match the program)
    if A_n_minus_k == 0 and o_n_minus_k == 0:
        return [7]
    # Because of reasons (I.e. me look at the input and doing maths)
    # possibilities are between 8 * A_n_minus_k, 8 * A_n_minus_k + 7
    matches = []
    for A_n_minus_k_minus_1 in range(8 * A_n_minus_k, 8*A_n_minus_k + 8):
        out = run_program([A_n_minus_k_minus_1, 0, 0], program)[0]
        if out == o_n_minus_k:
            matches.append(A_n_minus_k_minus_1)
    return matches


def calc_first(program):
    # work backwards iteratively through the required outputs
    flattened = list(chain.from_iterable(program))
    A_ns = [[0]]
    for o_n in flattened[::-1]:
        # there can be multiple matches per input, but not all of them will work
        # so we keep track of them in array and check each
        # only adding to the next array if there are matches
        A_n_minus_1 = []
        for A_n in A_ns[0]:
            matches = calc_prev(A_n, o_n)
            if len(matches) > 0:
                A_n_minus_1.extend(matches)
        A_ns.insert(0, A_n_minus_1)

    return A_ns[0][0]


if __name__ == "__main__":
    with open("inputs/day_17.txt") as f:
        input = f.readlines()
        registers = [int(input[0][12:-1]), int(input[1]
                                               [12:-1]), int(input[2][12:-1])]
        program = input[4][9:].split(",")
        program = [[int(program[2 * i]), int(program[2 * i + 1])]
                   for i in range(len(program) // 2)]
        output = run_program(registers, program)
        print(",".join([str(x) for x in output]), "< part 1")
        first_A = calc_first(program)
        print(first_A, "< part 2")
