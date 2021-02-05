import argparse
import os
import sys
from itertools import chain

import jinja2
from pip._internal.utils.misc import (dist_in_site_packages, dist_in_usersite,
                                      dist_is_editable, dist_is_local,
                                      get_installed_distributions)

from .version import version as __version__

__PACKAGE_NAME__ = 'pipdot'
__PROG__ = 'pipdot'

BOOLEAN_MAPPING = {
    0: ('0', 'n', 'no', 'off', 'false'),
    1: ('1', 'y', 'yes', 'on', 'true'),
}
BOOLEAN_CHOICES = list(chain.from_iterable(BOOLEAN_MAPPING.values()))


def s2b(s):
    for k, v in BOOLEAN_MAPPING.items():
        if s in v:
            return bool(k)
    raise ValueError(s)


def _args():
    prog = __PROG__
    _, tail = os.path.split(sys.argv[0])
    root, _ = os.path.splitext(tail)
    if root == __name__:
        prog = '{} -m {}'.format(sys.executable, __PACKAGE_NAME__)
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument(
        '--local-only', '-l', choices=BOOLEAN_CHOICES, default='true',
        help='If in a virtualenv that has global access, do not list globally-installed packages. (default=%(default)s)'
    )
    parser.add_argument(
        '--include-editables', '-e', choices=BOOLEAN_CHOICES, default='true',
        help='List editable projects. (default=%(default)s)'
    )
    parser.add_argument(
        '--editables-only', choices=BOOLEAN_CHOICES, default='false',
        help='List editable projects only. (default=%(default)s)'
    )
    parser.add_argument(
        '--user-only', '-u', choices=BOOLEAN_CHOICES, default='false',
        help='Only output packages installed in user-site. (default=%(default)s)'
    )
    parser.add_argument(
        '--include-extras', action='store_true',
        help='List extras dependent packages. (default=%(default)s)'
    )
    parser.add_argument(
        '--show-extras-label', action='store_true',
        help='Show extras dependencies label. (default=%(default)s)'
    )
    parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s {0} from {1} ({2} {3[0]}.{3[1]})'.format(
            __version__, sys.argv[0], sys.implementation.name, sys.version_info
        )
    )
    parser.add_argument(
        'outfile', type=argparse.FileType('w'),
        help='Write generated graphviz dot file here.',
    )
    return parser.parse_args()


def _do(args):
    installed_distributions = get_installed_distributions(
        local_only=s2b(args.local_only),
        include_editables=s2b(args.include_editables),
        editables_only=s2b(args.editables_only),
        user_only=s2b(args.user_only),
    )
    editable_distributions = []
    local_distributions = []
    user_distributions = []
    site_distributions = []

    for dist in installed_distributions:
        if dist_is_editable(dist):
            editable_distributions.append(dist)
        if dist_is_local(dist):
            local_distributions.append(dist)
        if dist_in_site_packages(dist):
            site_distributions.append(dist)
        if dist_in_usersite(dist):
            user_distributions.append(dist)

    context = dict(
        installed_distributions=installed_distributions,
        editable_distributions=editable_distributions,
        local_distributions=local_distributions,
        site_distributions=site_distributions,
        user_distributions=user_distributions,
        include_extras=args.include_extras,
        show_extras_label=args.show_extras_label,
    )

    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader(__PACKAGE_NAME__),
        extensions=['jinja2.ext.do']
    )
    template = jinja_env.get_template('default.dot.j2')
    for s in template.generate(context):
        args.outfile.write(s)


def main():
    args = _args()
    code = _do(args)
    return code

if __name__ == '__main__':
    exit(main())
