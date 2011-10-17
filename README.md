ABOUT
=====

a crawler for ajax applications using hashbang urls.

creating a html snapshot of your site for googlebot by walking through hashbang links.

sample usage:

<code>
./crawlajax.py 'http://2011.jsconf.us/#!/schedule'
</code>

this command create following folder structure and files

<pre>
|- www
 \|- schedule
  |\|- index.html
  |- news
  |\|- index.html
  |- speakers
  |\|- index.html
  ...
</pre>

you can use an apache server now to serve your static html snapshots by forwarding
requests with _escaped_fragment_ parameter to this folder.

<pre>
http://2011.jsconf.us/?_escaped_fragment_=/schedule => http://2011.jsconf.us/googlebot/schedule/index.html
</pre>

using [phantomjs](http://www.phantomjs.org/) to take html snapshot of rendered
dom. you can change snapshot command via construction parameter snapshot_cmd.

check instructions at

http://code.google.com/web/ajaxcrawling/docs/getting-started.html

for making ajax applications crawlable.

we tried using htmlunit as google suggests at first, but we had performance
problems, so we chose this way.

project satisfies only our applications requirements for now, you're free to
fork and enrich it according to your needs.

INSTALLATION
============

dependencies:
* python-2.6.6
* phantomjs-1.3.0

see instructions to build and install phantomjs:
* http://code.google.com/p/phantomjs/wiki/BuildInstructions
* http://code.google.com/p/phantomjs/wiki/Installation

TEST
====

you can run unit tests via cmd:

<code>
./testcrawlajax.py
</code>


