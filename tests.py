import loader
from algorithms import greedy


def run_algo(algo, case):
    algo(case)
    for inter in case.intersections:
        print(inter, case.intersections[inter].schedule)


def get_solution(algorithm, graph):
    solution = algorithm(graph)
    print(solution)


# run_algo(greedy, loader.load_text_file('resources\\a.txt'))
# run_algo(greedy, loader.load_text_file('resources\\d.txt'))
# żeby zobaczyć działanie time limit daj time limit np na 3 - na d.txt powinno dać krótsze schedule
