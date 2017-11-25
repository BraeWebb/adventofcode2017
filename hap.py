#!python3

import os, sys
from enum import Enum
import subprocess
from shutil import copyfile
import timeit
import argparse
import re

ROOT_DIR = "."
DIRECTORY_STRUCTURE = ["*.py", "*.in"]
TIMEOUT = 60
PYTHON_FILE = "*.py"
INPUT_FILE = "*.in"
LOAD_CMD = "load"
TIMES = 10
TIMER_TIMEOUT = 6
TEMPLATE_FILE = "day"

class LogLevel(Enum):
    """
    Different levels of debugging and their associated colours.
    """
    DEBUG = '\033[94m'
    SUCCESS = '\033[92m'
    LOG = ''
    WARNING = '\033[93m'
    ERROR = '\033[91m'

def log(message, level=LogLevel.LOG):
    """
    Function to abstract the logging of messages to the console.

    Parameters:
        message (str): The message to log.
        level (LogLevel, optional): The logging level of the message.
    """
    print(level.value + str(message) + '\033[0m')
    sys.stdout.flush()

def verify(root, structure, day):
    """
    Ensure that the root directory matches the provided structure.

    An example structure may look like this:
    STRUCTURE = ['rootfile.py', '*.py', 'input.txt',
                 ('output', ['out', 'sysout.c',
                             ('resources', ['image.png'])])]

    If root = . and day = day1 then these files would be searched for:

    ./
    ./rootfile.py
    ./day1.py
    ./input.txt
    ./output/
    ./output/out
    ./output/sysout.c
    ./output/resources/
    ./output/resources/image.png

    Parameters:
        root (str): The root directory to search.
        structure (list<str or tuple>): As described above.
        day (str): The day to replace wildcards with.
    """
    not_found = []
    
    if not os.path.isdir(root):
        not_found.append(root)
        
    for file in structure:
        if isinstance(file, tuple):
            folder = root + "/" + file[0].replace("*", day)
            not_found += verify(folder, file[1], day)
        else:
            file = root + "/" + file.replace("*", day)
            if not os.path.isfile(file):
                not_found.append(file)

    return not_found
            

def run_day(day, time=False, timeout=TIMEOUT):
    """
    Verify and run a day script.

    Parameters:
        day (str): The day to run.
    """
    # verify the directory structure
    root = day
    day = day.split('/')[-1]
    not_found = verify(root, DIRECTORY_STRUCTURE, day)

    if len(not_found) > 0:
        for file in not_found:
            log(f"Failed to find {file}", level=LogLevel.ERROR)
        log(f"Skipping {day}.", level=LogLevel.WARNING)
        log("")
        return
    else:
        log(f"{day} directory verified.", level=LogLevel.SUCCESS)

    python_file = f"{root}/{PYTHON_FILE.replace('*', day)}"
    input_file = f"{root}/{INPUT_FILE.replace('*', day)}"
    
    with open(input_file) as f:
        file_input = f.read()

    def run_process(timeout=timeout):
        process = subprocess.run(["python3", python_file],
                                 input=file_input,
                                 encoding='utf-8',
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 timeout=timeout)
        return process

    if time:
        timer = timeit.Timer(lambda: run_process(timeout=TIMER_TIMEOUT))
        try:
            log(f"{day} ran in {timer.timeit(TIMES)/TIMES:.4f} seconds.",
                level=LogLevel.SUCCESS)
        except subprocess.TimeoutExpired:
            log(f"{day} timed out measuring time taken", level=LogLevel.WARNING)

        log("")

    log(f"{day} output:")
    try:
        log(run_process().stdout, LogLevel.DEBUG)
    except subprocess.TimeoutExpired:
        log(f"{day} timed out after {timeout} seconds", level=LogLevel.WARNING)
        log("")
    
def make_day(day):
    root = day
    day = day.split('/')[-1]
    
    os.mkdir(root)

    python_file = f"{root}/{PYTHON_FILE.replace('*', day)}"
    input_file = f"{root}/{INPUT_FILE.replace('*', day)}"
    
    with open(input_file, "w+") as file:
        file.write('')

    copyfile(TEMPLATE_FILE, python_file)

def natural_sort(l):
    # credit https://stackoverflow.com/a/4836734
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def main():
    """
    Run the loader. If arguments are provided attempt to run those days
    otherwise attempt to run all directories in the current folder.

    Example Usage:
        # load all files in the current directory
        ./hap.py

        # load day 12 only
        ./hap.py day12
        
        # load days 12, 13 and 14
        ./hap.py day12 day13 day14

        # load day 21 in a different directory
        ./hap.py ../otherdir/day21
    """
    parser = argparse.ArgumentParser(description="Run Advent of Code Scripts")
    
    parser.add_argument('-l', '--load-day', dest='load', action='store_true',
                        help='generate new day directories')
    parser.add_argument('-t', '--time', dest='timeit', action='store_true',
                        help='time how long days take to run')
    parser.add_argument('-to', '--timeout',
                        dest='timeout', type=int, default=60,
                        help='specify timeout for running a day (default: 60)')
    parser.add_argument('days', nargs='*', help='days to run')
    
    args = parser.parse_args()
    if args.load:
        for day in args.days:
            make_day(day)
        return

    days = args.days
    if len(args.days) == 0:
        days = natural_sort([d for d in os.listdir(ROOT_DIR)
                             if os.path.isdir(d)
                             and not d.startswith('.')]) 

    for day in days:
        log(f"Loading {day}...")
        run_day(day, time=args.timeit, timeout=args.timeout)

if __name__ == "__main__":
    main()
