import sys

def sum_matching(line, index_func=lambda x: x + 1):
    max = len(line)
    sum = 0
    for i, num in enumerate(line):
        if num == line[index_func(i) % max]:
            sum += int(num)
    return sum

def run(stdin):
    line = stdin.splitlines()[0]
    max = len(line)

    print(sum_matching(line))
    print(sum_matching(line, index_func=lambda i: i + (max // 2)))

if __name__ == "__main__":
    run(sys.stdin.read())
