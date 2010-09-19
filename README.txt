ButtonBoard is a very simple PHP/JS web app for controlling certain features of a home theater PC, 
but could be used for any server that supports PHP.   It was developed and tested on a Mac, 
but there is no reason it shouldn't run on Linux or possibly a Windows machine.

It presents an iPhone Springboard-like grid of graphic buttons, and its primary client is
intended to be an iOS device, but it seems to look great on Safari or Google Chrome on a PC.
Each button press will launch a different custom script or program as defined by the user.

This is not a commercial product and the end-user is expected to be able to edit the commands file
("cmds.php"), write/edit the the underlying shell scripts (or apple script, or batch files), and 
generate icon files.

This is my first foray into web development in many years, so I am sure there are things that are
clunky and buggy.  I basically cobbled together pieces found in other projects on the web.
My main moviation for writing this was the aquisition of a USB-UIRT infrared 
tranceiver, which would allow a mac mini to control its associated AV equipment. 

Once set up, it was fairly easy to add other button/command combos like hiding/showing the media center app,
relaunching it and other apps, etc.

To install, just un-tar into the document root of your webserver, and point your iPhone browser
as http://{your.mediaserver}/buttonboard

Have fun!

anville@hotmail.com

-------------------------------------------------
Some links to check out:

MAMP - http://www.mamp.info/en/index.html
xammp - http://www.apachefriends.org/en/xampp.html
USB-UIRT - http://www.usbuirt.com/
Ribsu - http://www.xyster.net/ribsu/
        http://code.google.com/p/ribsu/
HTPC-Launchboard -
        http://www.beekerstudios.com/mind/introducing-htpc-launchboard-iphone-web-app
Plex  - http://www.plexapp.com/
Transmission -  http://www.transmissionbt.com/
Icon Generator - http://www.quirco.com/iPhoneIcon/
