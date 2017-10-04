from fabric.context_managers import lcd
from fabric.operations import local
from setuptools import find_packages

SRC_DIR = 'src'


def _get_packages(exclude=('*tests*',)):
    return find_packages(where=SRC_DIR, exclude=exclude)


def test(cov=''):
    """
    Run test suite
    """
    flags = ''
    if cov:
        flags += '--with-coverage --cover-html --cover-html-dir=coverage'

    local("nosetests --rednose {flags} {dir}".format(
        flags=flags,
        dir=SRC_DIR,
    ))


def qa():
    """
    Quality assurance test
    """
    with lcd(SRC_DIR):
        local('pylint {packages} --output-format=colorized'.format(
            packages=' '.join(_get_packages())
        ))


def fmt():
    """
    Run pep8
    """
    local('autopep8 --in-place --aggressive --max-line-length=120 -r {dir}'.format(
        dir=SRC_DIR
    ))
