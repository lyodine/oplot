import matplotlib.pyplot as plt
import matplotlib as mlp


def axis_labels(enable: bool = False) -> None:
    plt.gca().get_yaxis().set_ticks([])
    plt.gca().get_xaxis().set_ticks([])


def axis_lines(enable: bool = True) -> None:
    plt.gca().axhline(y=0, color='DimGrey', linestyle="--")
    plt.gca().axvline(x=0, color='DimGrey', linestyle="--")


def large_text(enable: bool = True) -> None:
    mlp.rc("font", size=15)
