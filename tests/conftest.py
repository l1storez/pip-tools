import json

from pip._vendor.packaging.version import Version
from pip.req import InstallRequirement
from pytest import fixture

from piptools.repositories.base import BaseRepository
from piptools.utils import as_name_version_tuple


class FakeRepository(BaseRepository):
    def __init__(self):
        with open('tests/fixtures/fake-index.json', 'r') as f:
            self.index = json.load(f)

        with open('tests/fixtures/fake-editables.json', 'r') as f:
            self.editables = json.load(f)

    def find_best_match(self, ireq, prereleases=False):
        if ireq.editable:
            return ireq

        versions = ireq.specifier.filter(self.index[ireq.req.key], prereleases=prereleases)
        return max(versions, key=Version)

    def get_dependencies(self, ireq):
        if ireq.editable:
            return self.editables[str(ireq.link)]

        name, version = as_name_version_tuple(ireq)
        return self.index[name][version]


@fixture
def repository():
    return FakeRepository()


@fixture
def from_line():
    return InstallRequirement.from_line


@fixture
def from_editable():
    return InstallRequirement.from_editable