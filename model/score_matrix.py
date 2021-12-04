from model.sequence import SequenceElem


class ScoreMatrix:
    def __init__(self):
        self.matrix = self.__build_score_matrix()

    def __build_score_matrix(self):
        matrix = {}
        for elem_a in SequenceElem:
            for elem_b in SequenceElem:
                key = self.__get_elems_score_key(elem_a, elem_b)
                score = 0
                if elem_a == elem_b:
                    score = 1

                matrix[key] = score

        return matrix

    def __get_elems_score_key(self, elem_a, elem_b):
        return str(elem_a) + str(elem_b)

    def get_match_score(self, elem_a, elem_b):
        return self.matrix[self.__get_elems_score_key(elem_a, elem_b)]

