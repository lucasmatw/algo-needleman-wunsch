import enum

from Bio import pairwise2, SeqIO

from model.profile import Profile
from model.sequence import SequenceElem, SequenceParser

gap = "_"


def nw(seq_a_str, seq_b_str, score_matrix, gap_score):

    parser = SequenceParser()
    seq1 = parser.parse(seq_a_str)
    seq2 = parser.parse(seq_b_str)

    result_matrix = alignment_bu(score_matrix, gap_score, seq1, seq2)
    aln_a, aln_b = traceback(seq1, seq2, result_matrix, score_matrix)
    return aln_a, aln_b, result_matrix[-1][-1]


def nw_profile(seq_a_str, seq_b_str, score_matrix, gap_score):

    parser = SequenceParser()
    seq1 = parser.parse(seq_a_str)
    seq2 = parser.parse(seq_b_str)

    profile = Profile(0)
    profile.add_sequence(seq1)

    result_matrix = alignment_profile(score_matrix, gap_score, profile, seq2)
    profile, align_seq = traceback_profile(profile, seq2, result_matrix, score_matrix)
    return profile, align_seq, result_matrix[-1][-1]


def alignment_bu(score_matrix, gap_score, sequence1, sequence2):

    len_seq1 = len(sequence1)
    len_seq2 = len(sequence2)

    matrix = build_result_matrix(gap_score, len_seq2, len_seq1)

    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):

            prev_score = matrix[i-1][j-1]
            ma_mm_score = 0 #get_match_score(score_matrix, sequence1.get(i-1), sequence2.get(j-1))

            gap_a = matrix[i-1][j] + gap_score
            gap_b = matrix[i][j-1] + gap_score

            matrix[i][j] = max(gap_a, gap_b, prev_score + ma_mm_score)

    return matrix


def alignment_profile(score_matrix, gap_score, profile, sequence):

    len_profile = len(profile)
    len_seq = len(sequence)

    matrix = build_result_matrix(gap_score, len_profile, len_seq)

    for i in range(1, len_profile + 1):
        for j in range(1, len_seq + 1):

            prev_score = matrix[i-1][j-1]
            ma_mm_score = profile.get_match_score(score_matrix, i-1, sequence.get(j-1))

            gap_a = matrix[i-1][j] + gap_score
            gap_b = matrix[i][j-1] + gap_score

            matrix[i][j] = max(gap_a, gap_b, prev_score + ma_mm_score)

    return matrix


def build_result_matrix(gap_score, n, m):
    result_matrix = []
    for i in range(m + 1):
        row = []
        for j in range(n + 1):
            init_value = 0
            if i == 0:
                init_value = gap_score * j
            else:
                if j == 0:
                    init_value = gap_score * i
            row.append(init_value)
        result_matrix.append(row)

    return result_matrix


def printm(matrix):
    mstring = ""
    for r in matrix:
        mstring = mstring + str(r) + '\n'
    print(mstring)


def traceback(seq_a, seq_b, result_matrix, score_matrix):
    idx_a = len(seq_a)
    idx_b = len(seq_b)

    align_a = str(seq_a)
    align_b = str(seq_b)

    while idx_a > 0 or idx_b > 0:
        if is_edge(idx_a, idx_b):
            align_a, align_b, idx_a, idx_b = walk_edge(align_a, align_b, idx_a, idx_b)
        else:
            # TERMINAR TRACBACK
            diag_sum = 0 #get_match_score(score_matrix, seq_a.get(idx_a - 1), seq_b.get(idx_b - 1))
            origin = get_origin(result_matrix, diag_sum, idx_a, idx_b)


            if origin == Origin.UP:
                align_b = insert_gap(align_b, idx_b)
                idx_a -= 1
            if origin == Origin.LEFT:
                align_a = insert_gap(align_a, idx_a)
                idx_b -= 1
            if origin == Origin.DIAG:
                idx_a -= 1
                idx_b -= 1

    return align_a, align_b


def traceback_profile(profile, sequence, result_matrix, score_matrix):
    idx_a = len(profile)
    idx_b = len(sequence)

    align_seq = str(sequence)

    while idx_a > 0 or idx_b > 0:
        if is_edge(idx_a, idx_b):
            idx_a, idx_b, align_seq = walk_edge_profile(profile, sequence, align_seq, idx_a, idx_b)
        else:
            ma_mm_score = profile.get_match_score(score_matrix, idx_a - 1, sequence.get(idx_b-1))
            origin = get_origin(result_matrix, ma_mm_score, idx_a, idx_b)

            if origin == Origin.UP:
                align_seq = insert_gap(align_seq, idx_b)
                profile.add_sequence_gap(idx_b)
                idx_a -= 1

            if origin == Origin.LEFT:
                profile.add_profile_gap(sequence.get(idx_b-1), idx_a)
                idx_b -= 1

            if origin == Origin.DIAG:
                profile.add_sequence_elem(sequence.get(idx_b-1), idx_a - 1)
                idx_a -= 1
                idx_b -= 1

    return profile, align_seq


def insert_gap(string, index):
    return string[:index] + gap + string[index:]


def get_origin(result_matrix, ma_mm_score, idx_a, idx_b):

    prev_diag_score = result_matrix[idx_a - 1][idx_b - 1]

    up_val = (Origin.UP, result_matrix[idx_a - 1][idx_b])
    left_val = (Origin.LEFT, result_matrix[idx_a][idx_b - 1])
    diag_val = (Origin.DIAG, prev_diag_score + ma_mm_score)

    origin = max((left_val, up_val, diag_val), key=lambda x: x[1])

    return origin[0]


def is_edge(idx_a, idx_b):
    return max(idx_a, idx_b) > 0 and min(idx_a, idx_b) == 0


def walk_edge(align_a, align_b, idx_a, idx_b):
    if idx_a == 0:
        return gap + align_a, align_b, idx_a, idx_b - 1
    else:
        return align_a, gap + align_b, idx_a - 1, idx_b


def walk_edge_profile(profile, sequence, align_seq, idx_a, idx_b):
    if idx_a == 0:
        seq_elem = sequence.get(idx_b - 1)
        profile.add_profile_gap(seq_elem, idx_a)
        return idx_a, idx_b - 1, align_seq
    else:
        profile.add_sequence_gap(idx_a - 1)
        return idx_a - 1, idx_b, gap + align_seq


class Origin(enum.Enum):
    UP = 0
    LEFT = 1
    DIAG = 2


