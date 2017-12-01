import sys

def sum_matching(line, index_func=lambda i: i + 1):
    """
    Computes the sum of matching pairs in a circular list.

    A matching pair is when a number equals the number found at index_func(i)
    in the list, where i is the numbers index and index_func is the provided
    function. By default this is the next number, i.e. i + 1.

    Parameters:
        line (str): A string of numbers.
        index_func (func): The function used to find a numbers match.

    Returns:
        (int): The sum of matching pairs.
    """
    max = len(line)
    sum = 0
    for i, num in enumerate(line):
        if num == line[index_func(i) % max]:
            sum += int(num)
    return sum

def run(stdin):
    """
    Takes problem input and yields solutions.

    Parameters:
        stdin (str): The input to the problem as a string.

    Yields:
        (*): The solutions to the problem.
    """
    line = stdin.splitlines()[0]
    max = len(line)

    yield sum_matching(line)
    yield sum_matching(line, index_func=lambda i: i + (max // 2))

if __name__ == "__main__":
    results = run(sys.stdin.read())
    for result in results:
        print(result)
