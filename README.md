# pipdot

Generate a [Graphviz][] `dot` file representing installed [PyPI][] distributions.

## Installation

```sh
pip install pipdot
```

## Usage

Generate a [graphviz][] `dot` file

```sh
pipdot --include-extras --show-extras-label 1.dot
```

Convert it to a `svg` (or other formats) image:

```sh
dot -Tsvg -O 1.dot
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
