import matplotlib.pyplot as plt


def plot_metric(metric_dict, metric_name):
    figure, ax = plt.subplots()

    ax.bar(range(len(metric_dict)), list(metric_dict.values()))
    ax.set_xticks(range(len(metric_dict)))
    ax.set_xticklabels(list(metric_dict.keys()))
    ax.set_title(f"Plot bar for {metric_name.capitalize()} metric")
    ax.set_xlabel(metric_name)
    ax.set_ylabel("Occurences")

    return figure


if __name__ == "__main__":
    level_dict = {
        "INFO": 3,
        "WARNING": 2,
        "ERROR": 1,
    }

    level_plot = plot_metric(level_dict, "level")

    plt.show()
