from algorithms import *
from loader import load_text_file

test_graph = load_text_file("resources\\a.txt")
greedy2(test_graph)
test_graph.evaluate()
