import matplotlib.pyplot as plt

def plot_curve(x,y, label:str, xlabel:str, ylabel:str, title:str, show:bool = True):

    fig, ax = plt.subplots()
    ax.plot(x, y, label= label)
    ax.set_xlabel(xlabel)  # Add an x-label to the axes.
    ax.set_ylabel(ylabel)  # Add a y-label to the axes.
    ax.set_title(title)  # Add a title to the axes.
    ax.legend()
    if show:
        plt.show()
        return None
    plt.close(fig)