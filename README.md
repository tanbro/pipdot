# pipdot

[![GitHub](https://img.shields.io/github/license/tanbro/pipdot)](https://github.com/tanbro/pipdot)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/tanbro/pipdot)](https://github.com/tanbro/pipdot/tags)
[![PyPI](https://img.shields.io/pypi/v/pipdot)](https://pypi.org/project/pipdot/)
[![PyPI - Status](https://img.shields.io/pypi/status/pipdot)](https://pypi.org/project/pipdot/)
[![PyPI - License](https://img.shields.io/pypi/l/pipdot)](https://pypi.org/project/pipdot/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipdot)](https://pypi.org/project/pipdot/)

Generate a [GraphViz][] `dot` file representing installed [PyPI][] distributions.

## Installation

```bash
pip install pipdot
```

It's a zero-dependency package.

## Usage

To generate a [GraphViz][] `dot` file for distributions of current Python environment, we shall run:

```bash
pipdot --extras-label 1.dot
```

Then convert it to a `svg` (or other formats) image:

```bash
dot -T svg -O 1.dot
```

We'll get something like:

![assets/1.dot.svg](assets/1.dot.svg)

For help messages, execute:

```bash
python -m pipdot --help
```

And we can use it by docker:

```bash
docker run -it --rm liuxueyan/pipdot -p "your-python-site-dir"
```

[PyPI]: https://pypi.org/
[pip]: https://pip.pypa.io/
[GraphViz]: https://graphviz.org/
