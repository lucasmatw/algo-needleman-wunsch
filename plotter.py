import matplotlib.pyplot as plt


def plot_grasp_solutions(solutions):

    for sols in solutions:

        sol_id = str(solutions.index(sols) + 1)
        xs = []
        ys = []
        for sol in sols:
            score_id = sol_id + str(sols.index(sol))
            xs.append(score_id)
            ys.append(sol.score)

        plt.plot(xs, ys, label="line " + sol_id)

    plt.xlabel('solition id')
    plt.ylabel('score')
    plt.title('GRASP')
    plt.legend()
    plt.show()
