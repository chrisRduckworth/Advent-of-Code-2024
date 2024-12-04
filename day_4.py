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
        diagonal = "".join(wordsearch[d][x -d] for d in range(x + 1))
        count += diagonal.count("XMAS") + diagonal[::-1].count("XMAS")
    for y in range(1, height):
        diagonal = "".join(wordsearch[y+d][width - d - 1] for d in range(height - y))
        count += diagonal.count("XMAS") + diagonal[::-1].count("XMAS")
    return count

if __name__ == "__main__":
    with open("day_4.txt") as f:
        ws = [s.strip() for s in f.readlines()]
        count = count_xmas(ws)
        print(count, "< count")