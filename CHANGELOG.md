# CHANGELOG

## v0.3a2

Date: 2022-3-18

- New:
  - Add "--python/-P" option
  - Add Dockerfile and docker hub repository "liuxueyan/pipdot"

## v0.3a1

Date: 2022-2-28

- Changes:

  - Now it's no longer dependent on `pip` during setup.

    The packaging/distribution features are now based on `importlib-metadata` and `packaging`,
    and all dependencies are vendored.

  - Command line interface was modified.

  - `dot` template slightly optimized.

## v0.2

date: 2022-2-28

- Update:
  - Update `Jinja2` to `>=2.0,<4.0`
  - Update `pip` to `>=22.0`

- Change:
  - Rename CLI argument `outfile` to `output`, and the default is `stdout`.

- Add:
  - A new `--installed-only` CLI argument.

- Optimize:
  - Better `extras` nodes and edges in dot template.

- Remove:
  - Remove `setuptools_scm_git_archive` dependency in project building.

## v0.1

date: 2021-2-5
