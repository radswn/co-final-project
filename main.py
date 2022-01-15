from algorithms import *
from loader import load_text_file
from tests import run_all_tests

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']
TEST = False
OUTPUT_TO_FILE = True

if TEST:
    run_all_tests()
    exit()

graphs = {
    letter: load_text_file("resources\\{}.txt".format(letter)) for letter in LETTERS
}

solutions = {
    letter: genetic_algorithm(graphs[letter]) for letter in LETTERS
}

if OUTPUT_TO_FILE:
    [save_to_file(letter, solution) for letter, solution in solutions.items()]
else:
    results = {
        letter: approximate_fitness(graphs[letter], solutions[letter]) for letter in LETTERS
    }
    print(results)
