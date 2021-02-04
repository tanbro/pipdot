from pip._internal.utils.misc import get_installed_distributions, dist_is_local, dist_in_usersite, dist_in_site_packages, dist_is_editable
import jinja2 as j2

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

# for dist in distributions:
#     if dist.key == 'setuptools':
#         break


# dist.requires()
