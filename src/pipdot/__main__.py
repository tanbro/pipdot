import argparse
import os
import sys
from itertools import chain

import jinja2 as j2
from pip._internal.utils.misc import (dist_in_site_packages, dist_in_usersite,
                                      dist_is_editable, dist_is_local,
                                      get_installed_distributions)

from .version import version as __version__

PACKAGE = PROG = 'pipdot'

BOOLEAN_MAPPING = {
    0: ('0', 'n', 'no', 'off', 'false'),
    1: ('1', 'y', 'yes', 'on', 'true'),
}
BOOLEAN_CHOICES = list(chain.from_iterable(BOOLEAN_MAPPING.values()))


def s2b(s):
    if s in BOOLEAN_MAPPING[0]:
        return False
    elif s in BOOLEAN_MAPPING[1]:
        return True
    else:
        raise ValueError(s)


def get_args():
    prog = PROG
    _, tail = os.path.split(sys.argv[0])
    root, _ = os.path.splitext(tail)
    if root == __name__:
        prog = '{} -m {}'.format(sys.executable, PACKAGE)
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument(
        '--local-only', '-l', choices=BOOLEAN_CHOICES, default='true',
        help='(default=%(default)s)'
    )
    parser.add_argument(
        '--include-editables', '-e', choices=BOOLEAN_CHOICES, default='true',
        help='(default=%(default)s)'
    )
    parser.add_argument(
        '--editables-only', choices=BOOLEAN_CHOICES, default='false',
        help='(default=%(default)s)'
    )
    parser.add_argument(
        '--user-only', '-u', choices=BOOLEAN_CHOICES, default='false',
        help='(default=%(default)s)'
    )
    parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s {0} from {1} ({2} {3[0]}.{3[1]})'.format(
            __version__, sys.argv[0], sys.implementation.name, sys.version_info
        )
    )
    args = parser.parse_args()
    print(args)


def main(args):
    return
    installed_distributions = get_installed_distributions(local_only=True)
    editable_distributions = []
    local_distributions = []
    user_distributions = []
    system_distributions = []

    for dist in installed_distributions:
        if dist_is_editable(dist):
            editable_distributions.append(dist)
        if dist_is_local(dist):
            local_distributions.append(dist)
        if dist_in_usersite(dist):
            user_distributions.append(dist)
        if dist_in_site_packages(dist):
            system_distributions.append(dist)

    context = dict(
        installed_distributions=installed_distributions,
        editable_distributions=editable_distributions,
        local_distributions=local_distributions,
        user_distributions=user_distributions,
        system_distributions=system_distributions,
    )

    j2_env = j2.Environment(
        loader=j2.FileSystemLoader(''),
        extensions=['jinja2.ext.do']
    )
    template = j2_env.get_template('graph.dot.j2')

    with open('out.dot', 'w') as fp:
        for s in template.generate(
            context,
            show_extras=True,
            show_extras_label=True,
        ):
            fp.write(s)


if __name__ == '__main__':
    args = get_args()
    code = main(args)
    exit(code)
