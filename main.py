from sys import argv

from algorithms import *
from loader import load_stdin


def main(chosen_algorithm):
    graph = load_stdin()
    solution = chosen_algorithm(graph)
    print(solution)


if __name__ == "__main__":
    algo = argv[1]
    if algo == 'simple':
        main(hill_climbing)
    elif algo == 'complex':
        main(genetic_algorithm)
    else:
        print('Wrong algorithm choice, possible choices: simple, complex')
        exit(1)
