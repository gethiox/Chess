from os.path import dirname

from fabric.context_managers import lcd
from fabric.operations import local
from fabric.state import env
from setuptools import find_packages

ROOT_DIR = dirname(env['real_fabfile'])
SRC_DIR = '{}/src/'.format(ROOT_DIR)


def _get_packages(exclude=('*tests*',)):
    return find_packages(where=SRC_DIR, exclude=exclude)


def nosetests(cov=''):
    """
    Run test suite
    """
    flags = ''
    if cov:
        flags += '--with-coverage --cover-html --cover-html-dir=coverage'

    with lcd(SRC_DIR):
        local("nosetests --rednose {flags}".format(
            flags=flags,
        ))


def pytest():
    """
    Run test suite
    """
    with lcd(SRC_DIR):
        local("python -m pytest")


def qa():
    """
    Quality assurance test
    """
    with lcd(SRC_DIR):
        local('pylint {packages} --output-format=colorized'.format(
            packages=' '.join(_get_packages())
        ))


def profile(sort=None):
    flags = ''
    if sort:
        flags = '--sort=%s' % sort
    with lcd(SRC_DIR):
        local('python -B -m cProfile {flags} example_profile.py'.format(flags=flags))


def fmt():
    """
    Run pep8
    """
    with lcd(SRC_DIR):
        local('autopep8 --in-place --aggressive --max-line-length=120 -r .')
