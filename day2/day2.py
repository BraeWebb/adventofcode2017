import sys

def checksum(lines, checksum_func=sum, separator="\t"):
    """
    Calculates the checksum of a set of lines in a spreadsheet.

    Parameters:
        lines (list<str>): The lines in the spreadsheet.
        checksum_func (func, optional): The function to calculate the checksum
                                        for each line in the spreadsheet.
                                        Default: sums all numbers.
        separator (str, optional): The character the separates numbers in
                                   the spreadsheet.
    """
    checksum = 0
    for line in lines:
        numbers = [int(num) for num in line.split(separator)]
        checksum += checksum_func(numbers)
    return checksum

def even_numbers(numbers):
    """
    Find the division of the two numbers in the numbers list that are
    evenly divisible.

    Parameters:
        numbers (list<int>): The list of numbers.

    Returns:
        (int): The division of the two evenly divisible numbers.
    """
    # TODO: Better solution?
    for num in numbers:
        for num1 in numbers:
            if num % num1 == 0 and num != num1:
                return num // num1

def run(stdin):
    """
    Takes problem input and yields solutions.

    Parameters:
        stdin (str): The input to the problem as a string.

    Yields:
        (*): The solutions to the problem.
    """
    yield checksum(stdin.splitlines(),
                   checksum_func=lambda nums: max(nums) - min(nums))
    yield checksum(stdin.splitlines(), checksum_func=even_numbers)

if __name__ == "__main__":
    if __name__ == "__main__":
        results = run(sys.stdin.read())
        for result in results:
            print(result)
