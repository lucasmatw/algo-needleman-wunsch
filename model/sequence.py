import enum

from Bio import SeqIO


class SequenceElem(enum.Enum):
    T = 'T'
    A = 'A'
    G = 'G'
    C = 'C'
    GAP = '_'

    @staticmethod
    def of(char):
        return SequenceElem(char)

    def __str__(self):
        return self.value


class Sequence:
    def __init__(self, elems):
        self.elems = elems

    def __str__(self):
        return ''.join(map(str, self.elems))

    def __repr__(self):
        return ''.join(map(str, self.elems))

    def __len__(self):
        return len(self.elems)

    def __eq__(self, other):
        return self.elems == other.elems

    def get(self, idx):
        return self.elems[idx]


class NamedSequence:
    def __init__(self, seq_id, sequence):
        self.seq_id = seq_id
        self.sequence = sequence

    def __str__(self):
        seq_str = str(self.sequence)
        if len(seq_str) > 20:
            seq_str = seq_str[:20] + "...]"

        return "id: " + str(self.seq_id) + ": " + seq_str

    def __repr__(self):
        seq_str = str(self.sequence)
        if len(seq_str) > 20:
            seq_str = seq_str[:20] + "...]"

        return "id: " + str(self.seq_id) + ": " + seq_str

    def __eq__(self, other):
        return self.seq_id == other.seq_id

    def __len__(self):
        return len(self.sequence)

    def get(self, idx):
        return self.sequence.get(idx)


class ScoredSequence:
    """ mantiene la relacion entre una lista de NamedSequence y un score """
    def __init__(self, sequences_list, score):
        self.sequences_list = sequences_list
        self.score = score

    def __str__(self):
        return "Score: " + str(self.score) + ", seq: " + str(self.sequences_list)

    def __repr__(self):
        return "Score: " + str(self.score) + ", seq: " + str(self.sequences_list)


class SequenceParser:
    def parse(self, string_sequence):
        sequence_elems = [SequenceElem.of(char) for char in string_sequence]
        return Sequence(sequence_elems)

    def parse_list(self, string_sequence_list):

        named_sequences = []

        for i in range(0, len(string_sequence_list)):
            named_sequences.append(NamedSequence(i, self.parse(string_sequence_list[i])))

        return named_sequences

    def parse_file(self, fasta_file_name):
        f_aln = SeqIO.parse(fasta_file_name, "fasta")

        file_seqs = []

        for aln in f_aln:
            file_seqs.append(str(aln.seq))

        return self.parse_list(file_seqs)
