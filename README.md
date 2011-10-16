a crawler for ajax applications using hashbang urls.

creating a snapshot of your site for googlebot by walking through hashbang links.

sample usage:

<code>
./crawlshot.py 'http://2011.jsconf.us/#!/schedule'
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

you can use an apache server now to serve your static snapshots by forwarding
requests with _escaped_fragment_ parameter to this folder.

<code>
http://2011.jsconf.us/?_escaped_fragment_=/schedule => http://2011.jsconf.us/?_escaped_fragment_=/schedule/index.html
</code>

using [phantomjs](http://www.phantomjs.org/) to take snapshot of rendered dom.

check instructions at

http://code.google.com/web/ajaxcrawling/docs/getting-started.html

for making ajax applications crawlable.

we tried using htmlunit as google suggests at first, but we had performance
problems, so we chose this way.


project satisfies only our applications requirements for now, you're free to
fork and enrich it according to your needs.

