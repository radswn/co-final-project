from tests import get_solution
from algorithms import greedy2
from loader import load_text_file

test_graph = load_text_file("resources\\a.txt")
get_solution(greedy2, test_graph)