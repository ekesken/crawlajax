#!/usr/bin/python

import unittest
import os
import shutil
from crawlajax import CrawlAjax


class CrawlAjaxTest(unittest.TestCase):

    def setUp(self):
        self.instance = CrawlAjax(webfolder="testwww", snapshot_cmd="echo %s")
        os.path.isdir("testwww") and shutil.rmtree("testwww")

    def tearDown(self):
        self.instance = CrawlAjax("testwww")
        os.path.isdir("testwww") and shutil.rmtree("testwww")

    def testSnapshot(self):
        self.assertEqual(self.instance.snapshot(None), 0)
        self.assertEqual(self.instance.snapshot([]), 0)
        self.assertEqual(self.instance.snapshot(["http://example.com"]), 0)
        self.assertEqual(self.instance.snapshot(["http://example.com/#!/foo", "http://hede.com/#!/bar"]), 1)
        self.assertEqual(self.instance.snapshot(["http://example.com/#!/foo", "http://hede.com/#!/bar", "http://example.com/#!/foo"]), 1)
        self.assertEqual(self.instance.snapshot(["http://example.com/#!/foo", "http://hede.com/#!/bar", "http://example.com/#!/foo", "http://example.com/#!/bar"]), 2)

    def testPathFromURL(self):
        self.assertEqual(self.instance.pathFromURLFragment("foo/--/bar/hede"), ("testwww/foo/--/bar/hede", "index.html"))
        self.assertEqual(self.instance.pathFromURLFragment("/foo/--/bar/hede"), ("testwww//foo/--/bar/hede", "index.html"))

    def testExtractHrefsFromHTML(self):
        extractedURLs = self.instance.extractHrefsFromHTML("<a href='#!/foo/--/bar/hede'>hede</a>")
        self.assertEqual(len(extractedURLs), 1)
        self.assertEqual(extractedURLs[0], "#!/foo/--/bar/hede")
        extractedURLs = self.instance.extractHrefsFromHTML("<a href='#!/foo/--/bar/hede'>hede</a><a href='#!/bar/--/bar/hede'>hede</a><a href=\"#!/aaa/--/bar/hede\">hede</a>")
        self.assertEqual(len(extractedURLs), 3)
        self.assertEqual(extractedURLs[0], "#!/foo/--/bar/hede")
        self.assertEqual(extractedURLs[1], "#!/bar/--/bar/hede")
        self.assertEqual(extractedURLs[2], "#!/aaa/--/bar/hede")
        extractedURLs = self.instance.extractHrefsFromHTML("<a href='#!/bar/--/bar/hede'>hede</a><br />\r\n<a href=\"#!/aaa/--/bar/hede\">hede</a>")
        self.assertEqual(len(extractedURLs), 2)
        self.assertEqual(extractedURLs[0], "#!/bar/--/bar/hede")
        self.assertEqual(extractedURLs[1], "#!/aaa/--/bar/hede")

    def testSaveResponse(self):
        testfolderpath = "testwww/foo/--/bar"
        self.assertFalse(os.path.isdir(testfolderpath))
        self.assertTrue(self.instance.saveResponse("/foo/--/bar/hede", "hede"))
        self.assertTrue(os.path.isdir(testfolderpath))

if __name__ == '__main__':
    unittest.main()

