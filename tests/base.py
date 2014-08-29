import ast
import os.path

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class BaseCheckerTestCase(unittest.TestCase):
    fixture = 'function_example.py'
    function_name = 'django.utils.strip_tags'

    def _get_fixture(self, filename):
        fixture_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures', self.fixture)
        return file(fixture_path)

    def setUp(self):
        self.tree = ast.parse(self._get_fixture(self.fixture).read())
