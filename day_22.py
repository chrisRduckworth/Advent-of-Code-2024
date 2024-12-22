def calc_secret(init, count):
    secret = init
    for i in range(count):
        m = secret << 6
        secret = (m ^ secret) % 16777216
        d = secret >> 5
        secret = (d ^ secret) % 16777216
        m2 = secret << 11
        secret = (m2 ^ secret) % 16777216
    return secret


def sum_secrets(inits):
    return sum([calc_secret(n, 2000) for n in inits])

# This is a ridiculously OTT bruteforce but eh, it worked (eventually)


def create_intervals():
    intervals = set()
    for p in range(0, 10):
        for q in range(0, 10):
            for r in range(0, 10):
                for s in range(0, 10):
                    for t in range(0, 10):
                        interval = (p - q, q - r, r - s, s - t)
                        intervals.add(interval)

    return intervals


def find_first_value(interval, init, count):
    # returns the buy the first time the interval appears
    secret = init
    changes = []
    for i in range(count):
        # calculate the new secret
        m = secret << 6
        n_secret = (m ^ secret) % 16777216
        d = n_secret >> 5
        n_secret = (d ^ n_secret) % 16777216
        m2 = n_secret << 11
        n_secret = (m2 ^ n_secret) % 16777216
        n_price = n_secret % 10

        if len(changes) == 4:
            changes.pop(0)
        changes.append(n_price - (secret % 10))

        if changes == interval:
            return n_price

        secret = n_secret

    return 0


def part_2(input, count):
    intervals = create_intervals()
    max_bananas = 0
    for i, interval in enumerate(intervals):
        if i % 1000 == 1:
            print(i)
        total = sum([find_first_value(list(interval), s, count)
                    for s in input])
        if total > max_bananas:
            max_bananas = total
            print(max_bananas, interval, "< new best")

    return max_bananas


if __name__ == "__main__":
    with open("inputs/day_22.txt") as f:
        input = [int(l.replace("\n", "")) for l in f.readlines()]
        total_secrets = sum_secrets(input)
        max_bananas = part_2(input, 2000)
        print(max_bananas, "< part 2")
