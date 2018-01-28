from os.path import dirname

from fabric.context_managers import lcd
from fabric.operations import local
from fabric.state import env

ROOT_DIR = dirname(env['real_fabfile'])
SRC_DIR = '{}/chess/'.format(ROOT_DIR)


def test():
    """
    Run test suite
    """
    with lcd(ROOT_DIR):
        local("pytest --cov=./chess ./tests")


def qa():
    """
    Quality assurance test
    """
    with lcd(ROOT_DIR):
        local('pylint ./chess --output-format=colorized')


def profile(sort=None):
    flags = ''
    if sort:
        flags = '--sort=%s' % sort
    with lcd(ROOT_DIR):
        local('python -m cProfile {flags} ./example_profile.py --silent'.format(flags=flags))


def fmt():
    """
    Run pep8
    """
    with lcd(ROOT_DIR):
        local('autopep8 --in-place --aggressive --max-line-length=120 -r ./chess')
