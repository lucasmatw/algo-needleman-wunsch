import itertools
from alignment import alignment_profile, printm, nw_profile, nw_profile_list, build_result_matrix, nw_list
from model.profile import Profile
from model.score_matrix import ScoreMatrix

from model.sequence import SequenceParser


def permutation(string_sequences):

    score_m = ScoreMatrix()

    parser = SequenceParser()
    named_sequences = []

    for index in range(0, len(string_sequences)):
        seq = string_sequences[index]
        parsed_seq = parser.parse(seq)

        named_sequences.append(NamedSequence(index, parsed_seq))

    perms = list(itertools.permutations(named_sequences))

    scored = list(map(lambda perm: scored_seq(perm, score_m), perms))

    return max(scored, key=lambda sc: sc[1])


def scored_seq(named_sequences, score_m):
    sequences = list(map(lambda ns: ns.sequence, named_sequences))
    result = nw_list(sequences, score_m)

    return named_sequences, result[2]


class NamedSequence:
    def __init__(self, seq_id, sequence):
        self.seq_id = seq_id
        self.sequence = sequence

    def __str__(self):
        return str(self.seq_id) + ": " + str(self.sequence)
