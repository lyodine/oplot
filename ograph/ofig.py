"""Utilities that create and check figures
of different dimensions.
"""

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D  # type: ignore[import-untyped]
from typing import Tuple
from typing import Optional
from typing import Any
import logging


def fig2(xlims: Optional[Tuple[float, float]] = None,
         ylims: Optional[Tuple[float, float]] = None,
         arg: None | tuple[float, float, float, float] = None,
         **kwargs: Any) -> Tuple[Figure, Axes]:
    """Create then return a figure with a 2-dimensional axis.

    Invoke :meth:`.pyplot.figure` to create figure, then
    invoke :meth:`.pyplot.axes` to create an :class:`Axes`.
    Return both objects in a tuple.

    Args:
        arg: :python:`None` or 4-tuple.

            - :python:`None`: A new full window Axes is added using
              ``subplot(**kwargs)``.

            - 4-tuple of floats *rect* = ``(left, bottom, width, height)``:
              Add a new Axes with dimensions *rect* in normalized
              (0, 1) units, using :meth:`Figure.add_axes` on the current
              figure.

        xlims: Size of figure along the X axis
        ylims: Size of figure along the Y axis
        *args: Positional arguments to pass to :meth:`.pyplot.axes`
        *kwargs: Keyword arguments to pass to :meth:`.pyplot.axes`
    """
    fig = plt.figure()
    ax = plt.axes(arg, projection='rectilinear', **kwargs)
    if (xlims is not None):
        ax.set_xlim(*xlims)
    if (ylims is not None):
        ax.set_ylim(*ylims)
    return (fig, ax)


def fig3(xlims: Optional[Tuple[float, float]] = None,  # type: ignore[no-any-unimported] # noqa: E501
         ylims: Optional[Tuple[float, float]] = None,
         zlims: Optional[Tuple[float, float]] = None,
         arg: None | tuple[float, float, float, float] = None,
         **kwargs: Any) \
        -> Tuple[Figure, Axes3D]:
    """Create then return a figure with a 3-dimensional axis.

    Invoke :meth:`.pyplot.figure` to create figure, then
    invoke :meth:`.pyplot.axes` to create an :class:`Axes3D`.
    Return both objects in a tuple.

    Args:
        arg: :python:`None` or 4-tuple.

            - :python:`None`: A new full window Axes is added using
              ``subplot(**kwargs)``.

            - 4-tuple of floats *rect* = ``(left, bottom, width, height)``:
              Add a new Axes with dimensions *rect* in normalized
              (0, 1) units, using :meth:`Figure.add_axes` on the current
              figure.

        xlims: Size of figure along the X axis
        ylims: Size of figure along the Y axis
        ylims: Size of figure along the Y axis
        *kwargs: Keyword arguments to pass to :meth:`.pyplot.axes`
    """
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


class DimensionError(ValueError):
    """Raised when the dimension of a figure does not agree
    with the plot.

    When this happens, something is going seriously wrong.
    """
    def __init__(self, expected: str, actual: str):
        """
        Args:
            expected: Dimensions of the plot
            actual: Dimensions of the figure
        """
        super().__init__(f"Dimension mismatch: expected {expected},"
                         f" got {actual}")


def ensure_axes_dimension(axes: Axes | Axes3D,  # type: ignore[no-any-unimported] # noqa: E501
                          dim: int) -> None:
    """Assert if the given axes is of the specified dimension.

    Raises:
        :class:`DimensionError`: if :arg:`dim` does not agree with the
            dimension of :arg:`axes:.`
    """
    dimension_to_name = {2: "rectilinear", 3: "3d"}
    if dim in dimension_to_name:
        if (axes.name != dimension_to_name[dim]):
            raise DimensionError(dimension_to_name[dim], axes.name)
    else:
        fig3() if dim == 3 else fig2()
        logging.warning(f"The current projection is not `{dim}d`."
                        f"A new {"Axes" if dim == 2 else "Axes3D"}"
                        " is created instead.")
