from algorithms import *
from loader import load_text_file

test_graph = load_text_file("resources\\f.txt")
test_graph = hill_climbing(test_graph)
score = test_graph.evaluate()
print("total score", score)
