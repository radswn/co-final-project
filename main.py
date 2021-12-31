from algorithms import *
from loader import load_text_file

test_graph = load_text_file("resources\\a.txt")
greedy2(test_graph)
score = test_graph.evaluate()
print("total score", score)
