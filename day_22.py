from collections import defaultdict


def calc_secret(init, count):
    secret = init
    for _ in range(count):
        m = secret << 6
        secret = (m ^ secret) % 16777216
        d = secret >> 5
        secret = (d ^ secret) % 16777216
        m2 = secret << 11
        secret = (m2 ^ secret) % 16777216
    return secret


def sum_secrets(inits):
    return sum([calc_secret(n, 2000) for n in inits])


def calc_intervals(secret, bananas):
    secrets = [secret]
    for i in range(2001):
        m = secret << 6
        secret = (m ^ secret) % 16777216
        d = secret >> 5
        secret = (d ^ secret) % 16777216
        m2 = secret << 11
        secret = (m2 ^ secret) % 16777216
        secrets.append(secret)

    # for each interval of 4 changes as they appear in the sequeunce
    # of secrets, find the final price and add it to the total price
    # in bananas if it hasn't already been added
    visited = set()
    for i in range(1, 1998):
        prices = [n % 10 for n in secrets[i - 1: i + 4]]
        changes = tuple(n - prices[j] for j, n in enumerate(prices[1:]))
        if changes in visited:
            continue
        price = prices[-1]
        bananas[changes] += price
        visited.add(changes)

    return


def part_2(secrets):
    bananas = defaultdict(lambda: 0)
    for secret in secrets:
        calc_intervals(secret, bananas)
    return max(b for b in bananas.values())


if __name__ == "__main__":
    with open("inputs/day_22.txt") as f:
        input = [int(l.replace("\n", "")) for l in f.readlines()]
        total_secrets = sum_secrets(input)
        print(total_secrets, "< part 1")
        max_bananas = part_2(input)
        print(max_bananas, "< part 2")
