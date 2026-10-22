"""Black-box mutation checks for the package validator (stdlib only)."""
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PackageValidation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'hmy-wiki-writing'
        self.root.mkdir()
        # Copy the intended distributable, never local runs or credentials.
        manifest = ROOT / 'scripts/package-files.json'
        self.assertTrue(manifest.exists(), 'distributable manifest is required')
        for rel in json.loads(manifest.read_text(encoding='utf-8')):
            src, dst = ROOT / rel, self.root / rel
            self.assertTrue(src.is_file(), f'missing package file: {rel}')
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    def tearDown(self):
        self.tmp.cleanup()
    def run_validator(self):
        proc = subprocess.run([sys.executable, '-X', 'utf8', str(self.root/'scripts/validate.py')],
                              capture_output=True, text=True, encoding='utf-8')
        return proc.returncode, proc.stdout
    def mutate(self, path, fn):
        p = self.root/path
        p.write_text(fn(p.read_text(encoding='utf-8')),encoding='utf-8')
    def test_clean_package_passes(self):
        code, output = self.run_validator()
        self.assertEqual(code, 0, output)
    def test_missing_reference_fails(self):
        (self.root/'references/frontmatter.md').unlink()
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_unknown_file_fails(self):
        (self.root/'private-export.txt').write_text('not distributable',encoding='utf-8')
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_broken_relative_anchor_fails(self):
        self.mutate('README.md', lambda s:s+'\n[bad](references/frontmatter.md#missing-heading)\n')
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_frontmatter_loss_fails(self):
        self.mutate('examples/fixtures/vault/01_하드웨어/M.2 점검.md',
                    lambda s:s.replace('  preserve: true\n',''))
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_image_loss_fails(self):
        self.mutate('examples/fixtures/vault/01_하드웨어/M.2 점검.md',
                    lambda s:s.replace('![CPU 직결과 칩셋 경유의 개념도](../_assets/data-path.svg)',''))
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_missing_wikilink_target_fails(self):
        self.mutate('examples/fixtures/vault/01_하드웨어/NVMe.md',lambda s:s+'\n[[없는 문서]]\n')
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_unclosed_fence_fails(self):
        self.mutate('examples/hmy-blocks.md',lambda s:s+'\n~~~hmy-spec\ntype: custom\n')
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_footnote_loss_fails(self):
        self.mutate('examples/fixtures/vault/01_하드웨어/M.2 점검.md',
                    lambda s:'\n'.join(x for x in s.splitlines() if not x.startswith('[^scope]:')))
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_active_visual_asset_is_rejected(self):
        self.mutate('examples/fixtures/vault/_assets/cpu-direct.svg',
                    lambda s:s.replace('<svg ', '<svg onload="bad()" ', 1))
        self.assertNotEqual(self.run_validator()[0], 0)
    def test_browser_requires_every_source_fixture(self):
        required=runpy.run_path(str(self.root/'scripts/verify-quartz.py'))['required_pages']
        fixtures=self.root/'.local/tiny-vault';fixtures.mkdir(parents=True)
        (fixtures/'AMD.md').write_text('---\ntitle: AMD\n---\n# AMD\n',encoding='utf-8')
        public=self.root/'.local/public';public.mkdir()
        index={'amd':{'title':'AMD'},'specimens':{'title':'블록 표본'}}
        (public/'amd.html').write_text('<article>AMD</article>',encoding='utf-8')
        (public/'specimens.html').write_text('<article>blocks</article>',encoding='utf-8')
        self.assertEqual(len(required(public,index,fixtures)),2)
        (public/'amd.html').unlink()
        with self.assertRaisesRegex(FileNotFoundError,'AMD'): required(public,index,fixtures)
        (public/'amd.html').write_text('<article>AMD</article>',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'AMD'): required(public,{'specimens':index['specimens']},fixtures)
    def test_browser_requires_source_fixture_inventory(self):
        required=runpy.run_path(str(self.root/'scripts/verify-quartz.py'))['required_pages']
        with self.assertRaisesRegex(ValueError,'No source fixtures'):
            required(self.root,{},self.root/'.local/absent')
    def test_local_path_is_rejected(self):
        self.mutate('README.md',lambda s:s+'\n'+chr(67)+':/'+ 'Users/' + 'private/document.md\n')
        self.assertNotEqual(self.run_validator()[0], 0)

if __name__ == '__main__':
    unittest.main()
