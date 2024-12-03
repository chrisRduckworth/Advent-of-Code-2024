def check_safe(report):
    # check all ascending
    # for i, level in enumerate(report):
    #     if i == 0:
    #         pass
    #     if level 
    asc = sorted(report)
    desc = sorted(report, reverse=True)
    # print(report)
    # print(asc)
    # print(desc == report)
    if report != asc and report != desc:
        # print("in here")
        return False
    differences = [abs(level - report[i]) for i, level in enumerate(report[1:])]
    # print(differences)
    return all(d>=1 and d <=3 for d in differences)
    # for i, level in enumerate(report):
    #     if i == 0:
    #         pass
    #     if abs(level - report[i - 1])

# def check_safe_d(report):
#     i = 1
#     dir = ""
#     mistak

#     while i < len(report):

def count_safe_two(r):
    reports = [[int(n) for n in l.split()] for l in r]
    # reports = [[7,6,4,2,1],[1,2,7,8,9],[9,7,6,2,1],[1,3,2,4,5],[8,6,4,4,1],[1,3,6,7,9]]

    count = 0

    for report in reports:
        is_safe = check_safe(report)
        if not is_safe:
            for i in range(len(report)):
                without_i = [l for j, l in enumerate(report) if i != j]
                if check_safe(without_i):
                    is_safe = True
                    break
                    # rem = check_safe([l for j, l in enumerate(report) if i != j])
        if is_safe:
            count += 1
        print(report, is_safe)
    return count



def count_safe(r):
    reports = [[int(n) for n in l.split()] for l in r]
    # # print(reports)
    # print(check_safe([7, 6, 4, 2, 1]))
    # for report in reports:
    #     print(check_safe(report))
    return sum(1 for r in reports if check_safe(r))

if __name__ == "__main__":
    with open("inputs/day_2.txt") as f:
        reports = f.readlines()
        safe = count_safe(reports)
        print(safe, "< safe")
        safe_2 = count_safe_two(reports)
        print(safe_2)

        
