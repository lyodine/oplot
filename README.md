<p align="center">
<img src="https://github.com/lyodine/ograph/blob/main/media/logo.png" width=100>
</p>


# OGraph

A lightweight Matplotlib wrapper.

## Installation

Install from PyPI:

```shell
pip install ograph
```

Install from source:

```
pip install .
```

Please see [documentation](https://yidingli.com/projects/ograph/docs/install-and-build.html) for detailed instructions.

## Components

The library have the following modules:

| Component                                          | Description                |
| -------------------------------------------------- | -------------------------- |
| [ofig](./ograph/ofig/) | Create and check the dimensions of plots |
| [oplot](./ograph/oplot/) | Plot to the current axes  |
| [oconfig](./ograph/oconfig/)                       | Configure plots            |
| [ofunc](./ograph/ofunc/) | Supply test functions and matrices |
| [swarm](./ograph/swarm/) | Plot point clusters |

The ograph.oplot library contains the following plotters: 

| Plotter   | Dimension of Plot | Data               |
| --------- | ----------------- | ------------------ |
| heatmap   | 2                 | $M\times N$ matrix |
| chull     | 2, 3              | $R^2$ or $R^3$     |
| arrow     | 2, 3              | $R^2$ or $R^3$     |
| plot      | 2                 | $R\rightarrow R$   |
| wireframe | 3                 | $R^2\rightarrow R$ |
| surface   | 3                 | $R^2\rightarrow R$ |
| stems     | 2                 | $R\rightarrow R$   |
| stem      | 2                 | `xs`  and `ys      |
| patch     | Any               | Colours and labels |

The `application.swarm` module contains the following plotters:


plot_positions 2 list[R^2] or list[list[R^2]]
plot_bests 2 list[R^2]