import importlib.util, pathlib, unittest
spec=importlib.util.spec_from_file_location('preserve',pathlib.Path(__file__).with_name('check-preservation.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Preservation(unittest.TestCase):
 def test_light_rewrite_requires_region(self): self.assertEqual(m.check('# A\noriginal','# A\nrewritten','light')['status'],'Failed')
 def test_old_without_new(self): self.assertEqual(m.check('A','A','light','A',None)['status'],'Failed')
 def test_new_without_old(self): self.assertEqual(m.check('A','A','light',None,'B')['status'],'Failed')
 def test_same(self): self.assertEqual(m.check('same','same')['status'],'Passed')
 def test_link_loss(self): self.assertEqual(m.check('[[PCI Express]]','PCI Express')['status'],'Failed')
 def test_image_loss(self): self.assertEqual(m.check('![diagram](image.svg)','')['status'],'Failed')
 def test_nested_frontmatter_loss(self): self.assertEqual(m.check('---\ncustom:\n  keep: true\n---\nbody','---\n---\nbody')['status'],'Failed')
 def test_heading_change(self): self.assertEqual(m.check('# A\ntext','# B\ntext','light')['status'],'Failed')
 def test_scoped_change(self):
  self.assertEqual(m.check('A\nB','C\nB','light','A','C')['status'],'Passed')
  self.assertEqual(m.check('A\nB','C\nD','light','A','C')['status'],'Failed')
if __name__=='__main__': unittest.main()
