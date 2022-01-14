from algorithms import *
from loader import load_text_file
from tests import run_all_tests

# LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']
# LETTERS = ['a', 'b', 'c', 'e', 'f']
LETTERS = ['d']
TEST = False
OUTPUT_TO_FILE = False

if TEST:
    run_all_tests()
    exit()

graphs = {
    letter: load_text_file("resources\\{}.txt".format(letter)) for letter in LETTERS
}

start = time()
solutions = {
    letter: hill_climbing(graphs[letter]) for letter in LETTERS
}
stop = time()
print(f'algorithm execution took {stop - start} seconds')

start = time()
results = {
    letter: graphs[letter].evaluate(solutions[letter]) for letter in LETTERS
}
stop = time()

if OUTPUT_TO_FILE:
    [save_to_file(letter, solution) for letter, solution in solutions.items()]

print(results)
print(f"evaluation took {stop - start} seconds")
