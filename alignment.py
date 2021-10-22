def alignment_bu(sequence1, sequence2):

    len_seq1 = len(sequence1)
    len_seq2 = len(sequence2)

    matrix = [[0 for i in range(len_seq2 + 1)] for j in range(len_seq1 + 1)]

    for i in range(0, len_seq1 + 1):
        matrix[i][0] = i

    for i in range(0, len_seq2 + 1):
        matrix[0][i] = i

    print(str(matrix))

    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):
            if sequence1[i-1] == sequence2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]
            else:
                pad1 = matrix[i][j-1] + 1
                pad2 = matrix[i-1][j] + 1
                pad_both = matrix[i-1][j-1] + 1

                matrix[i][j] = min(pad1, pad2, pad_both)

    return matrix[len_seq1][len_seq2]


print(alignment_bu("abc", "bcc"))




