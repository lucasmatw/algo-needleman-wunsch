import itertools

import numpy as np
from Bio import pairwise2, SeqIO
from enum import Enum
import matplotlib.pyplot as plt

# aln = pairwise2.align.globalxx("AAT", "ATT")
# print(aln[0].score)
#
# print(aln[0].seqA)
# print(aln[0].seqB)
from grasp import generate_initial_solutions
from local_search import LocalSearch
from model.grasp_conf import GraspConfig
from model.score_matrix import ScoreMatrix
from model.sequence import SequenceParser


parser = SequenceParser()

#### from file
f_aln = SeqIO.parse("my_fasta.fasta", "fasta")

file_seqs = []

for aln in f_aln:
    file_seqs.append(str(aln.seq))

####


seqs = parser.parse_list(file_seqs)  # parser.parse_list(seqs_str)

solutions = generate_initial_solutions(seqs)

conf = GraspConfig()
score_mtx = ScoreMatrix()

search = LocalSearch(conf, score_mtx, solutions)

best = search.find_best()

print(str(best[0]))

solutions_list = best[1]

