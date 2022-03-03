"""
Generate a GraphViz dot file representing installed PyPI distributions
"""

import site
import sys
from pathlib import Path
from argparse import ArgumentParser, FileType
from os import path
from pathlib import Path
from typing import Iterable, Mapping, Optional, Union
import importlib.metadata as importlib_metadata

try:
    from argparse import BooleanOptionalAction  # type: ignore
except ImportError:
    from .boolean_optional_action import BooleanOptionalAction

from .utils import AddSysPath
from .version import version as __version__


def _get_args():
    _, tail = path.split(sys.argv[0])
    root, _ = path.splitext(tail)
    prog = '{} -m {}'.format(sys.executable, __package__) \
        if root == __name__ \
        else __package__
    parser = ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s {0} from {1} ({2} {3})'.format(
            __version__, sys.argv[0], sys.implementation.name, sys.version
        )
    )
    parser.add_argument(
        '--path', '-p', action='append',
        help='If path is set, only report the distributions present at the specified location. '
             'This option can be specified multiple times for more than one locations.'
    )
    parser.add_argument(
        '--local-only', action=BooleanOptionalAction, default=True,
        help='If in a virtual-env that has global access, '
             'do not list globally-installed packages.'
    )
    parser.add_argument(
        '--include-editables', action=BooleanOptionalAction, default=True,
        help='List editable projects.'
    )
    # parser.add_argument(
    #     '--editables-only', action=BooleanOptionalAction, default=False,
    #     help='List editable projects only.'
    # )
    parser.add_argument(
        '--user-only', action=BooleanOptionalAction, default=False,
        help='Only output packages installed in user-site.'
    )
    parser.add_argument(
        '--show-extras-label', action=BooleanOptionalAction, default=False,
        help='Show extras dependencies label.'
    )
    parser.add_argument(
        '--installed-only', action=BooleanOptionalAction, default=True,
        help='Only output installed packages. Extras packages those are not installed will not be shown.'
    )
    parser.add_argument(
        '--template', '-t',
        help='The Jinja2 template file be used to render GraphViz. '
             'If not specified, a default template will be used.'
    )
    parser.add_argument(
        'output', type=FileType('w', encoding='utf-8'),
        nargs='?', default=sys.stdout,
        help='Write generated graphviz dot to the file. It will output to "stdout" if not specified.',
    )
    return parser.parse_args()


def in_site(distribution: importlib_metadata.Distribution) -> bool:
    location = Path(distribution.locate_file(''))
    for dir in site.getsitepackages():
        pth = Path(dir)
        if pth == location:
            return True
    return False


def in_usersite(distribution: importlib_metadata.Distribution) -> bool:
    location = Path(distribution.locate_file(''))
    pth = Path(site.getusersitepackages())
    if pth == location:
        return True
    return False


def _find_distribution(
    dists: Iterable[importlib_metadata.Distribution],
    name: str
) -> Optional[importlib_metadata.Distribution]:
    import jinja2
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name

    for d in dists:
        if canonicalize_name(d.metadata['Name']) == canonicalize_name(name):
            return d


def _get_requires_extras(
    dists: Iterable[importlib_metadata.Distribution],
    dist_or_name: Union[importlib_metadata.Distribution, str],
) -> Mapping[str, str]:

    import jinja2
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name

    requires_extras = dict()
    if isinstance(dist_or_name, str):
        dist = _find_distribution(dists, dist_or_name)
    else:
        dist = dist_or_name
    if dist is None:
        return requires_extras

    extras = dist.metadata.get_all('Provides-Extra')

    if dist.requires:
        for s in dist.requires:
            require = Requirement(s)
            rc_name = canonicalize_name(require.name)
            extra_matched = False
            if extras:
                for extra in extras:
                    if require.marker:
                        if require.marker.evaluate(environment={'extra': extra}):
                            extra_matched = True
                            if rc_name in requires_extras:
                                requires_extras[rc_name].append(extra)
                            else:
                                requires_extras[rc_name] = [extra]
            if not extra_matched:
                if rc_name in requires_extras:
                    requires_extras[rc_name].append('')
                else:
                    requires_extras[rc_name] = ['']

    for k in requires_extras:
        requires_extras[k] = list(set(requires_extras[k]))

    return requires_extras


def _perform(args):

    import jinja2
    from packaging.requirements import Requirement
    from packaging.utils import canonicalize_name

    kdargs = dict()
    if args.path:
        kdargs.update(path=args.path)
    dists = list(importlib_metadata.distributions(**kdargs))

    context = {
        'distributions': dists,
        'show_extras_label': args.show_extras_label,
        'installed_only': args.installed_only,
        'in_site': in_site,
        'in_usersite': in_usersite,
        'canonicalize_name': canonicalize_name,
        'requires_extras': lambda x: _get_requires_extras(dists, x),
        'installed': lambda x: _find_distribution(dists, str(x)) is not None,
        'Requirement': Requirement,
    }

    if args.template:
        template = jinja2.Environment(
            loader=jinja2.FileSystemLoader(''),
            extensions=['jinja2.ext.do']
        ).get_template(args.template)
    else:
        template = jinja2.Environment(
            loader=jinja2.PackageLoader(__package__),
            extensions=['jinja2.ext.do']
        ).get_template('default.dot.j2')

    for s in template.generate(context):
        args.output.write(s)


def main():
    args = _get_args()

    vendor_dir = Path(
        importlib_metadata.distribution(__package__)
        .locate_file('')
    ).joinpath(__package__, '_vendor')

    with AddSysPath(vendor_dir):
        return _perform(args)


if __name__ == '__main__':
    exit(main())
