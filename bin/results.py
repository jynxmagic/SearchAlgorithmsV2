from matplotlib import pyplot as plt


def graph(searches, x_pos, xs, xlabel, ylabel, title):
    plt.bar(searches, xs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.table(title)
    plt.xticks(x_pos, searches)
    plt.show()


def time_graph(res):
    searches = res.keys()
    x_pos = [i for i, _ in enumerate(searches)]
    time_elapsed = [res[k][1] * 1000 for k in res]
    graph(
        searches,
        x_pos,
        time_elapsed,
        "Search Algorithm",
        "Time Taken (ms)",
        "Time taken for pathfinding algorithms",
    )


def cost_graph(res):
    searches = res.keys()
    x_pos = [i for i, _ in enumerate(searches)]
    cost = [res[k][3] for k in res]
    graph(
        searches,
        x_pos,
        cost,
        "Search Algorithm",
        "Total Path Cost",
        "Total Cost of each algorithm",
    )


def memory_graph(res):
    searches = res.keys()
    x_pos = [i for i, _ in enumerate(searches)]
    memory = [res[k][4] for k in res]
    graph(
        searches,
        x_pos,
        memory,
        "Search Algorithm",
        "Memory usage (bytes)",
        "Total memory usage of each algorithm",
    )
    plt.show()


def generate_graphs(results):
    """Print results using Matplotlib.

    Args:
        results ([dict]): dict with search algorithms as key and results as value
    """

    time_graph(results)
    cost_graph(results)
    memory_graph(results)
