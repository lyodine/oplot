from typing import Optional, Callable
import numpy as np
from .oplot import contour
from .oplot import Vec1D, Vec2D
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import Collection
from collections import deque
from pathlib import Path


def plot_positions(data: Vec1D | Vec2D,
                   objective: Optional[Callable[[float, float], float]] = None,
                   *,
                   override_region: tuple[tuple[float, float],
                                          tuple[float, float]] = None,
                   override_margin: Optional[float] = None):
    """Plot a sequence of collections of points as they
    change over time.

    Args:
        data: Either a 2-D tensor or a 3-D tensor.

            * If :arg:`data` is 2-D: data[t] is a single point. Plot
              its change over time.

            * If :arg:`data` is 3-D: data[t] is a collection oof
              points. Plot the change of these points over
              time.

        objective: An objective function to be plotted as background.

        override_region: Only plot points that fall in this region.
            Has form ``((x_min, x_max), (y_min, y_max))``.

        override_margin: A small margin to add to override_region.
            Might make the plot prettier.
    """
    mort = np.array(data)

    margin: float = 1 if override_margin is None\
        else override_margin

    x_min: float
    x_max: float
    y_min: float
    y_max: float

    x_min = np.min(mort.T[0])
    x_max = np.max(mort.T[0])
    y_min = np.min(mort.T[1])
    y_max = np.max(mort.T[1])

    if (override_region is not None):
        x_min = override_region[0][0]
        x_max = override_region[0][1]
        y_min = override_region[1][0]
        y_max = override_region[1][1]

        mort =\
            np.apply_along_axis(func1d=lambda arr: [
                arr[0] if x_min < arr[0] < x_max else np.nan,
                arr[1] if y_min < arr[1] < y_max else np.nan],
                axis=2 if len(mort.shape) == 3 else 1,
                arr=mort)
    # Adjust margins. Matplotlib does not plot ticks that intersect
    #   with borders of the graph; this trick makes plots prettier.
    x_min -= margin
    y_min -= margin
    x_max += margin
    y_max += margin

    if objective is not None:
        contour(fun=lambda x, y: objective(x, y),
                x_range=(x_min, x_max),
                y_range=(y_min, y_max))  # type: ignore

    for i in range(len(mort)):
        _xs: float
        _ys: float
        _xs, _ys = np.array(mort[i]).T
        _intensity: float = i / len(mort)
        plt.scatter(_xs, _ys, s=9,
                    color=mpl.colormaps['RdYlGn'](_intensity),
                    alpha=0.5)  # type: ignore

    plt.xlim((x_min + margin, x_max - margin))
    plt.ylim((y_min + margin, y_max - margin))


def plot_fitnesses(
        data: Vec2D,
        best_selector: Callable[[Vec2D],
                                np.float64] = np.max,
        best_label: str = "Best value",
        all_label: str = "All values",) -> None:
    """Plot a sequence of numbers against the best one.
    The "best value" is plotted as a horizontal line.


    Args:
        data: A sequence of points to be plotted. Each
            data[i] should be a 2-tuple.

        best_selector: A :class:`Callable` that returns the best
            value in :arg:`data`. To plot a pre-determined, constant
            best value, let :arg:`best_selector` always return that value.

        best_label: Label for the best value.

        all_label: Label for other values.
    """
    mort = data

    plt.vlines(x=range(len(mort)),
               ymin=np.repeat(a=np.min(mort), repeats=len(mort)),
               ymax=mort,
               zorder=-9,
               linewidth=0.8)

    plt.hlines(best_selector(mort),
               xmin=0,
               xmax=len(mort),
               color="tab:green",
               label=best_label)

    plt.plot([],
             [],
             color="tab:blue",
             label=all_label)

    plt.scatter(range(len(mort)),
                mort,
                s=12,
                color="tab:blue",
                facecolors="white",)

    plt.legend()


# def plot_fitnesses(
#         data: Vec2D,
#         fitnesses: Vec1D,) -> None:
#     """
#     """
#     assert len(data) == len(fitnesses),\
#         "Fitness vector does not meet data length"\
#         f" ({len(data)} != {len(fitnesses)})"
#     plt.xlabel("Generation")
#     plt.ylabel("Fitness")

#     mort = fitnesses

#     plt.scatter(range(len(mort)),
#                 mort,
#                 s=12,
#                 color="tab:blue",
#                 facecolors="white",)

#     plt.vlines(x=range(len(mort)),
#                ymin=np.repeat(a=data, repeats=len(mort)),
#                ymax=mort,
#                zorder=-9,
#                linewidth=0.8)

#     plt.hlines(fitnesses,
#                xmin=0,
#                xmax=len(mort),
#                color="tab:green",
#                label="Best fitness ever")

#     plt.plot([],
#              [],
#              color="tab:blue",
#              label="Best fitness in generation")

#     plt.legend()


def animate_positions(
        data: Vec1D | Vec2D,
        objective: Optional[Callable[[float, float], float]] = None,
        *,
        override_region: Optional[
            tuple[tuple[float, float],
                  tuple[float, float]]] = None,
        override_margin: Optional[float] = None,
        save_as: Path = "./animation.gif"):

    if override_region is not None:
        x_rect_lb: float = override_region[0][0]
        x_rect_ub: float = override_region[0][1]
        y_rect_lb: float = override_region[1][0]
        y_rect_ub: float = override_region[1][1]
    else:
        x_rect_lb, y_rect_lb =\
            np.min(data, axis=(0, 1))
        x_rect_ub, y_rect_ub =\
            np.max(data, axis=(0, 1))

    margin: float = 1 if override_margin is None\
        else override_margin

    fig, ax = plt.subplots()

    ax.set_xlim(x_rect_lb, x_rect_ub)
    ax.set_ylim(y_rect_lb, y_rect_ub)

    #: Keeping type correctness at all cost.
    artists_to_remove: deque[Collection] = deque()
    if objective is not None:
        contour(objective,  # type: ignore
                x_range=(x_rect_lb - margin,
                         x_rect_ub + margin),
                y_range=(y_rect_lb - margin,
                         y_rect_ub + margin))

    def _animate_frame(i: int):
        while artists_to_remove:
            artists_to_remove.pop().remove()

        ax.set_xlim(x_rect_lb, x_rect_ub)
        ax.set_ylim(y_rect_lb, y_rect_ub)
        _xs, _ys = np.array(data[i]).T
        _intensity = i / len(data)
        new_artist = plt.scatter(
            _xs,
            _ys,
            s=1,
            color=mpl.colormaps['RdYlGn'](_intensity))  # type: ignore
        artists_to_remove.append(new_artist)
        return [new_artist]

    ani = FuncAnimation(fig, _animate_frame,
                        frames=len(data),
                        blit=True,  # Supposedly "optimises drawing"
                        repeat=False,
                        interval=400,
                        cache_frame_data=False)

    # See here https://matplotlib.org/stable/api/animation_api.html
    #   for available writers. PillowWriter is chosen here arbitrarily.
    ani.save(save_as,
             dpi=300,
             writer=PillowWriter(fps=25))
