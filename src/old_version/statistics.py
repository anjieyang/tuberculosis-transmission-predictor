import numpy
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd


def draw_degree_distribution(literally_adjacencies, save_path):
    """
    Draws a histogram of the degree distribution of the graph represented by the given adjacencies.

    Args:
        literally_adjacencies (dict): A dictionary of the graph's adjacencies, where each key represents a node and the corresponding value is a dictionary containing its adjacent nodes.
        save_path (str): The directory path to save the degree distribution plot.

    Returns:
        None
    """
    lst = [[cluster, len(adjacencies)] for cluster, adjacencies in literally_adjacencies.items()]
    degrees = pd.DataFrame(lst, columns=['Node', 'Degree'])
    sns.displot(data=degrees['Degree'], kde=False)
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.savefig(save_path + 'degree_distribution.png')



if __name__ == '__main__':
    literally_adjacencies = {0: [], 1: [2, 4, 5], 2: [1, 3], 3: [2], 4: [1], 5: [1]}
    draw_degree_distribution(literally_adjacencies)