import numpy as np
from Bio import pairwise2, SeqIO
from enum import Enum

aln = pairwise2.align.globalxx("AAT", "ATT")
print(aln[0].score)

print(aln[0].seqA)
print(aln[0].seqB)