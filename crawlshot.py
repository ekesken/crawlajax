#!/usr/bin/python
import sys
import os
import re
import logging

logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', filename='crawlshot.log', level=logging.DEBUG)

class CrawlShot:

    def __init__(self, webfolder = "www"):
        self.webfolder = webfolder

    def snapshot(self, newURLs, fetchedURLs = []):
        if newURLs is None or len(newURLs) == 0:
            return 0
        fetchedURLs = fetchedURLs[:]
        logging.debug("URLs: %s, fetchedURLs: %s" % (newURLs, fetchedURLs))
        processedURLCount = 0
        for newURL in newURLs:
            if newURL in fetchedURLs:
                logging.debug("URL-'%s' was fetched before", newURL)
                continue
            logging.info("fetching URL-'%s'" % (newURL))
            fetchedURLs.append(newURL)
            # response = os.popen("phantomjs phantomjs/snapshot.js '%s'" % (newURL)).read()
            response = newURL
            self.saveResponse(newURL, response)
            foundURLs = self.extractHrefsFromHTML(response)
            self.snapshot(foundURLs, fetchedURLs)
            processedURLCount += 1
        return processedURLCount

    def extractHrefsFromHTML(self, response):
        foundURLs = []
        logging.debug("extracted %d URL" % (len(foundURLs)))
        return foundURLs

    def saveResponse(self, requestURL, response):
        (folder, path) = self.pathFromURL(requestURL)
        not os.path.isdir(folder) and os.makedirs(folder)
        logging.debug("saved URL-'%s' response at folder-'%s'" % (requestURL, folder))
        return True

    def pathFromURL(self, requestURL):
        folderpath = os.path.dirname(re.sub(".*#!", "", requestURL))
        filename = os.path.basename(requestURL)
        return (self.webfolder + "/" + folderpath, filename)

if __name__ == '__main__':
    URLs = sys.argv[1:]
    cs = CrawlShot()
    cs.snapshot(URLs)

