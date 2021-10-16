from matplotlib import pyplot as plt


def generate_graphs(results):

    searches = results.keys()
    x_pos = [i for i, _ in enumerate(searches)]
    time_elapsed = [results[k][1]*100 for k in results] # removed limited algorithms

    plt.bar(searches, time_elapsed)
    plt.xlabel("Search Algorithm")
    plt.ylabel("Time Taken (ms)")
    plt.table("Time taken for path finding algorithms")
    plt.xticks(x_pos, searches)
    plt.show()
