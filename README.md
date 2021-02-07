# pipdot

Generate a [GraphViz][] `dot` file representing installed [PyPI][] distributions.

## Installation

```sh
pip install pipdot
```

## Usage

A [pip][] `>=10.0` is needed.

Generate a [GraphViz][] `dot` file:

```sh
pipdot --include-extras --show-extras-label 1.dot
```

Convert it to a `svg` (or other formats) image:

```sh
dot -T svg -O 1.dot
```

we'll get something like:

![assets/1.dot.svg](https://github.com/tanbro/pipdot/raw/main/assets/1.dot.svg)

Run

```sh
python -m pipdot --help
```

for help messages

[PyPI]: https://pypi.org/
[pip]: https://pip.pypa.io/
[graphviz]: https://graphviz.org/
