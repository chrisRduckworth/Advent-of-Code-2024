def count_pos(map):
    height = len(map)
    width = len(map[0])
    pos = complex("".join(map).find("^") %
                  width, "".join(map).find("^") // width)

    def replace_step(pos, m=map):
        # replaces the character in the string with an X
        x, y = int(pos.real), int(pos.imag)
        m[y] = m[y][:x] + "X" + m[y][x+1:]
        return

    dir = -1j
    while 0 <= pos.real < width and 0 <= pos.imag < height:
        if map[int(pos.imag)][int(pos.real)] == "#":
            # turn
            pos -= dir
            dir = dir * 1j
            pass
        else:
            replace_step(pos)
            pos += dir

    return "".join(map).count("X")


# after attempting to be clever for a while, I just used brute force

def count_loops(map):
    # lets just put an O in each space and see if it forms a loop
    height = len(map)
    width = len(map[0])
    start = complex("".join(map).find("^") %
                    width, "".join(map).find("^") // width)
    loops = 0
    # obstruction location is an integer because it's easier to increment
    obs_loc = 0

    while obs_loc < width * height:
        pos = start
        dir = -1j

        obs_x, obs_y = obs_loc % width, obs_loc // width
        if map[obs_x][obs_y] == "#" or map[obs_x][obs_y] == "^":
            # we can skip this space to save time
            pass

        cached_row = map[obs_y]
        # add the obstruction
        map[obs_y] = map[obs_y][:obs_x] + "#" + map[obs_y][obs_x+1:]

        # test the obstruction to see if we find a loop
        visited = set()
        loop = False
        while True:
            next_pos = pos + dir
            n_x, n_y = int(next_pos.real), int(next_pos.imag)
            if n_x < 0 or n_x >= width or n_y < 0 or n_y >= height:
                # out of the grid, so no loop
                break
            elif map[n_y][n_x] == "#":
                # about to hit an obstacle, so turn
                dir *= 1j
            else:
                # take a step
                pos = next_pos

            if (pos, dir) in visited:
                # formed a loop
                loop = True
                break

            visited.add((pos, dir))

        if loop:
            loops += 1
        obs_loc += 1

        map[obs_y] = cached_row

    return loops


if __name__ == "__main__":
    with open("inputs/day_6.txt") as f:
        map = [l.strip() for l in f.readlines()]
        steps = count_pos(map)
        print(steps, "< steps")
    
    # need to reread the file because part 1 wasn't pure (oops)
    with open("inputs/day_6.txt") as f:
        map = [l.strip() for l in f.readlines()]
        obs = count_loops(map)
        print(obs, "< obs")
