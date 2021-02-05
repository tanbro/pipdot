# pipdot

Generate a [Graphviz][] `dot` file representing installed [PyPI][] distributions.

## Installation

```sh
pip install pipdot
```

## Usage

Execute

```sh
pipdot out.dot
```

we'll get something like:

```dot
digraph {
    rankdir = "LR";
    "setuptools" [
        label="setuptools\n44.0.0",
        color="#e27dd6ff", fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pkg-resources" [
        label="pkg-resources\n0.0.0",
        color="#e27dd6ff", fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pip" [
        label="pip\n20.0.2",
        color="#e27dd6ff", fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "markupsafe" [
        label="MarkupSafe\n1.1.1",
        color="#e27dd6ff", fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "jinja2" [
        label="Jinja2\n2.11.3",
        color="#e27dd6ff", fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pipdot" [
        label="pipdot\n0.1.dev5+g0b50457.d20210205",
        color="#e27dd6ff", fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "setuptools" [
        label="setuptools\n44.0.0",
        color="#e27dd6ff",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pkg-resources" [
        label="pkg-resources\n0.0.0",
        color="#e27dd6ff",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pip" [
        label="pip\n20.0.2",
        color="#e27dd6ff",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "markupsafe" [
        label="MarkupSafe\n1.1.1",
        color="#e27dd6ff",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "jinja2" [
        label="Jinja2\n2.11.3",
        color="#e27dd6ff",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pipdot" [
        label="pipdot\n0.1.dev5+g0b50457.d20210205",
        color="#e27dd6ff",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "setuptools" [
        label="setuptools\n44.0.0",
        color="#8383cc",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pkg-resources" [
        label="pkg-resources\n0.0.0",
        color="#8383cc",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pip" [
        label="pip\n20.0.2",
        color="#8383cc",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "markupsafe" [
        label="MarkupSafe\n1.1.1",
        color="#8383cc",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "jinja2" [
        label="Jinja2\n2.11.3",
        color="#8383cc",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pipdot" [
        label="pipdot\n0.1.dev5+g0b50457.d20210205",
        color="#8383cc",
        fillcolor="#d9e7ee",
        style="filled,setlinewidth(6)"
    ];
    "pipdot" [
        label="pipdot\n0.1.dev5+g0b50457.d20210205",
        color="#51bf5b",
        fillcolor="#91b5c9",
        style="filled,setlinewidth(6)"
    ];
    "jinja2" -> "markupsafe"[
        color="#61c2c5"
    ];
    "pipdot" -> "pip"[
        color="#61c2c5"
    ];
    "pipdot" -> "jinja2"[
        color="#61c2c5"
    ];
}
```

Run

```sh
python -m pipdot --help
```

for help messages

[PyPI]: https://pypi.org/
[pip]: https://pip.pypa.io/
[graphviz]: https://graphviz.org/
