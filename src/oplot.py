import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.colors as colors
import numpy as np

from . import ofig as of

import logging
from typing import TypeAlias, Any, Self
import math
from numpy.typing import ArrayLike

from typing import Optional, Sequence, Annotated, Callable

from scipy.spatial import ConvexHull, distance  # type: ignore[import-untyped]

from matplotlib.axes import Axes
from matplotlib.patches import FancyArrowPatch

from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # type: ignore[import-untyped]
from mpl_toolkits.mplot3d.axes3d import Axes3D  # type: ignore[import-untyped]
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d.proj3d import proj_transform  # type: ignore[import-untyped]

from numpy import ndarray

Array2D: TypeAlias = Annotated[ndarray, (2, 2)]


FILL_COLOR: dict[str, str | float] = {"alpha": 0.5}
EDGE_COLOR = {"color": "black", "alpha": 1}
VERTEX_COLOR = {"color": "black", "alpha": 0.5}
CONTOUR_CMAP = "viridis"


class DimensionError(ValueError):
    def __init__(self, expected: str, actual: str):
        super().__init__(f"Dimension mismatch: expected {expected}, got {actual}")


def ensure_axes_dimension(axes: Axes | Axes3D,  # type: ignore[no-any-unimported]
                          dim: int) -> None:
    """ Assert if the give Axes (or Axes3D) is of the specified dimension.
    If not, create an Axes (or Axes3D) with the correct dimension.
    @param axes The Axes or Axes3D whose dimension is to be checked.
    @exception DimensionMismatchException if the first item does not
    match the specified dimension.
    """
    dimension_to_name = {2: "rectilinear", 3: "3d"}
    if dim in dimension_to_name:
        if (axes.name != dimension_to_name[dim]):
            raise DimensionError(dimension_to_name[dim], axes.name)
    else:
        of.fig3() if dim == 3 else of.fig2()
        logging.warning(f"The current projection is not `{dim}d`."
                        f"A new {"Axes" if dim == 2 else "Axes3D"} is created instead.")

        #raise ValueError(f"The specified dimension cannot be checked.")


def ensure_matrix_dimension(mat: Sequence[Sequence[float]] | np.ndarray,
                            dim: int) -> None:
    """ Examine if the first item in a sequence matches the given dimension.
    If not, raise an exception.
    @param mat A <del>matrix</del> sequence of sequences of numbers.
    @exception DimensionMismatchException if the first item does not match the specified
        dimension.
    """
    dimension_to_name = {2: 2, 3: 3}
    mat_dim = len(mat[0])
    if dim in dimension_to_name:
        if (mat_dim != dimension_to_name[dim]):
            raise DimensionError(str(dimension_to_name[dim]), str(mat_dim))
    else:
        raise ValueError("The specified dimension cannot be checked.")


#  @var A 2-dimensional unit square. Immutable.
unit_square = np.array(
    [[0, 0],
     [0, 1],
     [1, 0],
     [1, 1]]
)
unit_square.flags.writeable = False


# @var A 3-dimensional unit cube. Immutable.
unit_cube = np.array(
    [[0, 0, 0],
     [1, 0, 0],
     [0, 1, 0],
     [0, 0, 1],
     [1, 1, 0],
     [0, 1, 1],
     [1, 0, 1],
     [1, 1, 1],]
)
unit_cube.flags.writeable = False


def view_rotate(h_rotate: float, v_rotate: float) -> None:
    """ Rotate the current Axes3D.
    @param h_rotate the degree to rotate vertically
    @param v_rotate the degree to rotate horizontally
    """
    ax: Axes = plt.gca()
    ensure_axes_dimension(ax, 3)
    if (isinstance(ax, Axes3D)):  # Make mypy happy
        ax.view_init(h_rotate, v_rotate)
    else:
        raise Exception("This should not happen. The exception has been checked.")


