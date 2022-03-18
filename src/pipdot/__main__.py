"""
Generate a GraphViz dot file representing installed PyPI distributions
"""

import json
import site
import sys
from argparse import ArgumentParser, FileType
from functools import lru_cache, partial
from itertools import chain
from os import path
from pathlib import Path
from subprocess import check_output

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
        '--python', '-P', type=str,
        help='Report the distributions for this python executable. '
             '"--path/-p" option will not affect if this option was set. '
             'The program check specified python\'s "sys.path" by an actual execution, so you can not use it in a container.'
    )
    parser.add_argument(
        '--path', '-p', action='append',
        help='Report the distributions present at the specified location. '
             'This option will not affect if "--python/-P" was set. '
             'This option can be specified multiple times for more than one locations.'
    )
    parser.add_argument(
        '--site', action=BooleanOptionalAction, default=True,
        help='Include distributions in global site-packages directories.'
    )
    parser.add_argument(
        '--user', action=BooleanOptionalAction, default=True,
        help='Include distributions in user-specific site-packages directory.'
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
    pth = Path(dist.locate_file(''))
    return any(pth == Path(x) for x in site.getsitepackages())


@lru_cache(maxsize=None)
def in_usersite(dist):
    pth = Path(dist.locate_file(''))
    return pth == Path(site.getusersitepackages())


def _installed(dists, name):
    return _find_distribution(dists, name) is not None


def _find_distribution(dists, name):
    from packaging.utils import canonicalize_name  # type: ignore

    c_name = canonicalize_name(name)
    for d in dists:
        if canonicalize_name(d.metadata['Name']) == c_name:
            return d


def _get_requires_extras(dists, dist_or_name):
    from packaging.requirements import Requirement  # type: ignore
    from packaging.utils import canonicalize_name  # type: ignore

    result = dict()

    if isinstance(dist_or_name, str):
        dist = _find_distribution(dists, dist_or_name)
    else:
        dist = dist_or_name
    if dist is None:
        return result
    if not dist.requires:
        return result

    extras = dist.metadata.get_all('Provides-Extra')

    for line in dist.requires:
        require = Requirement(line)
        rc_name = canonicalize_name(require.name)
        matched_extras = (
            set(
                # requires like:
                # `SecretStorage (>=3.2) ; sys_platform == "linux"`
                # will match every extra, so we add a `''` to detect it.
                s for s in chain(extras, ('',))
                if require.marker
                and require.marker.evaluate(environment=dict(extra=s))
            )
            if extras
            else set()
        )
        if matched_extras:
            if rc_name in result:
                result[rc_name] = result[rc_name].union(matched_extras)
            else:
                result[rc_name] = matched_extras
        else:
            if rc_name in result:
                result[rc_name].add('')
            else:
                result[rc_name] = set(('',))

    return result


def perform(args):
    import importlib_metadata  # type: ignore
    import jinja2  # type: ignore
    from packaging.requirements import Requirement  # type: ignore
    from packaging.utils import canonicalize_name  # type: ignore

    if args.python:
        output = check_output([
            args.python, '-c', 'import json, sys; json.dump(sys.path, sys.stdout)'
        ])
        sys_paths = json.loads(output)
        args.path = [p for p in sys_paths if path.isdir(p)]

    kdargs = dict()
    if args.path:
        kdargs.update(path=args.path)
    dists = list(importlib_metadata.distributions(**kdargs))

    requires_extras = lru_cache(maxsize=None)(
        partial(_get_requires_extras, dists)
    )
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
