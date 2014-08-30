import unittest

from flakey.checks import BannedFunctionChecker

from .base import BaseCheckerTestCase


class TestBannedFunctionTestCase(BaseCheckerTestCase):
    function_name = 'alpha.bravo.charlie'

    def assert_items_equal(self, first, second, message=None):
        self.assertEqual(set(first), set(second), message)

    def test_import_from(self):
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        tree = self.get_tree('from_import_function_example.py')
        checker = CustomBannedFunctionChecker(tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        self.assert_items_equal(line_numbers, [3, 6])

    def test_import_module(self):
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        tree = self.get_tree('absolute_import_function_example.py')
        checker = CustomBannedFunctionChecker(tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        self.assert_items_equal(line_numbers, [3, 6])

    def test_hybrid_import(self):
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        tree = self.get_tree('hybrid_import_function_example.py')
        checker = CustomBannedFunctionChecker(tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        self.assert_items_equal(line_numbers, [3, 6])

    def test_function_returns(self):
        """
        Ensure we can resolve functions returned by other functions
        """
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        tree = self.get_tree('function_returning_function_example.py')
        checker = CustomBannedFunctionChecker(tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        self.assert_items_equal(line_numbers, [6])

    @unittest.skip("Lambdas not supported yet")
    def test_lambda(self):
        """
        We can't parse lambdas are functions returns yet, but at least test it doesn't explode.
        """
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        tree = self.get_tree('lambda_example.py')
        checker = CustomBannedFunctionChecker(tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        self.assert_items_equal(line_numbers, [4])
