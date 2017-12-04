import sys

def is_valid(phrase, condition=lambda word, words: word in words):
    """
    Determine if a phrase is valid based on the specifying condition.

    Parameters:
        phrase (str): The phrase to check for validity.
        condition (func): The condition where a phrase is not valid.

    Returns:
        (bool): True iff the phrase is valid, else False.
    """
    words = []
    for word in phrase.split(" "):
        if condition(word, words):
            return False
        words.append(word)
    return True

def is_anagram(first, second):
    """(bool) Returns True iff the second word is an anagram of the first."""
    return sorted(first) == sorted(second)

def run(stdin):
    """
    Takes problem input and yields solutions.

    Parameters:
        stdin (str): The input to the problem as a string.

    Yields:
        (*): The solutions to the problem.
    """
    # function to find if there are any anagrams of a word in a word list
    any_anagrams = lambda word, words: any(is_anagram(val, word)
                                           for val in words)

    valid_words = [0, 0]
    for line in stdin.splitlines():
        if is_valid(line):
            valid_words[0] += 1
        if is_valid(line, condition=any_anagrams):
            valid_words[1] += 1

    yield valid_words[0]
    yield valid_words[1]

if __name__ == "__main__":
    if __name__ == "__main__":
        results = run(sys.stdin.read())
        for result in results:
            print(result)
