from alignment import nw_list
from model.sequence import ScoredSequence


class LocalSearch:
    def __init__(self, nw_conf, score_matrix, initial_solutions):
        self.conf = nw_conf
        self.score_matrix = score_matrix
        self.initial_solutions = initial_solutions

    def find_best(self):
        """ realiza busqueda local en cada una de las soluciones iniciales.
            Devuelve las soluciones por score de mayor a menor """

        print("Running local search")
        best_score_from_each = []

        global_registered_solutions = []

        for initial_solution in self.initial_solutions:
            print("Improving solution: S" + str(self.initial_solutions.index(initial_solution)))

            registered_solutions = []

            initial_nw_result = nw_list(initial_solution, self.score_matrix)

            best_solution = ScoredSequence(initial_solution, initial_nw_result.score)
            improved_solution = self.__find_best(best_solution.sequences_list)

            registered_solutions.append(best_solution)

            improvements = 0
            while improved_solution.score > best_solution.score:
                improvements += 1
                registered_solutions.append(improved_solution)

                best_solution = improved_solution
                improved_solution = self.__find_best(best_solution.sequences_list)

            print("Improvements found: " + str(improvements))

            print("Best solution: S" + str(self.initial_solutions.index(initial_solution)) + ": " + str(best_solution))
            best_score_from_each.append(best_solution)

            global_registered_solutions.append(registered_solutions)

        global_best = sorted(best_score_from_each, key=lambda nw: nw.score, reverse=True)[0]
        return global_best, global_registered_solutions

    def __find_best(self, named_sequences):
        """explora la vencindad de la solucion local modificando el orden de las secuencias"""

        print("Finding best for: " + str(named_sequences))
        local_named_sequences = named_sequences.copy()

        print("Get current score for total sequences alignment: " + str(len(local_named_sequences)))
        best_nw_result = nw_list(local_named_sequences, self.score_matrix)
        print("Done: " + str(best_nw_result.score))
        best_solution = ScoredSequence(local_named_sequences.copy(), best_nw_result.score)

        sequences_length = len(named_sequences)

        range_step = max(int(round(sequences_length / 5)), 1)

        improvements = 0

        print("Sarching from 0 to " + str(sequences_length - 1) + " with steps of " + str(range_step))
        for i in range(2, sequences_length - 1, range_step):

            new_sequences_order = self.change_order(local_named_sequences, i)
            new_solution = nw_list(new_sequences_order, self.score_matrix)

            if new_solution.score > best_solution.score:
                best_nw_result = nw_list(new_sequences_order, self.score_matrix)
                best_solution = ScoredSequence(new_sequences_order.copy(), best_nw_result.score)
                improvements += 1
                print("Improvement found!")

        print("Best solution found: " + str(best_solution))
        print("With improvements: " + str(improvements))
        return best_solution

    def change_order(self, named_sequences, current_index):
        copied_sequences = named_sequences.copy()
        seqs = self.__swap_elem(copied_sequences, current_index, current_index + 1)

        from_last = len(copied_sequences) - current_index
        return self.__swap_elem(seqs, from_last, from_last - 1)

    def __swap_elem(self, elems, pos_x, pos_y):
        elems[pos_x], elems[pos_y] = elems[pos_y], elems[pos_x]
        return elems
