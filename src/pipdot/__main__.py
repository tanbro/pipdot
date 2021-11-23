"""
Generate a GraphViz dot file representing installed PyPI distributions
"""

import sys
from argparse import ArgumentParser, FileType
from os import path

import jinja2
from pip._internal.utils.misc import (dist_in_site_packages, dist_in_usersite,
                                      dist_is_editable, dist_is_local,
                                      get_installed_distributions)

from .version import version as __version__

try:
    from argparse import BooleanOptionalAction  # type: ignore
except ImportError:
    from .boolean_optional_action import BooleanOptionalAction


__PACKAGE_NAME__ = 'pipdot'
__PROG__ = 'pipdot'


def _get_args():
    prog = __PROG__
    _, tail = path.split(sys.argv[0])
    root, _ = path.splitext(tail)
    if root == __name__:
        prog = '{} -m {}'.format(sys.executable, __PACKAGE_NAME__)
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
    parser.add_argument(
        '--editables-only', action=BooleanOptionalAction, default=False,
        help='List editable projects only.'
    )
    parser.add_argument(
        '--user-only', action=BooleanOptionalAction, default=False,
        help='Only output packages installed in user-site.'
    )
    parser.add_argument(
        '--include-extras', action=BooleanOptionalAction, default=False,
        help='List extras dependent packages.'
    )
    parser.add_argument(
        '--show-extras-label', action=BooleanOptionalAction, default=False,
        help='Show extras dependencies label.'
    )
    parser.add_argument(
        '--template', '-t',
        help='The Jinja2 template file be used to render GraphViz. '
             'If not specified, a default template will be used.'
    )
    parser.add_argument(
        'outfile', type=FileType('w', encoding='utf-8'),
        help='Write generated graphviz dot file here.',
    )
    return parser.parse_args()


def _perform(args):
    dist_list = get_installed_distributions(
        local_only=args.local_only,
        include_editables=args.include_editables,
        editables_only=args.editables_only,
        user_only=args.user_only,
        paths=args.path
    )

    context = {
        'installed_distributions': dist_list,
        'editable_distributions': [],
        'local_distributions': [],
        'site_distributions': [],
        'user_distributions': [],
        'include_extras': args.include_extras,
        'show_extras_label': args.show_extras_label,
    }

    for dist in dist_list:
        if dist_is_editable(dist):
            context['editable_distributions'].append(dist)
        if dist_is_local(dist):
            context['local_distributions'].append(dist)
        if dist_in_site_packages(dist):
            context['site_distributions'].append(dist)
        if dist_in_usersite(dist):
            context['user_distributions'].append(dist)

    if args.template:
        template = jinja2.Environment(
            loader=jinja2.FileSystemLoader(''),
            extensions=['jinja2.ext.do']
        ).get_template(args.template)
    else:
        template = jinja2.Environment(
            loader=jinja2.PackageLoader(__PACKAGE_NAME__),
            extensions=['jinja2.ext.do']
        ).get_template('default.dot.j2')

    for s in template.generate(context):
        args.outfile.write(s)


def main():
    args = _get_args()
    return _perform(args)


if __name__ == '__main__':
    exit(main())
