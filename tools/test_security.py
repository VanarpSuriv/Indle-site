import unittest
from pathlib import Path
import shutil
import tempfile
from unittest.mock import patch
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

    def test_exact_config_allows_git_and_windows_line_endings_but_not_changed_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in build.SOURCE:
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(build.ROOT / name, destination)
            config = root / 'firebase-public-config.json'
            canonical = config.read_bytes().replace(b'\r\n', b'\n')
            with patch.object(build, 'ROOT', root):
                for raw in (canonical, canonical.replace(b'\n', b'\r\n')):
                    config.write_bytes(raw)
                    self.assertEqual(5, len(build.validate()))
                config.write_bytes(canonical.replace(b'indicgame', b'not-the-reviewed-project'))
                with self.assertRaises(AssertionError):
                    build.validate()


if __name__ == '__main__':
    unittest.main()
