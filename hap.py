#!python3

import os, sys
from enum import Enum
import subprocess
from shutil import copyfile
import timeit
import argparse
import re
from collections import OrderedDict

# the default directory to search
ROOT_DIR = "."
# the required structure of each day directory
DIRECTORY_STRUCTURE = ["*.py", "*.c", "*.in", "*.java"]

# default timeout
TIMEOUT = 60
# amount of times to run to test speed
TIMES = 10
# timeout for time trials
TIMER_TIMEOUT = 6

# input file
INPUT_FILE = "*.in"

# python files
PYTHON_FILE = "*.py"
PYTHON_TEMPLATE = "day.py"

# c files
C_FILE = "*.c"
C_TEMPLATE = "day.c"

# java files
JAVA_FILE = "*.java"
JAVA_TEMPLATE = "day.java"

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
            

def run_day(day, time=False, timeout=TIMEOUT, programs=("py", "c", "java")):
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

    c_file = f"{root}/{C_FILE.replace('*', day)}"
    c_out_file = c_file.replace('.c', '.exe')

    java_file = f"{root}/{JAVA_FILE.replace('*', day)}"

    input_file = f"{root}/{INPUT_FILE.replace('*', day)}"
    
    with open(input_file) as f:
        file_input = f.read()

    run = OrderedDict([("py",
                        (False, ("python3", python_file))),
                       ("c",
                        (("make", "build", f"DAY={day}"), c_out_file)),
                       ("java",
                        (("javac", java_file), ("java", "-cp", day, day)))])

    def compile(args):
        process = subprocess.run(args, encoding='utf-8',
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        if process.stderr:
            log(process.stderr, level=LogLevel.ERROR)
        log(process.stdout)



    def run_process(timeout=timeout, label="py"):
        try:
            process = subprocess.run(run[label][1],
                                     input=file_input,
                                     encoding='utf-8',
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     timeout=timeout)
            return process
        except subprocess.TimeoutExpired:
            log(f"{day}.{label} timed out after {timeout} seconds",
                level=LogLevel.WARNING)
            log("")

    for label in programs:
        if label not in run:
            log(f"{label} is not a valid program.", level=LogLevel.ERROR)
            return

        if run[label][0]:
            compile(run[label][0])

        if time:
            timer = timeit.Timer(lambda: run_process(timeout=TIMER_TIMEOUT,
                                                     label=label))
            log(f"{day}.{label} ran in {timer.timeit(TIMES)/TIMES:.4f} seconds.",
                level=LogLevel.SUCCESS)

        log(f"{day}.{label} output:")
        process = run_process(label=label)
        if process is not None:
            if process.stderr:
                log(process.stderr, LogLevel.ERROR)
            log(process.stdout, LogLevel.DEBUG)

    
def make_day(day):
    root = day
    day = day.split('/')[-1]

    if os.path.isdir(root):
        log(f"{day} already exists", level=LogLevel.ERROR)
        return
    
    os.mkdir(root)

    python_file = f"{root}/{PYTHON_FILE.replace('*', day)}"
    c_file = f"{root}/{C_FILE.replace('*', day)}"
    java_file = f"{root}/{JAVA_FILE.replace('*', day)}"
    input_file = f"{root}/{INPUT_FILE.replace('*', day)}"
    
    with open(input_file, "w+") as file:
        file.write('')

    copyfile(PYTHON_TEMPLATE, python_file)
    copyfile(C_TEMPLATE, c_file)
    copyfile(JAVA_TEMPLATE, java_file)

    with open(java_file, 'r') as file:
        java_text = file.read()
    java_text = java_text.replace('{day}', day)
    with open(java_file, 'w') as file:
        file.write(java_text)

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
    
    parser.add_argument('-c', '--create', dest='create', action='store_true',
                        help='generate new day directories')
    parser.add_argument('-p', '--program', dest='programs', action='append',
                        help='which types of programs to run')
    parser.add_argument('-t', '--time', dest='timeit', action='store_true',
                        help='time how long days take to run')
    parser.add_argument('-to', '--timeout',
                        dest='timeout', type=int, default=60,
                        help='specify timeout for running a day (default: 60)')
    parser.add_argument('days', nargs='*', help='days to run')
    
    args = parser.parse_args()
    if args.create:
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
        if args.programs:
            run_day(day, time=args.timeit, timeout=args.timeout,
                    programs=args.programs)
        else:
            run_day(day, time=args.timeit, timeout=args.timeout)

if __name__ == "__main__":
    main()
