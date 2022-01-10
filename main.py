from algorithms import *
from loader import load_text_file
from tests import run_all_tests

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']
TEST = True

if TEST:
    run_all_tests()
    exit()

graphs = {
    letter: load_text_file("resources\\{}.txt".format(letter)) for letter in LETTERS
}

start = time()
solutions = {
    letter: greedy2(graphs[letter]) for letter in LETTERS
}
stop = time()
print(f'algorithm execution took {stop - start} seconds')

start = time()
results = {
    letter: approximate_fitness(graphs[letter], solutions[letter]) for letter in LETTERS
}
stop = time()
print(results)
print(f"evaluation took {stop - start} seconds")
