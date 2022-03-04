"""
Generate a GraphViz dot file representing installed PyPI distributions
"""

import site
import sys
from argparse import ArgumentParser, FileType
from functools import lru_cache, partial
from os import path
from pathlib import Path

try:
    from argparse import BooleanOptionalAction  # type: ignore
except ImportError:
    from .backports.argparse import BooleanOptionalAction

from .utils import AddSysPath
from .version import version as __version__


def get_args():
    _, tail = path.split(sys.argv[0])
    root, _ = path.splitext(tail)
    prog = (
        '{} -m {}'.format(sys.executable, __package__)
        if root == __name__
        else __package__
    )
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
        '--user-only', action=BooleanOptionalAction, default=False,
        help='Only output packages installed in user-site.'
    )
    parser.add_argument(
        '--extras-label', action=BooleanOptionalAction, default=False,
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


@lru_cache(maxsize=None)
def in_site(dist):
    loc_path = Path(dist.locate_file(''))
    return any(loc_path == Path(x) for x in site.getsitepackages())


@lru_cache(maxsize=None)
def in_usersite(dist):
    loc_path = Path(dist.locate_file(''))
    return loc_path == Path(site.getusersitepackages())


def _installed(dists, name):
    return _find_distribution(dists, name) is not None


def _find_distribution(dists, name):
    from packaging.utils import canonicalize_name  # type: ignore

    for d in dists:
        if canonicalize_name(d.metadata['Name']) == canonicalize_name(name):
            return d


def _get_requires_extras(dists, dist_or_name):
    from packaging.requirements import Requirement  # type: ignore
    from packaging.utils import canonicalize_name  # type: ignore

    requires_extras = dict()
    if isinstance(dist_or_name, str):
        dist = _find_distribution(dists, dist_or_name)
    else:
        dist = dist_or_name
    if dist is None:
        return requires_extras

    extras = dist.metadata.get_all('Provides-Extra')

    if dist.requires:
        for require_exp in dist.requires:
            require = Requirement(require_exp)
            rc_name = canonicalize_name(require.name)
            matched_extras = (
                set(
                    m for m in extras
                    if require.marker
                    and require.marker.evaluate(environment={'extra': m})
                )
                if extras
                else set()
            )
            if matched_extras:
                if rc_name in requires_extras:
                    requires_extras.update({
                        rc_name: requires_extras[rc_name].union(matched_extras)
                    })
                else:
                    requires_extras[rc_name] = matched_extras
            else:
                if rc_name in requires_extras:
                    requires_extras[rc_name].add('')
                else:
                    requires_extras[rc_name] = set([''])

    return requires_extras


def perform(args):
    import importlib_metadata  # type: ignore
    import jinja2  # type: ignore
    from packaging.requirements import Requirement  # type: ignore
    from packaging.utils import canonicalize_name  # type: ignore

    kdargs = dict()
    if args.path:
        kdargs.update(path=args.path)
    dists = list(importlib_metadata.distributions(**kdargs))

    requires_extras = lru_cache(maxsize=None)(
        partial(_get_requires_extras, dists))
    installed = lru_cache(maxsize=None)(partial(_installed, dists))

    context = {
        'distributions': dists,
        'options': args,
        'in_site': in_site,
        'in_usersite': in_usersite,
        'canonicalize_name': canonicalize_name,
        'requires_extras': requires_extras,
        'installed': installed,
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
    print('', file=args.output)


def main():
    args = get_args()
    vendor_dir = Path(__file__).parent.joinpath('_vendor')
    with AddSysPath(vendor_dir):
        return perform(args)


if __name__ == '__main__':
    exit(main())
