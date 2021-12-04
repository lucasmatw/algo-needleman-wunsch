from alignment import alignment_profile, printm, nw_profile
from model.profile import Profile
from model.score_matrix import ScoreMatrix
from model.sequence import SequenceParser, SequenceElem

parser = SequenceParser()

seq = parser.parse("AA")
seq2 = parser.parse("AG")
seq3 = parser.parse("AAAAAA")


prof = Profile(2)


score_m = ScoreMatrix()

prof.add_sequence(seq)
prof.add_sequence(seq)
prof.add_sequence(seq2)

# def alignment_profile(score_matrix, gap_score, profile, sequence):

#result = alignment_profile(score_m, 0, prof, seq2)
result = nw_profile("ATT", "AGG", score_m, 0)

# A T T _ _
# A _ _ G G

print(result[0])
print(result[1])
print(result[2])







