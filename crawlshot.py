#!/usr/bin/python
import sys
import os
import re
import logging
from urlparse import urlparse

# logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', filename='crawlshot.log', level=logging.DEBUG)
logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.INFO)

class CrawlShot:

    def __init__(self, webfolder = "www", testmode = False):
        self.domain = None
        self.webfolder = webfolder
        self.testmode = testmode

    def snapshot(self, newURLs, fetchedURLFragments = []):
        if newURLs is None or len(newURLs) == 0:
            return 0
        fetchedURLFragments = fetchedURLFragments[:]
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
            if self.testmode == True:
                response = newURLFragment
            else:
                response = os.popen("phantomjs phantomjs/snapshot.js '%s'" % (newURL)).read()
            self.saveResponse(newURLFragment, response)
            foundURLs = self.extractHrefsFromHTML(response)
            self.snapshot(foundURLs, fetchedURLFragments)
            processedURLCount += 1
        return processedURLCount

    def extractHrefsFromHTML(self, response):
        foundURLs = re.findall("href=['\"]([^'\"]*)['\"]", response)
        logging.debug("extracted %d URL" % (len(foundURLs)))
        # return [urlparse(foundURL).fragment[1:] for foundURL in foundURLs if foundURL.find("#!") != -1] # strips ! character from fragment
        return foundURLs

    def saveResponse(self, urlFragment, response):
        (folderpath, filename) = self.pathFromURLFragment(urlFragment)
        not os.path.isdir(folderpath) and os.makedirs(folderpath)
        f = open(folderpath + "/" + filename, "w")
        f.write(response)
        f.close()
        logging.debug("saved URL-'%s' response at '%s/%s'" % (urlFragment, folderpath, filename))
        return True

    def pathFromURLFragment(self, urlFragment):
        return (self.webfolder + "/" + urlFragment, "index.html")

if __name__ == '__main__':
    URLs = sys.argv[1:]
    cs = CrawlShot()
    cs.snapshot(URLs)

