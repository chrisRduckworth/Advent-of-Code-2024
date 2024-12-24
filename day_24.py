from copy import deepcopy
from graphlib import TopologicalSorter
from itertools import combinations, permutations
from random import randint

def create_input(input):
    wires, gates = input.split("\n\n")
    wires = wires.splitlines()
    gates = gates.splitlines()
    wires = {l.split(": ")[0]: int(l.split(": ")[1]) for l in wires}
    gates = [l.split(" ") for l in gates]
    gates = {g[4]: {"type": g[1], "in1": g[0], "in2": g[2]} for g in gates}
    return wires, gates

def run_machine(wires, gates):
    # do a topological sort of the wires
    # where each wire is dependent on the in wires of the graph
    wire_graph = {g: {gates[g]["in1"], gates[g]["in2"]} for g in gates}
    ts = TopologicalSorter(wire_graph)
    for w in ts.static_order():
        if w not in wires: # to ignore x00, y00 etc
            gate_type, in1, in2 = gates[w].values()
            match gate_type:
                case "AND":
                    wires[w] = wires[in1] & wires[in2]
                case "OR":
                    wires[w] = wires[in1] | wires[in2]
                case "XOR":
                    wires[w] = wires[in1] ^ wires[in2]
    return wires

def calc_num(wires):
    zs = sorted(w for w in wires if w[0] == "z")
    return sum(wires[v] * (2 ** i) for i, v in enumerate(zs))

def test(wires, gates):
    #hmm 
    # lets see what x and y are, and the z we are getting is
    wires = run_machine(wires, gates)
    xs = sorted(w for w in wires if w[0] == "x")
    ys = sorted(w for w in wires if w[0] == "y")
    zs = sorted(w for w in wires if w[0] == "z")
    x = sum(wires[v] * (2 ** i) for i, v in enumerate(xs))
    y = sum(wires[v] * (2 ** i) for i, v in enumerate(ys))
    z = sum(wires[v] * (2 ** i) for i, v in enumerate(zs))
    print(x, y)
    print(x + y, z)
    print(bin(x + y)[2:])
    print(bin(z)[2:])
    bin_sum = bin(x + y)[2:]
    bin_z = bin(z)[2:]
    for i in range(len(bin_sum)-1, -1, -1):
        print(bin_sum[i], bin_z[i], i)
    for i in range(len(bin_sum)-1, -1, -1):
        # print(bin_sum[i], bin_z[i], i)
        if bin_sum[i] != bin_z[i]:
            print("failed to match at ", i)

    # problem is
    # there could be some switched gates which aren't effecting the output
    # eg if a 1 and a 1 get swapped nothing changes

    # however we know these must be wrong
    # so by going backwards along the route those bits come from, we have a list of potentially swapped gates
    # which we brute force
    # et voila

def find_potential_swaps(wires, gates, pad = 46):
    # finds a list of output wires that could be swapped
    # we can create a list of every z that's wrong by doing a bunch of calculations
    # but for now we'll just start with what we're given
    

    out_wires = run_machine(deepcopy(wires), gates)
    xs = sorted(w for w in out_wires if w[0] == "x")
    ys = sorted(w for w in out_wires if w[0] == "y")
    zs = sorted(w for w in out_wires if w[0] == "z")

    x = sum(out_wires[v] * (2 ** i) for i, v in enumerate(xs))
    y = sum(out_wires[v] * (2 ** i) for i, v in enumerate(ys))
    z = sum(out_wires[v] * (2 ** i) for i, v in enumerate(zs))

    # i can just join the rest, this makes no sense wtf am i doing
    # expected = bin(x + y)[2:]
    expected = f'{x + y:0{pad}b}'
    # actual = bin(z)[2:]
    actual = f'{z:0{pad}b}'
    # print(len(expected), len(actual))

    # print(expected,actual, "< expected, actual")

    incorrect_zs = []

    for i in range(len(expected)):
        if expected[i] != actual[i]:
            # print("z{0:02}".format(i))
            # incorrect_zs.append("z{0:02}".format(i))
            # print(f'z{i:02}')
            incorrect_zs.append(f'z{i:02}')

    # for each of these, we backtrack through the wires to get all of the parents? 

    potential_swapped = set()
    # for z in incorrect_zs:
    # print(gates)
    def find_parents(wire):
        if wire[0] == "x" or wire[0] == "y":
            return
        
        potential_swapped.add(wire)
        parent_1, parent_2 = gates[wire]["in1"], gates[wire]["in2"]
        find_parents(parent_1)
        find_parents(parent_2)
    # find_parents(incorrect_zs[0]) print(potential_swapped)
    for z in incorrect_zs:
        find_parents(z)
    # print(potential_swapped)
    # print(len(potential_swapped), len(out_wires))
    return potential_swapped

