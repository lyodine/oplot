"""
    Custom plotting library.

    A point of improvement: create a global manager pool, so that the manager count does
        not leak.
"""

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D  # type: ignore[import-untyped]
from typing import Tuple
from typing import Optional
from typing import Any


def fig2(xlims: Optional[Tuple[float, float]] = None,
         ylims: Optional[Tuple[float, float]] = None,
         *args: tuple, **kwargs: Any) -> Tuple[Figure, Axes]:
    fig = plt.figure()
    ax = plt.axes(*args, projection='rectilinear', **kwargs)
    if (xlims is not None):
        ax.set_xlim(*xlims)
    if (ylims is not None):
        ax.set_ylim(*ylims)
    return (fig, ax)


def fig3(xlims: Optional[Tuple[float, float]] = None,  # type: ignore[no-any-unimported]
         ylims: Optional[Tuple[float, float]] = None,
         zlims: Optional[Tuple[float, float]] = None,
         arg: tuple[float, float, float, float] | None = None,
         **kwargs: Any) \
        -> Tuple[Figure, Axes3D]:

    fig = plt.figure()
    ax: Axes3D = plt.axes(arg,  # type: ignore[no-any-unimported]
                          projection='3d',
                          **kwargs)

    if (xlims is not None):
        ax.set_xlim(*xlims)
    if (ylims is not None):
        ax.set_ylim(*ylims)
    if (zlims is not None):
        ax.set_zlim(*zlims)
    return (fig, ax)
