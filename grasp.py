import itertools
from alignment import alignment_profile, printm, nw_profile, build_result_matrix, nw_list
from model.grasp_conf import GraspConfig
from model.score_matrix import ScoreMatrix
import random


def generate_initial_solutions(named_sequences):
    """ generar soluciones iniciales *distintas* para luego ejecutarles busqueda local """

    print("Generating initial solutions")
    score_mtx = ScoreMatrix()
    conf = GraspConfig()

    couples = best_couples(conf, named_sequences, score_mtx)

    print("Best couples found: " + str(couples))

    starter_couples = select_starter_couples(conf, couples, len(named_sequences))

    print("Selected started couples: " + str(starter_couples))

    ordered_sequences = select_followers(conf, starter_couples, named_sequences)

    print("Initial solutions size:  " + str(len(ordered_sequences)) + ", seqs: " + str(ordered_sequences))

    return ordered_sequences


# return List<ScoredCouple>
def best_couples(conf, named_sequences, score_m):
    """ listado de parejas alineadas ordenado por score (acotado por configuracion) """

    couples = generate_couples(conf, named_sequences)
    print("Couples to calculate: " + str(len(couples)))

    result_list = []

    for couple in couples:
        seqs = [couple[0].sequence, couple[1].sequence]
        nw_result = nw_list(seqs, score_m)
        result_list.append(ScoredCouple(couple, nw_result.score))

    best_scores = sorted(result_list, key=lambda sc: sc.score, reverse=True)

    taken = []
    for scored_couple in best_scores:
        if scored_couple.couple[0].seq_id not in taken and scored_couple.couple[1].seq_id not in taken:
            taken.append(scored_couple)

    return taken


# return List(NamedSequence, NamedSequence)
def generate_couples(conf, elems):
    max_couples = conf.max_couples
    result = []
    for i in range(0, len(elems)):
        for j in range(i+1, len(elems)):
            result.append((elems[i], elems[j]))
            if len(result) == max_couples:
                return result

    return result


def select_starter_couples(conf, couples, total_sequences):
    """ elegir distintas parejas que van a encabezar los alineamientos """
    print("Selecting starter couples from len of " + str(total_sequences) + " with size: " + str(conf.initial_size))

    to_take = int(round(total_sequences * conf.initial_size, 0))

    score_distribution = create_score_distribution(to_take, couples)

    return select_couple_with_distribution(score_distribution, couples)


def create_score_distribution(to_take, couples):
    """ crear una distribucion del score en base al maximo y el minimo del score entre parejas iniciales """

    print("Calculating score distribution...")
    print("take: " + str(to_take))
    print("couples: " + str(len(couples)))

    max_score = max(couples, key=lambda sc: sc.score)
    min_score = min(couples, key=lambda sc: sc.score)

    print("max_score: " + str(max_score))
    print("min_score: " + str(min_score))

    partition_size = max(int(round((max_score.score - min_score.score) / to_take)), 1)

    return list(range(int(min_score.score), int(max_score.score), partition_size))


def select_couple_with_distribution(score_distribution, scored_couples):
    """ poder elegir parejas cercanas a la distribucion del score """

    selected_couples = []
    selected_seqs = []

    if len(score_distribution) == 0:
        raise "Not enough score distribution"

    sorted_score = sorted(score_distribution, reverse=True)
    current_score = sorted_score.pop()

    sorted_couples = sorted(scored_couples, key=lambda sc: sc.score)

    for scored_couple in sorted_couples:
        couple = scored_couple.couple
        if scored_couple.score > current_score and couple[0] not in selected_seqs and couple[1] not in selected_seqs:

            selected_couples.append(scored_couple)
            selected_seqs.append(couple[0])
            selected_seqs.append(couple[1])

            if len(sorted_score) == 0:
                return selected_couples

            current_score = sorted_score.pop()

    return selected_couples


def select_followers(conf, starter_couples, named_sequences):
    """ seleccionar el orden para las siguientes cadenas de cada pareja """
    couple_with_remaining_tuples = get_lists_with_couples(starter_couples, named_sequences)
    sequences_lists = []

    for couple_list_tuple in couple_with_remaining_tuples:

        # la idea era agregar otro orden arbitrario para el resto de las sequencias
        # random.shuffle(couple_list_tuple[1])

        seq_list = couple_list_tuple[0] + couple_list_tuple[1]
        sequences_lists.append(seq_list)

    return sequences_lists


def get_lists_with_couples(starter_couples, named_sequences):
    """ armar una lista con cada pareja, y devolver las cadenas restantes para cada caso """

    couples_lists = []

    list_and_remaining = []

    for scored_couple in starter_couples:

        named_sequences_copy = named_sequences.copy()
        seq1 = scored_couple.couple[0]
        seq2 = scored_couple.couple[1]

        couples_lists.append([seq1, seq2])

        if seq1 in named_sequences_copy:
            named_sequences_copy.remove(seq1)
        if seq2 in named_sequences_copy:
            named_sequences_copy.remove(seq2)

        list_and_remaining.append(([seq1, seq2], named_sequences_copy))

    return list_and_remaining


class ScoredCouple:
    def __init__(self, couple, score):
        self.couple = couple
        self.score = score

    def __str__(self):
        return str(self.couple) + ", score: " + str(self.score)

    def __repr__(self):
        return str(self.couple) + ", score: " + str(self.score)