def view_axis_pos(pos: Optional[str]) -> None:
    """ Position labels and ticks of the current Axes3D.
    @param pos the position, one of 'lower', 'upper', 'default', 'both', 'none', and None
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


def high_res() -> None:
    """Update the current rcParams to generate figures with 200 DPI.
    @effect Update rcParams.
    """
    pylab.rcParams.update({'figure.dpi': 200})


def annotate(title: str,
             xlabel: str,
             ylabel: str,
             zlabel: Optional[str] = None) -> None:
    """Add annotations (title, xlabel, ylabel) to the current figure.
    Also set runtime configurations.
    @param title Title of the figure
    @param xlabel Labels for the x axis
    @param ylabel Labels for the y axis
    @param zlabel Labels for the z axis
    @effect Plot to the current active figure; update rcParams.
    """
    # import matplotlib.pylab as pylab
    # To reset the parameters, use: matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    axes_label_size: str = "x-large"
    plot_title_size: str = "x-large"

    font = {'legend.fontsize': 'x-large',
            'axes.titlesize': plot_title_size,
            'axes.labelsize': axes_label_size,
            'xtick.labelsize': axes_label_size,
            'ytick.labelsize': axes_label_size,
            'text.usetex': False,
            'font.family': 'Open Sans',
            'axes.titlepad': 15, }

    ax: Axes | Axes3D = plt.gca()  # type: ignore[no-any-unimported]

    pylab.rcParams.update(font)
    ax.set_xlabel(xlabel, fontname='PT Serif')
    ax.set_ylabel(ylabel, fontname='PT Serif')
    if (zlabel is not None):
        ensure_axes_dimension(ax, 3)
        if (isinstance(ax, Axes3D)):
            ax.set_zlabel(zlabel, fontname='PT Serif')
        else:
            raise Exception("This should not happen.")

    my_fig = ax.get_figure()

    if (my_fig is not None):
        my_fig.suptitle(title, fontname='PT Serif')
    else:
        raise Exception("Somehow the Axes is not attached to a Figure. How?")


def heatmap(data: ndarray,
            xlabels: Optional[Sequence[str]] = None,
            ylabels: Optional[Sequence[str]] = None) -> None:
    """Plot a heatmap from a square matrix.
    @param data A matrix.
    @param xlabels Labels for cells along the x axis.
    @param ylabels Labels for cells along the y axis.
    @effect Plot to the current active Axes.
    """
    if not isinstance(data, ndarray):
        # If the input is not an numpy array, attempt to cast it into one.
        data = np.array(data)

    # Configure the size of the plot to accommodate the size of each cell
    plt.rcParams["figure.figsize"] = [len(data) * math.sqrt(len(data)),
                                      len(data[0]) * math.sqrt(len(data[0]))]
    # if len(data) != len(data[0]):
    #     raise Exception("Dimension check error, dimension mismatch")

    xlabels = xlabels if (xlabels is not None)\
        else ["X" + str(i) for i, _ in enumerate(data[0])]
    ylabels = ylabels if (ylabels is not None)\
        else ["Y" + str(i) for i, _ in enumerate(data)]

    # fig, ax = plt.subplots()

    ax = plt.gca()

    ensure_axes_dimension(ax, 2)
    ax.imshow(data, cmap="Greys")

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(xlabels)), labels=xlabels)
    ax.set_yticks(np.arange(len(ylabels)), labels=ylabels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(),
             rotation=45,
             ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    print(len(ylabels))
    print(len(xlabels))

    max_cell_value = data.max()
    min_cell_value = data.min()

    for i in range(len(ylabels)):
        for j in range(len(xlabels)):
            cell_value_scale = max_cell_value - min_cell_value
            ratio = (data[i, j] - min_cell_value) / cell_value_scale
            ax.text(j, i, "{:.2f}".format(data[i, j]),
                    ha="center",
                    va="center",
                    color="w" if ratio > .6 else "k")

    my_fig = ax.get_figure()
    if (my_fig is not None):
        my_fig.tight_layout()


def chull(shape: Annotated[ndarray, (..., 2)] | Annotated[ndarray, (..., 3)]) -> None:
    """Plot a convex hull to the current active Axes.
    @param shape A sequence of 2- or 3-dimensional points.
    @effect Plot to the current active Axes.
    """
    # Note that the checker only checks if the first element has the correct dimension.
    match len(shape[0]):
        case 2:
            _chull_2d(shape)
        case 3:
            _chull_3d(shape)
        case _:
            raise ValueError("Input must be either 2 or 3")


def _chull_3d(shape: ndarray) -> None:
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    ensure_axes_dimension(ax, 3)
    # color = 'r'

    hull = ConvexHull(shape)
    for s in hull.simplices:
        tri = Poly3DCollection([shape[s]])

        if "alpha" in FILL_COLOR:
            tri.set_alpha(FILL_COLOR["alpha"])
        if "color" in FILL_COLOR:
            tri.set_color(FILL_COLOR["color"])

        tri.set_edgecolor('none')
        ax.add_collection3d(tri)
        edges = []
        if distance.euclidean(shape[s[0]], shape[s[1]])\
                < distance.euclidean(shape[s[1]], shape[s[2]]):
            edges.append((s[0], s[1]))
            if distance.euclidean(shape[s[1]], shape[s[2]])\
                    < distance.euclidean(shape[s[2]], shape[s[0]]):
                edges.append((s[1], s[2]))
            else:
                edges.append((s[2], s[0]))
        else:
            edges.append((s[1], s[2]))
            if distance.euclidean(shape[s[0]], shape[s[1]]) <\
                    distance.euclidean(shape[s[2]], shape[s[0]]):
                edges.append((s[0], s[1]))
            else:
                edges.append((s[2], s[0]))
        for v0, v1 in edges:
            ax.plot(xs=shape[[v0, v1], 0],
                    ys=shape[[v0, v1], 1],
                    zs=shape[[v0, v1], 2],
                    **EDGE_COLOR)

    ax.scatter(shape[:, 0], shape[:, 1], shape[:, 2], marker='o', **VERTEX_COLOR)


def _chull_2d(points: ndarray) -> None:
    ax = plt.gca()
    ensure_axes_dimension(ax, 2)
    hull = ConvexHull(points)
    ax.plot(points[:, 0], points[:, 1], 'o', **VERTEX_COLOR)  # type: ignore[arg-type]
    for simplex in hull.simplices:
        ax.plot(points[simplex, 0],
                points[simplex, 1],
                **EDGE_COLOR)  # type: ignore[arg-type]
    ax.fill(points[hull.vertices, 0], points[hull.vertices, 1], lw=2, **FILL_COLOR)


Vec2D = Annotated[Sequence[float], 2]
Vec3D = Annotated[Sequence[float], 3]


class BigArrow(FancyArrowPatch):
    """An 2- or 3-dimensional arrow.
    """
    def __init__(self,
                 start: Vec2D | Vec3D,
                 end: Vec2D | Vec3D,
                 *args: Any,
                 **kwargs: Any):
        default_styles = {
            "mutation_scale": 30,
            "arrowstyle": "-|>",
            "linestyle": "--"
        }
        super().__init__((start[0], start[1]),
                         (end[0], end[1]),
                         *args,
                         **(kwargs | default_styles))
        # Note that two copies of `start` and `end` are preserved:
        #   One copy is passed to ->_posA_posB of the parent class; this copy
        #       is used in `draw`.
        #   the other copy is passed to ->start and ->end of this class; this
        #       copt is used in do_3d_projections.
        self.start = start
        self.end = end

    def draw(self: Self, renderer: Any) -> None:
        super().draw(renderer)

    def do_3d_projection(self: Self, renderer: Any = None) -> Any:
        # The reference
        #   https://github.com/matplotlib/matplotlib/blob/v3.8.2/lib/
        #       mpl_toolkits/mplot3d/art3d.py#L998-L1065
        #   appears to return np.min(tzs).
        # Removing it does not seem to change anything. Still, just to be safe...
        if self.axes is None or not isinstance(self.axes, Axes3D):
            raise Exception("Rendered without axes")
        else:
            txs, tys, tzs = proj_transform(*zip(self.start, self.end), self.axes.M)
            self.set_positions((txs[0], tys[0]), (txs[1], tys[1]))
            return np.min(tzs)


def arrow(start: Vec2D | Vec3D,
          end: Vec2D | Vec3D,
          *args: Any,
          **kwargs: Any) -> None:
    '''Plot an arrow to the current Axes or Axes3D.
    @param start The starting point of the arrow
    @param end The ending point of the arrow

    '''
    ax = plt.gca()
    # Type checking `ax` is necessary, since the arrow class can handle the difference.
    #   Plotting to 2D (projection='rectilinear') Axes calls `draw`.
    #   Plotting to 3D (projection='3d') calls do_3d_projection.
    #   Still, this function might not work for other projections.
    arrow = BigArrow(start, end, *args, **kwargs)
    ax.add_artist(arrow)


def plot(fun: Callable[[Array2D], Array2D],
         x_range: Vec2D,
         density: int = 1000,
         *args: ArrayLike,
         **kwargs: Any) -> None:
    '''Plot a contour map to the current Axes or Axes3D.
    @param fun The function to plot
    @param x_range A tuple of the beginning and end of the x axis
    @param density the number of points sampled over each axis
    '''
    ax = plt.gca()
    x_max: float = max(x_range)
    x_min: float = min(x_range)
    xs = np.arange(x_min, x_max, (x_max - x_min) / density)
    ys = fun(xs)
    ax.plot(xs, ys, *args, **kwargs)


def _make_zs(fun: Callable[[Array2D, Array2D], Array2D],
             x_range: Vec2D,
             y_range: Vec2D,
             density: int = 100,) -> tuple[ndarray, ndarray, ndarray]:

    x_max: float = max(x_range)
    x_min: float = min(x_range)
    y_max: float = max(y_range)
    y_min: float = min(y_range)

    xs = np.arange(x_min, x_max, step=(x_max - x_min) / density)
    ys = np.arange(y_min, y_max, step=(y_max - y_min) / density)

    xs, ys = np.meshgrid(xs, ys)
    zs = fun(xs, ys)

    return (xs, ys, zs)


def contour(fun: Callable[[Array2D, Array2D], Array2D],
            x_range: Vec2D,
            y_range: Vec2D,
            density: int = 100,
            levels: int = 50,
            cmap: str = CONTOUR_CMAP,
            colorbar: bool = True,
            alpha: float = 0.5) -> None:
    '''Plot a contour map to the current Axes or Axes3D.
    @param fun The function to plot
    @param x_range A tuple of the beginning and end of the x axis
    @param y_range A tuple of the beginning and end of the y axis
    @param Density the number of points sampled over each axis
    @param levels The number of contour lines
    @param cmap The colour map used by the contour map
    @param colorbar If True, draw the colour bar
    '''
    ax = plt.gca()
    xs, ys, zs = _make_zs(fun, x_range, y_range, density)
    ax.set_aspect('equal')  # Very important, otherwise axes use different scales.
    cs = ax.contour(xs, ys, zs, levels=levels, cmap=cmap,
                    norm=colors.Normalize(vmin=zs.min(), vmax=zs.max()), alpha=alpha)

    current_figure = ax.get_figure()
    if colorbar and current_figure is not None:
        current_figure.colorbar(cs)


def wireframe(fun:  # type: ignore[no-any-unimported]
              Callable[[Array2D, Array2D], Array2D],
              x_range: Vec2D,
              y_range: Vec2D,
              density: int = 100,
              cmap: str = CONTOUR_CMAP,
              alpha: float = 0.9) -> Line3DCollection:
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    xs, ys, zs = _make_zs(fun, x_range, y_range, density)
    ax.set_aspect('equal')  # Very important, otherwise axes use different scales.
    return ax.plot_wireframe(xs, ys, zs,
                             cmap=cmap,
                             norm=colors.Normalize(vmin=zs.min(), vmax=zs.max()),
                             alpha=alpha)


def surface(fun: Callable[[Array2D, Array2D], Array2D],  # type: ignore[no-any-unimported]
            x_range: Vec2D,
            y_range: Vec2D,
            density: int = 100,
            cmap: str = CONTOUR_CMAP,
            colorbar: bool = True,
            alpha: float = 0.9) -> Line3DCollection:
    ax: Axes3D = plt.gca()  # type: ignore[no-any-unimported]
    xs, ys, zs = _make_zs(fun, x_range, y_range, density)
    ax.set_aspect('equal')  # Very important, otherwise axes use different scales.
    cs = ax.plot_surface(xs, ys, zs,
                         cmap=cmap,
                         norm=colors.Normalize(vmin=zs.min(), vmax=zs.max()),
                         alpha=alpha,
                         rstride=1,
                         cstride=1,
                         edgecolor='none')

    if colorbar:
        ax.get_figure().colorbar(cs)
    return cs
