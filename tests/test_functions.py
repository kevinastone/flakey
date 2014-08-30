from .base import BaseCheckerTestCase

from flakey.checks import BannedFunctionChecker


class TestBannedFunctionTestCase(BaseCheckerTestCase):
    function_name = 'django.utils.strip_tags'

    def test_import_from(self):
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        tree = self.get_tree('from_import_function_example.py')
        checker = CustomBannedFunctionChecker(tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        for expected_match in [3, 6]:
            self.assertIn(expected_match, line_numbers)

    def test_import_module(self):
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        tree = self.get_tree('absolute_import_function_example.py')
        checker = CustomBannedFunctionChecker(tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        for expected_match in [3, 6]:
            self.assertIn(expected_match, line_numbers)

    def test_hybrid_import(self):
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        tree = self.get_tree('hybrid_import_function_example.py')
        checker = CustomBannedFunctionChecker(tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        for expected_match in [3, 6]:
            self.assertIn(expected_match, line_numbers)
