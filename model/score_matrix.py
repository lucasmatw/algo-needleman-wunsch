from model.sequence import SequenceElem

match_score = 3
mismatch_score = -2
gap_score = -1


class ScoreMatrix:
    def __init__(self):
        self.matrix = self.__build_score_matrix()

    def get_match_score(self, elem_a, elem_b):

        if SequenceElem.GAP == elem_a or SequenceElem.GAP == elem_b:
            return gap_score

        return self.matrix[self.__get_elems_score_key(elem_a, elem_b)]

    def get_gap_score(self):
        return gap_score

    def __build_score_matrix(self):
        matrix = {}
        for elem_a in SequenceElem:
            for elem_b in SequenceElem:
                key = self.__get_elems_score_key(elem_a, elem_b)
                score = mismatch_score
                if elem_a == elem_b:
                    score = match_score

                matrix[key] = score

        return matrix

    def __get_elems_score_key(self, elem_a, elem_b):
        return str(elem_a) + str(elem_b)



