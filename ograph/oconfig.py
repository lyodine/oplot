"""Utilities that configure the current plot
or all plots in the current session.
"""

from typing import Optional

import matplotlib.pyplot as plt
import matplotlib as mlp
import matplotlib.pylab as pylab
from mpl_toolkits.mplot3d.axes3d import Axes3D  # type: ignore[import-untyped]

from .ofig import ensure_axes_dimension


def clear_axis_labels(enable: bool = False) -> None:
    plt.gca().get_yaxis().set_ticks([])
    plt.gca().get_xaxis().set_ticks([])


def use_axis_lines(enable: bool = True) -> None:
    plt.gca().axhline(y=0, color='DimGrey', linestyle="--")
    plt.gca().axvline(x=0, color='DimGrey', linestyle="--")


def set_font_size(size: int) -> None:
    """Set the font size to :arg:`size`.

    Effect:
        Configure the current plot.
    """
    mlp.rc("font", size=size)


def use_high_res() -> None:
    """Set figures to render in higher resolution.

    Set runtime configuration ``figure.dpi`` to 200.

    Effect:
        Configure all plots in the current session.
    """
    pylab.rcParams.update({'figure.dpi': 200})


def use_low_res() -> None:
    """Set figures to render in the default resolution.

    Set runtime configuration ``figure.dpi`` to 100, the default value.

    Effect:
        Configure all plots in the current session.
    """
    pylab.rcParams.update({'figure.dpi': 100})


def view_rotate(h_rotate: float, v_rotate: float) -> None:
    """Rotate the current `Axes3D`.

    @param h_rotate the degree to rotate vertically
    @param v_rotate the degree to rotate horizontally
    """
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    ensure_axes_dimension(ax, 3)
    if (isinstance(ax, Axes3D)):  # Make mypy happy
        ax.view_init(h_rotate, v_rotate)
    else:
        raise Exception("This should not happen."
                        "The exception has been checked.")


def view_axis_pos(pos: Optional[str]) -> None:
    """Position labels and ticks of the current Axes3D.

    Args:
        pos: The position, one of :python:`'lower'`,
            :python:`'upper'`,
            :python:`'default'`,
            :python:`'both'`,
            :python:`'none'`,
            and :python:`None`.
    """
    accepted_values: list[str] = ['lower', 'upper', 'default', 'both', 'none']
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    ensure_axes_dimension(ax, 3)
    match pos:
        case None:
            ax.axis('off')
        case other:
            if other in accepted_values:
                for axis in ax.xaxis, ax.yaxis, ax.zaxis:
                    axis.set_label_position(other)
                    axis.set_ticks_position(other)
            else:
                raise ValueError(f"The input {other} is not one of"
                                 f"{str(accepted_values)}.")
