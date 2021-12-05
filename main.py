from alignment import alignment_profile, printm, nw_profile, nw_profile_list, build_result_matrix
from grasp import permutation
from model.profile import Profile
from model.score_matrix import ScoreMatrix
from model.sequence import SequenceParser, SequenceElem
import random
import string

score_m = ScoreMatrix()

# def alignment_profile(score_matrix, gap_score, profile, sequence):

#result = alignment_profile(score_m, 0, prof, seq2)

# result = nw_profile(("GATTACA", "GTCGACGCA"), score_m)

def rand_sequences(chars = string.ascii_uppercase + string.digits, N=20):
    return ''.join(random.choice(chars) for _ in range(N))


random_sequences = list(map(lambda i: rand_sequences(chars="GTAC"), range(0, 5)))
print(str(random_sequences))

# 'TGACCCCTGTGTAGTCACAC', 'GGTTCGCCGCGACGATCGGC', 'AGACGAAGGGAGCTCTCGTA','GTTAGAGTCCCCACAAAGCA', 'GCACTGGTAACGATTCCCTA'
error_seqs = ['CA', 'GC']
#result = nw_profile_list(error_seqs, score_m)

#ver si funciona con el add sequence gap -1 en trace back

# result = nw_profile("GC", "CA", score_m)

# result = nw_profile("AGC", "CGA", score_m)


#
# print(result[0])
# print(result[1])
# print(result[2])

# winner = permutation(['GGTTCGCCGCGACGATCGGC', 'AGACGAAGGGAGCTCTCGTA', 'GTTAGAGTCCCCACAAAGCA', 'TGACCCCTGTGTAGTCACAC', 'GCACTGGTAACGATTCCCTA'])

#(["GTCGACGCA", "GTCGACGCA", "GATTACA", "GTCGACGCA"])
#

winner = permutation(['TGACCCCTGTGTAGTCACAC', 'GTTAGAGTCCCCACAAAGCA'])


for s in winner[0]:
    print(str(s))

print(winner[1])





