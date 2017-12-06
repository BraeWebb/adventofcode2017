import sys


def find_max_index(list):
    """
    Finds the index of the maximum value in a list.

    Parameters:
        list (list<int>): The list to find a maximum within.

    Returns:
        (int): The index of the maximum value.
    """
    return max(enumerate(list), key=lambda pair: pair[1])[0]


def distribute(bank, index=0):
    """
    Distribute the number at an index throughout the rest of the bank.

    Parameters:
        bank (list<int>): The bank to distribute a number through.
        index (int): The index of the value to distribute.

    Returns:
        (list<int>): The updated bank.
    """
    value = bank[index]
    bank[index] = 0

    while value > 0:
        index += 1
        bank[index % len(bank)] += 1
        value -= 1

    return bank


def scan(bank, exit_condition=lambda bank, states, count: bank in states):
    """
    Distribute an item throughout a bank until the exit condition is reached.

    Parameters:
        bank (list<int>): The bank to scan through.
        exit_condition (func, optional): The condition where scanning should stop.

    Returns:
        (int, list<int>): The amount of iterations made and the resulting bank.
    """
    count = 0
    states = [bank]

    while True:
        bank = distribute(bank[:], index=find_max_index(bank))

        count += 1

        if exit_condition(bank, states, count):
            return count, bank

        states.append(bank)


def run(stdin):
    """
    Takes problem input and yields solutions.

    Parameters:
        stdin (str): The input to the problem as a string.

    Yields:
        (*): The solutions to the problem.
    """
    line = stdin.splitlines()[0]
    banks = list(map(int, line.split('\t')))

    count, number = scan(banks)

    yield count
    yield scan(number)[0]

if __name__ == "__main__":
    if __name__ == "__main__":
        results = run(sys.stdin.read())
        for result in results:
            print(result)
