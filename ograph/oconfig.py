import matplotlib.pyplot as plt
import matplotlib as mlp

def axis_labels(enable=False):
    plt.gca().get_yaxis().set_ticks([])
    plt.gca().get_xaxis().set_ticks([])

def axis_lines(enable=True):
    plt.gca().axhline(y=0, color='DimGrey', linestyle="--")
    plt.gca().axvline(x=0, color='DimGrey', linestyle="--")

def large_text(enable=True):
    mlp.rc("font", size=15)