def test_swap(wires, gates, swaps):
    # returns the value of z when the swaps in swap are used
    gates = deepcopy(gates)
    for wire_1, wire_2 in swaps:
        temp_1 = gates[wire_1]
        temp_2 = gates[wire_2]
        gates[wire_2] = temp_1
        gates[wire_1] = temp_2

    try:
        out_wires = run_machine(deepcopy(wires), gates)
    except:
        # print("failed")
        return 0
    # print(out_wires)
    zs = sorted(w for w in out_wires if w[0] == "z")
    return sum(out_wires[v] * (2 ** i) for i, v in enumerate(zs))

def part_2(wires, gates):
    swaps = find_potential_swaps(wires, gates)
    # print(len(list(combinations(swaps, 8))))
    for combo in combinations(swaps, 8):
        # this is a bonkers number in the actual input
        # about 218 billion so this probably isn't going to work
        # :(
        print(list(combo), "< combo")
        # create pairings
        # for p in permutations(combo, 8):
        #     print(list(p))

def take_2(wires, gates):
    # lets try a variety of different inputs, create potential swaps from that and find their intersections    
    potentials = find_potential_swaps(wires, gates)
    # print(potentials, "< first")
    for i in range(45):
        # print(i, "< i")
        wires_c = deepcopy(wires)
        for c in range(5):
            wires_c[f'x{c:02}'] = 0
        wires_c[f'x{i:02}'] = 1
        # print(wires_c["x00"])
        # print(wires_c["x01"])
        # print(wires_c["x02"])
        # print(wires_c["x03"])
        # print(wires_c["x04"])

        # bin_rep_x = f'{i:05b}'
        # print(bin_rep_x)
        # print(bin_rep_x)
        # for x, d in enumerate(bin_rep_x):
        #     wires_c[f'x{5 - x:02}'] = int(d)
        #     print(f'x{5 - x:02}', wires_c[f'x{5 - x:02}'])
            
        for j in range(45):
            for c in range(5):
                wires_c[f'y{c:02}'] = 0
            wires_c[f'y{j:02}'] = 1

            # print(j, "< j")
            # bin_rep_y = f'{j:05b}'
            # for y, d in enumerate(bin_rep_y):
            #     wires_c[f'y{5 - y:02}'] = int(d)
            #     print(f'y{5 - y:02}', wires_c[f'y{5 - y:02}'])

            # wires are loaded up, find potential swapped
            pot = find_potential_swaps(wires_c, gates)
            # print(pot, "< pot")
            potentials = potentials & pot
            # print(potentials, "< potentials")
                
    print(potentials)
    print(len(potentials))
            
    return

