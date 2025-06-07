# Tests for google-calendar-api

This directory contains unit tests and functional tests for google-calendar-api. To run them all, make sure
you've installed [tox](https://tox.wiki/) and a supported python version.

Install tox via pipx (recommended) or pip:

```shell
pip install pipx
pipx install tox
tox --help
```

Run all tests:

```shell
git submodule update --init
tox
```

Run individual configurations:

```shell
tox -e py312,cli
```

The supported tox testing envs are listed and configured in [../tox.ini](../tox.ini).

## Unit tests

The python test files under tests/ are unit tests run via [pytest](https://pytest.org/). If you
hit failures, you can start a debugger with the --pdb flag to troubleshoot (probably also
specifying an individual test env and test to debug). Example:

```shell
tox -e py312 -- tests/test_gcalcli.py::test_format_event_time_from_iso_valid_date --pdb
```
