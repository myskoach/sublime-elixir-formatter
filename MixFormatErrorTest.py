import unittest

from MixFormatError import MixFormatError

class TestSyntaxErrors(unittest.TestCase):
    def test_unexpected_token_ex_1_10(self):
        error = MixFormatError("** (SyntaxError) lib/skoach_bot/repo/users.ex:150: unexpected token: end. The \"{\" at line 149 is missing terminator \"}\"", "")

        self.assertTrue(error.did_match)
        self.assertEqual(error.line, 150)
        self.assertEqual(error.status_message, "SyntaxError - unexpected token: end. The \"{\" at line 149 is missing terminator \"}\"")

    def test_unexpected_token_ex_1_11(self):
        error = MixFormatError("** (SyntaxError) opt/skoach/apps/skoach_bot/lib/skoach_bot/repo/users.ex:150:5: unexpected reserved word: end. The \"{\" at line 149 is missing terminator \"}\"", "")

        self.assertTrue(error.did_match)
        self.assertEqual(error.line, 150)
        self.assertEqual(error.status_message, "SyntaxError - unexpected reserved word: end. The \"{\" at line 149 is missing terminator \"}\"")

class TestDependecyErrors(unittest.TestCase):
    def test_dependency_error_ex_1_10(self):
        error = MixFormatError("** (Mix) Unknown dependency :assertions given to :import_deps in the formatter configuration. The dependency is not listed in your mix.exs for environment :dev", "")

        self.assertTrue(error.did_match)
        self.assertIsNone(error.line)
        self.assertEqual(error.status_message, "unknown dependency: :assertions given to :import_deps for env :dev")

if __name__ == '__main__':
    unittest.main()
