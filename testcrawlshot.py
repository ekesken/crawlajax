import unittest
import os
from crawlshot import CrawlShot


class CrawlShotTest(unittest.TestCase):

    def setUp(self):
        self.instance = CrawlShot("testwww")

    def testSnapshot(self):
        self.assertEqual(self.instance.snapshot(None), 0)
        self.assertEqual(self.instance.snapshot([]), 0)
        self.assertEqual(self.instance.snapshot(["http://google.com"]), 1)
        self.assertEqual(self.instance.snapshot(["http://google.com", "http://hede.com"]), 2)
        self.assertEqual(self.instance.snapshot(["http://google.com", "http://hede.com", "http://google.com"]), 2)

    def testPathFromURL(self):
        self.assertEqual(self.instance.pathFromURL("foo/--/bar/hede"), ("testwww/foo/--/bar", "hede"))
        self.assertEqual(self.instance.pathFromURL("!foo/--/bar/hede"), ("testwww/!foo/--/bar", "hede"))
        self.assertEqual(self.instance.pathFromURL("#foo/--/bar/hede"), ("testwww/#foo/--/bar", "hede"))
        self.assertEqual(self.instance.pathFromURL("#!foo/--/bar/hede"), ("testwww/foo/--/bar", "hede"))
        self.assertEqual(self.instance.pathFromURL("#!/foo/--/bar/hede"), ("testwww//foo/--/bar", "hede"))
        self.assertEqual(self.instance.pathFromURL("/#!/foo/--/bar/hede"), ("testwww//foo/--/bar", "hede"))
        self.assertEqual(self.instance.pathFromURL("http://example.com#!foo/--/bar/hede"), ("testwww/foo/--/bar", "hede"))
        self.assertEqual(self.instance.pathFromURL("http://example.com#!/foo/--/bar/hede"), ("testwww//foo/--/bar", "hede"))
        self.assertEqual(self.instance.pathFromURL("http://example.com/#!/foo/--/bar/hede"), ("testwww//foo/--/bar", "hede"))

    def testSaveResponse(self):
        testfolderpath = "testwww/foo/--/bar"
        os.path.isdir(testfolderpath) and os.removedirs(testfolderpath)
        self.assertFalse(os.path.isdir(testfolderpath))
        self.assertTrue(self.instance.saveResponse("#!/foo/--/bar/hede", ""))
        self.assertTrue(os.path.isdir(testfolderpath))

if __name__ == '__main__':
    unittest.main()

