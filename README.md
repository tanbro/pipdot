# pipdot

[![GitHub](https://img.shields.io/github/license/tanbro/pipdot)](https://github.com/tanbro/pipdot)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/tanbro/pipdot)](https://github.com/tanbro/pipdot/tags)
[![PyPI](https://img.shields.io/pypi/v/pipdot)](https://pypi.org/project/pipdot/)
[![PyPI - Status](https://img.shields.io/pypi/status/pipdot)](https://pypi.org/project/pipdot/)
[![PyPI - License](https://img.shields.io/pypi/l/pipdot)](https://pypi.org/project/pipdot/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipdot)](https://pypi.org/project/pipdot/)

Generate a [GraphViz][] `dot` file representing installed [PyPI][] distributions.

## Installation

```sh
pip install pipdot
```

## Usage

A [pip][] `>=22.0` is needed.

Generate a [GraphViz][] `dot` file:

```sh
pipdot --show-extras-label 1.dot
```

Convert it to a `svg` (or other formats) image:

```sh
dot -T svg -O 1.dot
```

we'll get something like:

![assets/1.dot.svg](assets/1.dot.svg)

Run

```sh
python -m pipdot --help
```

for help messages

[PyPI]: https://pypi.org/
[pip]: https://pip.pypa.io/
[GraphViz]: https://graphviz.org/
