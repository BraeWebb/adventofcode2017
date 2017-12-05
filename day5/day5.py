import sys

def jump(numbers, new_value=lambda old_value: old_value + 1):
    """
    Jump between numbers in a list, replacing the last number based on the
    new_value function result.

    Parameters:
        numbers (list<int>): The numbers to jump between.
        new_value (func): A function to calculate the replacement value
                          after jumping.

    Returns:
        (int): The amount of jumps it takes to exit the bounds of the list.
    """
    numbers = numbers[:]
    current, last, count = 0, 0, 0
    while 0 <= current < len(numbers):
        last = current
        current += numbers[current]
        numbers[last] = new_value(numbers[last])
        count += 1
    return count

def run(stdin):
    """
    Takes problem input and yields solutions.

    Parameters:
        stdin (str): The input to the problem as a string.

    Yields:
        (*): The solutions to the problem.
    """
    numbers = [int(x) for x in stdin.splitlines()]
    yield jump(numbers)
    yield jump(numbers, new_value=lambda old_value: old_value + 1
                                    if old_value < 3 else old_value - 1)

if __name__ == "__main__":
    if __name__ == "__main__":
        results = run(sys.stdin.read())
        for result in results:
            print(result)
