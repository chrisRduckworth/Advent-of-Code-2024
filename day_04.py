import re


def count_xmas(wordsearch):
    width = len(wordsearch[0])
    height = len(wordsearch)
    count = 0
    # horizontal
    for l in wordsearch:
        count += l.count("XMAS") + l[::-1].count("XMAS")
    # vertical
    for x in range(width):
        col = "".join(l[x] for l in wordsearch)
        count += col.count("XMAS") + col[::-1].count("XMAS")
    # top left to bottom right diagonal
    for x in range(width):
        diagonal = "".join(wordsearch[d][x+d] for d in range(width - x))
        count += diagonal.count("XMAS") + diagonal[::-1].count("XMAS")
    for y in range(1, height):
        diagonal = "".join(wordsearch[y+d][d] for d in range(height - y))
        count += diagonal.count("XMAS") + diagonal[::-1].count("XMAS")
    # top right to bottom left diagonal
    for x in range(width):
        diagonal = "".join(wordsearch[d][x - d] for d in range(x + 1))
        count += diagonal.count("XMAS") + diagonal[::-1].count("XMAS")
    for y in range(1, height):
        diagonal = "".join(wordsearch[y+d][width - d - 1]
                           for d in range(height - y))
        count += diagonal.count("XMAS") + diagonal[::-1].count("XMAS")
    return count


def count_x_mas(wordsearch):
    # create 3x3 chunks of letters, then check for the pattern
    # The magic regex (I'm very pleased with this):
    # ((M)|S).((M)|S).A.(?(4)S|(?(3)M)).(?(2)S|(?(1)M))
    width = len(wordsearch[0])
    height = len(wordsearch)
    count = 0
    reg = re.compile(r'((M)|S).((M)|S).A.(?(4)S|(?(3)M)).(?(2)S|(?(1)M))')
    for x in range(width - 2):
        for y in range(height - 2):
            line_1 = wordsearch[y][x:x+3]
            line_2 = wordsearch[y+1][x:x+3]
            line_3 = wordsearch[y+2][x:x+3]
            block = line_1 + line_2 + line_3
            if reg.match(block):
                count += 1
    return count


if __name__ == "__main__":
    with open("inputs/day_04.txt") as f:
        ws = [s.strip() for s in f.readlines()]
        count = count_xmas(ws)
        print(count, "< xmas count")
        count_2 = count_x_mas(ws)
        print(count_2, "< x_mas count")  # 1758 is incorect
