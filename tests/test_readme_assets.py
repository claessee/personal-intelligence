import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('image_release_checker', ROOT / 'scripts/check_release.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ReadmeAssetTests(unittest.TestCase):
    def test_malformed_or_unreviewed_png_blocks_release(self):
        for case in ['wrong_format', 'bad_checksum', 'unreviewed_path']:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                inventory = json.loads((ROOT / 'release-files.json').read_text())
                for rel in inventory['files']:
                    target = root / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / rel, target)
                self.assertEqual(checker.check(root)['status'], 'PASS')
                image = root / 'assets/readme/how-it-works.png'
                if case == 'wrong_format':
                    image.write_bytes(b'not an image')
                    reason = 'invalid README PNG'
                elif case == 'bad_checksum':
                    data = bytearray(image.read_bytes())
                    data[29] ^= 1
                    image.write_bytes(data)
                    reason = 'invalid README PNG'
                else:
                    extra = 'assets/readme/unreviewed.png'
                    shutil.copyfile(image, root / extra)
                    inventory['files'].append(extra)
                    (root / 'release-files.json').write_text(json.dumps(inventory))
                    reason = 'unapproved file type'
                with self.assertRaisesRegex(ValueError, reason):
                    checker.check(root)


if __name__ == '__main__':
    unittest.main()
