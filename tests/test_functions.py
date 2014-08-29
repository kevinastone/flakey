from .base import BaseCheckerTestCase

from flakey.checks import BannedFunctionChecker


class TestBannedFunctionTestCase(BaseCheckerTestCase):
    fixture = 'function_example.py'
    function_name = 'django.utils.strip_tags'

    def test_import_from(self):
        class CustomBannedFunctionChecker(BannedFunctionChecker):
            functions = {
                self.function_name: 'B201',
            }

        checker = CustomBannedFunctionChecker(self.tree)
        results = list(checker.run())
        line_numbers = [err[0] for err in results]
        for expected_match in [5, 8]:
            self.assertIn(expected_match, line_numbers)
