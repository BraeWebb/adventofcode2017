import sys

def star_one(line):
    max = len(line)
    sum = 0
    for i, num in enumerate(line):
        if num == line[(i + 1) % max]:
            sum += int(num)
    return sum

def star_two(line):
    max = len(line)
    sum = 0
    midway = max // 2
    for i, num in enumerate(line):
        x = (i + midway) % max
        if num == line[x]:
            sum += int(num)
    return sum

def run(stdin):
    line = stdin.splitlines()[0]

    print(star_one(line))
    print(star_two(line))

if __name__ == "__main__":
    run(sys.stdin.read())
