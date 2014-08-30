import ast
import os.path

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class BaseCheckerTestCase(unittest.TestCase):
    def _get_fixture(self, filename):
        fixture_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures', filename)
        return open(fixture_path)

    def get_tree(self, fixture):
        return ast.parse(self._get_fixture(fixture).read())