def take_3(wires, edges):
    potentials = find_potential_swaps(wires, edges)
    init = wires
    wires = deepcopy(wires)
    p = 0
    while len(potentials) > 8:
        i = randint(0, 2**45 - 1)
        j = randint(0, 2**45 - 1)
        bin_rep_i = f'{i:045b}'
        bin_rep_j = f'{j:045b}'
        for n, digit in enumerate(bin_rep_i[::-1]):
            wire = f'x{n:02}'
            wires[wire] = int(digit)
        for n, digit in enumerate(bin_rep_j[::-1]):
            wire = f'y{n:02}'
            wires[wire] = int(digit)
        new_potentials = find_potential_swaps(wires, edges)
        # print(new_potentials, "< new potentials")
        if len(new_potentials) >= 8:
            potentials = potentials & new_potentials
        # print(potentials, "< intersected")
        p += 1
        if p % 1000 == 0:
            break
        
    # for i in range(2**45):
    #     wires_c = deepcopy(wires)
    #     bin_rep_i = f'{i:045b}'
    #     print(bin_rep_i)
    print(potentials)

    xs = sorted(w for w in init if w[0] == "x")
    ys = sorted(w for w in init if w[0] == "y")
    # zs = sorted(w for w in init if w[0] == "z")

    x = sum(init[v] * (2 ** i) for i, v in enumerate(xs))
    y = sum(init[v] * (2 ** i) for i, v in enumerate(ys))
    # z = sum(init[v] * (2 ** i) for i, v in enumerate(zs))

    expected = x + y
    p = 0
    for combo in combinations(potentials, 8):
        swaps = [[combo[0], combo[1]], [combo[2], combo[3]], [combo[4], combo[5]], [combo[6], combo[7]]]
        # print(list(combo), "< combo")
        res = test_swap(init, gates, swaps)
        # print(res)
        if(res == expected):
            print(swaps)
            break
        p += 1
        if p % 1000 == 0:
            print(p, res)

if __name__ == "__main__":
    with open("inputs/day_24.txt") as f:
        input = f.read()
#         input = """x00: 1
# x01: 1
# x02: 1
# y00: 0
# y01: 1
# y02: 0

# x00 AND y00 -> z00
# x01 XOR y01 -> z01
# x02 OR y02 -> z02"""
#         input = """x00: 1
# x01: 0
# x02: 1
# x03: 1
# x04: 0
# y00: 1
# y01: 1
# y02: 1
# y03: 1
# y04: 1

# ntg XOR fgs -> mjb
# y02 OR x01 -> tnw
# kwq OR kpj -> z05
# x00 OR x03 -> fst
# tgd XOR rvg -> z01
# vdt OR tnw -> bfw
# bfw AND frj -> z10
# ffh OR nrd -> bqk
# y00 AND y03 -> djm
# y03 OR y00 -> psh
# bqk OR frj -> z08
# tnw OR fst -> frj
# gnj AND tgd -> z11
# bfw XOR mjb -> z00
# x03 OR x00 -> vdt
# gnj AND wpb -> z02
# x04 AND y00 -> kjc
# djm OR pbm -> qhw
# nrd AND vdt -> hwm
# kjc AND fst -> rvg
# y04 OR y02 -> fgs
# y01 AND x02 -> pbm
# ntg OR kjc -> kwq
# psh XOR fgs -> tgd
# qhw XOR tgd -> z09
# pbm OR djm -> kpj
# x03 XOR y03 -> ffh
# x00 XOR y04 -> ntg
# bfw OR bqk -> z06
# nrd XOR fgs -> wpb
# frj XOR qhw -> z04
# bqk OR frj -> z07
# y03 OR x01 -> nrd
# hwm AND bqk -> z03
# tgd XOR rvg -> z12
# tnw OR pbm -> gnj"""
        # wires = wires.splitlines()
        # gates = gates.splitlines()
        wires, gates = create_input(input)
        # print(wires, "< wires")
        # print(gates, "< gates")
        # wires = run_machine(wires, gates)
        # print(wires)
        # out_1 = calc_num(wires)
        # print(out_1, "< part 1")
        # test(wires, gates)
        # find_potential_swaps(wires, gates)
        # test_swap(wires, gates, [["rvg", "fgs"], ["tgd", "qhw"], ["djm", "ntg"], ["kjc", "z05"]])
        # take_2(wires, gates)
        take_3(wires, gates)
        # part_2(wires, gates)
