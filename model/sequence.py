import enum


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

    def __len__(self):
        return len(self.elems)

    def get(self, idx):
        return self.elems[idx]


class SequenceParser:
    def parse(self, string_sequence):
        sequence_elems = [SequenceElem.of(char) for char in string_sequence]
        return Sequence(sequence_elems)
