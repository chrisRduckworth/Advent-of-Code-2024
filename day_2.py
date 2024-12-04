def check_safe(report):
    asc = sorted(report)
    desc = sorted(report, reverse=True)
    if report != asc and report != desc:
        return False
    differences = [abs(level - report[i])
                   for i, level in enumerate(report[1:])]
    return all(d >= 1 and d <= 3 for d in differences)


def count_safe_two(r):
    reports = [[int(n) for n in l.split()] for l in r]

    count = 0

    for report in reports:
        is_safe = check_safe(report)
        if not is_safe:
            for i in range(len(report)):
                without_i = [l for j, l in enumerate(report) if i != j]
                if check_safe(without_i):
                    is_safe = True
                    break
        if is_safe:
            count += 1
    return count


def count_safe(r):
    reports = [[int(n) for n in l.split()] for l in r]
    return sum(1 for r in reports if check_safe(r))


if __name__ == "__main__":
    with open("inputs/day_2.txt") as f:
        reports = f.readlines()
        safe = count_safe(reports)
        print(safe, "< safe")
        safe_2 = count_safe_two(reports)
        print(safe_2)
