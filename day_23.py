import networkx as nx

def create_network(edges):
    network = nx.Graph()
    network.add_edges_from(edges)
    return network

def part_1(edges):
    network = create_network(edges)
    cycles = [set(c) for c in nx.simple_cycles(network, 3) if len(c) == 3]
    filtered = []
    for c in cycles:
        to_add = False
        for n in c:
            if n[0] == "t":
                to_add = True
                break
        if to_add: filtered.append(c)
    return len(filtered)

def part_2(edges):
    # this is asking for the maximal clique
    # this is an NP-complete program aka hard
    # fortunately networkx can just do it 
    network = create_network(edges)
    cliques = nx.approximation.max_clique(network)
    max_clique = [c for c in cliques if len(c) == max(len(c) for c in cliques)]
    return ",".join(sorted(max_clique))


if __name__ == "__main__":
    with open("inputs/day_23.txt") as f:
        input = [l.replace("\n", "") for l in f.readlines()]
        edges = [tuple(l.split("-")) for l in input]
        out_1 = part_1(edges)
        print(out_1, "< part 1")
        out_2 = part_2(edges)
