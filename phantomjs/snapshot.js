var page = new WebPage(),
    t, address;

page.settings.userAgent = 'googlebot';
page.settings.loadImages = false;
page.settings.loadPlugins = true;

if (phantom.args.length === 0) {
    console.log('Usage: snapshot.js <some URL>');
    phantom.exit();
} else {
    t = Date.now();
    address = phantom.args[0];
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('FAIL to load the address');
        } else {
            // t = Date.now() - t;
            // console.log('Page title is ' + page.evaluate(function () {
            //     return document.title;
            // }));
            // console.log('Loading time ' + t + ' msec');
            console.log(page.content);
        }
        phantom.exit();
    });
}
