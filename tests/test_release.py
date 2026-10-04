import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('check_release',ROOT/'scripts/check_release.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)

class ReleaseTests(unittest.TestCase):
    def copy_inventory(self,directory):
        root=Path(directory)
        for rel in json.loads((ROOT/'release-files.json').read_text())['files']:
            target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,target)
        return root

    def test_exact_reviewed_inventory_passes(self):
        self.assertEqual(checker.check()['status'],'PASS')

    def test_unlisted_private_file_blocks_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root=self.copy_inventory(directory);(root/'local-private.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'inventory mismatch'):checker.check(root)

    def test_private_path_or_credential_material_blocks_release(self):
        for extra in ['/'+'Users/'+'synthetic-person/source','sk-'+'a'*32]:
            with self.subTest(kind=extra[:3]),tempfile.TemporaryDirectory() as directory:
                root=self.copy_inventory(directory);p=root/'README.md';p.write_text(p.read_text()+extra+'\n')
                with self.assertRaisesRegex(ValueError,'private path or credential-like'):checker.check(root)

    def test_symlink_blocks_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root=self.copy_inventory(directory);p=root/'LICENSE';p.unlink();p.symlink_to(root/'README.md')
            with self.assertRaisesRegex(ValueError,'symlink'):checker.check(root)

if __name__=='__main__':unittest.main()
