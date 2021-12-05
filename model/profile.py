from model.sequence import SequenceElem


class Profile:
    def __init__(self, length):
        self.length = length
        self.elem_matrix_count = self.__init_matrix()
        self.sequences = 0

    def add_sequence(self, sequence):
        sequence_len = len(sequence)
        self.__check_length(sequence_len)
        for elem_idx in range(0, sequence_len):
            elem = sequence.get(elem_idx)
            self.__increase_elem_at(elem, elem_idx)

        self.sequences += 1

    def add_sequence_elem(self, elem, idx):
        self.__increase_elem_at(elem, idx)

    def get_match_score(self, score_matrix, elem_idx, seq_elem):
        fractional_score_dict = self.__get_fractional_at(elem_idx)
        total_score = 0
        for elem in fractional_score_dict:
            elem_frac_occurrence = fractional_score_dict[elem]
            match_score = score_matrix.get_match_score(elem, seq_elem)
            total_score += match_score * elem_frac_occurrence

        return round(total_score, 2)

    def __get_fractional_at(self, elem_idx):
        if elem_idx >= self.length:
            raise ValueError("Invalid index")

        fractional_dict = {}
        for elem in self.elem_matrix_count:
            fractional_result = self.elem_matrix_count[elem][elem_idx] / self.sequences
            fractional_dict[elem] = fractional_result

        return fractional_dict

    def add_sequence_gap(self, elem_idx):
        self.__increase_elem_at(SequenceElem.GAP, elem_idx)

    def add_profile_gap(self, elem, elem_idx):
        self.__insert_gap(elem_idx)
        self.__increase_elem_at(SequenceElem.GAP, elem_idx, self.sequences)
        self.__increase_elem_at(elem, elem_idx)

    def increase_sequences(self):
        self.sequences += 1

    def __insert_gap(self, elem_idx):
        for count_list in self.elem_matrix_count.values():
            self.__insert_gap_in_list(count_list, elem_idx)
        self.length += 1

    def __insert_gap_in_list(self, count_list, idx):
        count_list.insert(idx, 0)

    def __check_length(self, new_seq_length):
        delta = new_seq_length - self.length
        if delta > 0:
            self.length = new_seq_length
            for k in self.elem_matrix_count:
                self.elem_matrix_count[k] = self.elem_matrix_count[k] + ([0] * delta)

    def __increase_elem_at(self, elem, idx, amount=1):
        self.elem_matrix_count[elem][idx] += amount

    def __init_matrix(self):
        matrix = {}
        for elem in SequenceElem:
            matrix[elem] = self.__build_list()
        return matrix

    def __build_list(self):
        return [0] * self.length

    def __str__(self):
        matrix_string = ""
        for elem in self.elem_matrix_count:
            matrix_string += str(elem) + ": " + str(self.elem_matrix_count[elem]) + '\n'
        return matrix_string

    def __len__(self):
        return self.length
