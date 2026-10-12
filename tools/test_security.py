import unittest
import build


class PublicSurfaceTest(unittest.TestCase):
    def test_only_verified_deletion_form_is_allowed(self):
        build.Page('account-deletion.html').feed('<form id="deletion-form" hidden></form>')
        for page, html in [('privacy.html', '<form id="deletion-form"></form>'),
                           ('account-deletion.html', '<form id="upload"></form>'),
                           ('account-deletion.html', '<iframe src="https://evil.invalid"></iframe>')]:
            with self.assertRaises(AssertionError):
                build.Page(page).feed(html)

    def test_deletion_runtime_is_in_the_exact_public_allowlist(self):
        for name in ('page.mjs', 'delete-flow.mjs', 'firebase-public-config.json', 'deletion.css'):
            self.assertIn(name, build.PUBLIC)
        self.assertNotIn('tools/test_security.py', build.PUBLIC)


if __name__ == '__main__':
    unittest.main()
