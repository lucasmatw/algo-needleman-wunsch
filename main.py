from grasp import generate_initial_solutions
from local_search import LocalSearch
from model.grasp_conf import GraspConfig
from model.score_matrix import ScoreMatrix
from model.sequence import SequenceParser


# Running example
from plotter import plot_grasp_solutions

conf = GraspConfig()
score_mtx = ScoreMatrix()
parser = SequenceParser()

# parse sequences from fasta file
sequences = parser.parse_file("my_fasta.fasta")

# create initial solutions
solutions = generate_initial_solutions(sequences)

local_search = LocalSearch(conf, score_mtx, solutions)

search_result = local_search.find_best()

print("Best score: " + str(search_result[0]))

# plot searches on graph
plot_grasp_solutions(search_result[1])

