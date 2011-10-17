#!/usr/bin/python

"""
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import re
import logging
from urlparse import urlparse

# logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', filename='crawlajax.log', level=logging.DEBUG)
logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.INFO)

class CrawlAjax:
    """
    creating a html snapshot of your site for googlebot by walking through hashbang links.
    """

    def __init__(self, snapshot_cmd="phantomjs phantomjs/snapshot.js '%s'", webfolder = "www"):
        self.domain = None
        self.snapshot_cmd = snapshot_cmd
        self.webfolder = webfolder

    def snapshot(self, newURLs, fetchedURLFragments = []):
        """ main method that crawls and saves html snapshots by recursive calls """
        if newURLs is None or len(newURLs) == 0:
            return 0
        fetchedURLFragments = fetchedURLFragments[:] # needed to clone solve reference problems
        # logging.debug("URLs: %s, fetchedURLFragments: %s" % (newURLs, fetchedURLFragments))
        processedURLCount = 0
        if len(newURLs) == 0:
            return 0
        if self.domain == None:
            self.domain = urlparse(newURLs[0]).netloc
            logging.debug("first URL is '%s', setting valid domain as '%s'" % (newURLs[0], self.domain))
        newURLFragments = [urlparse(newURL).fragment[1:] for newURL in newURLs if newURL.find("#!") != -1 and (urlparse(newURL).netloc == self.domain or urlparse(newURL).netloc == '')]
        logging.debug("found %d valid URLs to process" % (len(newURLFragments)))
        # ignored url path, because we don't need it for now
        # stripped ! character from fragment
        if len(newURLFragments) == 0:
            logging.warn("only URLs with #! hashbang are valid!")
            return 0
        for newURLFragment in newURLFragments:
            if newURLFragment in fetchedURLFragments:
                logging.debug("URL-'%s' was fetched before", newURLFragment)
                continue
            newURL = "http://" + self.domain + "#!" + newURLFragment
            logging.info("fetching URL-'%s'" % (newURL))
            fetchedURLFragments.append(newURLFragment)
            response = os.popen(self.snapshot_cmd % (newURL)).read()
            self.saveResponse(newURLFragment, response)
            foundURLs = self.extractHrefsFromHTML(response)
            self.snapshot(foundURLs, fetchedURLFragments)
            processedURLCount += 1
        return processedURLCount

    def extractHrefsFromHTML(self, response):
        """ collects all hrefs to an array without any modification """
        foundURLs = re.findall("href=['\"]([^'\"]*)['\"]", response)
        logging.debug("extracted %d URL" % (len(foundURLs)))
        return foundURLs

    def saveResponse(self, urlFragment, response):
        """ saves response of url to a path generated according to urlFragment """
        (folderpath, filename) = self.pathFromURLFragment(urlFragment)
        not os.path.isdir(folderpath) and os.makedirs(folderpath)
        f = open(folderpath + "/" + filename, "w")
        f.write(response)
        f.close()
        logging.debug("saved URL-'%s' response at '%s/%s'" % (urlFragment, folderpath, filename))
        return True

    def pathFromURLFragment(self, urlFragment):
        """ generates a folder path and file name for url fragment given """
        return (self.webfolder + "/" + urlFragment, "index.html")

if __name__ == '__main__':
    URLs = sys.argv[1:]
    cs = CrawlAjax()
    cs.snapshot(URLs)

