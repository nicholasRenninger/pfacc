import matplotlib.pyplot as plt


def plot_n_vs_k(x_lists, y_lists, titleStr, saveTitle, xlabel, ylabel,
                legendStr):
    """
    plot_n_vs_k(x_lists, y_lists, titleStr, saveTitle, xlabel, ylabel,
                legendStr)
    plots the x and y data in each tuple of lists

    :param x_lists: tuple of lists of x-data for each plot
    :type x_lists: tuple(list(float), list(float))
    :param y_lists: tuple of lists of y-data for each plot
    :type y_lists: tuple(list(float), list(float))
    :param titleStr: plot title string
    :type titleStr: str
    :param saveTitle: string containing save location and filename for plot
    :type saveTitle: str
    :param xlabel: plot x-axis label string
    :type xlabel: str
    :param ylabel: plot y-axis label string
    :type ylabel: str
    :param legendStr: list of strings containing legend label for each list in
                      n_lists
    :type legendStr: str
    """

    lineStyles = ['r-', 'b:']
    plots = []
    plt.figure()

    for i in range(0, len(x_lists)):

        (x_list, y_list) = (x_lists[i], y_lists[i])

        p, = plt.plot(x_list, y_list, lineStyles[i])
        plots.append(p)

    # formatting
    plt.setp(p, 'linewidth', 3)
    plt.grid()
    plt.title(titleStr)
    plt.yscale('log')
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(plots, legendStr, loc='best')
    plt.savefig(saveTitle)
