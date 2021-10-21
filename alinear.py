def alignment(sequence1, sequence2, idx1, idx2):

    if len(sequence1) == idx1:
        return len(sequence2) - idx2

    if len(sequence2) == idx2:
        return len(sequence1) - idx1

    if sequence1[idx1] == sequence2[idx2]:
        return alignment(sequence1, sequence2, idx1+1, idx2+1)

    pad1 = alignment(sequence1, sequence2, idx1, idx2+1) + 1
    pad2 = alignment(sequence1, sequence2, idx1+1, idx2) + 1
    pad_both = alignment(sequence1, sequence2, idx1+1, idx2+1) + 1

    return min(pad1, pad2, pad_both)




print(alignment("aaa", "", 0, 0))




