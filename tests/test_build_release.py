import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_release


class ArchiveTests(unittest.TestCase):
    def test_exact_archive_content_checksums_and_reproducibility(self):
        inventory = json.loads((ROOT / 'release-files.json').read_text())['files']
        plugin_prefix = 'plugins/personal-intelligence/'
        expected = {
            'personal-intelligence-v0.1.0-repository.zip': {
                'personal-intelligence/' + rel: rel for rel in inventory
            },
            'personal-intelligence-v0.1.0-plugin.zip': {
                'personal-intelligence/' + rel.removeprefix(plugin_prefix): rel
                for rel in inventory if rel.startswith(plugin_prefix)
            },
        }
        expected['personal-intelligence-v0.1.0-plugin.zip']['personal-intelligence/LICENSE'] = 'LICENSE'
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            build_release.build(first)
            build_release.build(second)
            sums = dict(line.split('  ')[::-1] for line in (Path(first) / 'SHA256SUMS.txt').read_text().splitlines())
            self.assertEqual(set(sums), set(expected))
            for name, entries in expected.items():
                archive_path = Path(first) / name
                self.assertEqual(archive_path.read_bytes(), (Path(second) / name).read_bytes())
                self.assertEqual(hashlib.sha256(archive_path.read_bytes()).hexdigest(), sums[name])
                with zipfile.ZipFile(archive_path) as archive:
                    self.assertEqual(sorted(archive.namelist()), sorted(entries))
                    for member, rel in entries.items():
                        self.assertNotIn('_prev', member)
                        self.assertEqual(archive.read(member), (ROOT / rel).read_bytes())
                        self.assertEqual(archive.getinfo(member).date_time, (2026, 10, 6, 0, 0, 0))

    def test_existing_output_refused_before_partial_build(self):
        for name in ['personal-intelligence-v0.1.0-repository.zip', 'SHA256SUMS.txt']:
            with self.subTest(existing=name), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / name
                target.write_bytes(b'invented existing draft')
                with self.assertRaisesRegex(ValueError, 'existing release output'):
                    build_release.build(directory)
                self.assertEqual([p.name for p in Path(directory).iterdir()], [name])
                self.assertEqual(target.read_bytes(), b'invented existing draft')


if __name__ == '__main__':
    unittest.main()
