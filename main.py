from algorithms import *
from loader import load_text_file
from tests import run_all_tests
import concurrent.futures

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']
# LETTERS = ['a', 'b', 'c', 'e', 'f']
TEST = False
OUTPUT_TO_FILE = False

def main():

    if TEST:
        run_all_tests()
        exit()

    graphs = {
        letter: load_text_file("resources\\{}.txt".format(letter)) for letter in LETTERS
    }

    graphs_arr = [load_text_file("resources\\{}.txt".format(letter)) for letter in LETTERS]

    # multiprocessing start of algorithm
    with concurrent.futures.ProcessPoolExecutor() as executor:
        start = time()
        ftrs = executor.map(hill_climbing, graphs_arr)
        # solutions = {
        #     letter: executor.submit(genetic_algorithm, args=(graphs[letter],)) for letter in LETTERS
        # }

        solutions = {}
        for f, letter in zip(ftrs, LETTERS):
            solutions[letter] = f

        stop = time()
        print(f'algorithm execution took {stop - start} seconds')

        start = time()
        results = {
            letter: approximate_fitness(graphs[letter], solutions[letter]) for letter in LETTERS
        }
        stop = time()
        [save_to_file(letter, solution) for letter, solution in solutions.items()]
        print(results)
        print(f"evaluation took {stop - start} seconds")

    # end

    # start = time()
    # solutions = {
    #     letter: genetic_algorithm(graphs[letter]) for letter in LETTERS
    # }
    # stop = time()
    # print(f'algorithm execution took {stop - start} seconds')

    # start = time()
    # results = {
    #     letter: approximate_fitness(graphs[letter], solutions[letter]) for letter in LETTERS
    # }
    # stop = time()
    #
    # [save_to_file(letter, solution) for letter, solution in solutions.items()]
    # print(results)
    # print(f"evaluation took {stop - start} seconds")


if __name__ == '__main__':
    main()
