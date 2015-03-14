# Intro #

**_NOTE 7/13/2011:  Version 2.0 of Tornado breaks ButtonBoard. If you have it installed you will have to remove it and re-install 1.1 with:_
```
sudo easy_install -m tornado==2.0
sudo easy_install tornado==1.1
```**


_**UPDATE:  Version 0.4.1 5/26/2011** minor fixes_


ButtonBoard is designed for remotely running scripts and commands on a media server Mac.   It was developed and tested on a Mac (OS X 10.6), but there is no reason it shouldn't run on Linux or possibly a Windows machine (with some work!)

It presents an iPhone Springboard-like grid of graphic buttons, and each button press will launch a different custom script or program as defined by the user.  It was primarily designed to be used on an iPhone, but it works great on Safari or Google Chrome, IE9, and Firefox 4+.  It can be added to the iPhone/iPad homescreen and run like a regular local app.  Since it also supports caching page elements on iOS, is can start up very fast, even when running away from your LAN.

ButtonBoard supports a cookie-based authentication with a password, so once you log in, your cookie is good for a month.

Possible uses are controlling A/V equipment using IR, running batch scripts, restarting crashed server processes, media center control, etc.  I actually got started on this project when I got a USB-based IR transceiver, wanted to be able to control my stereo and TV from my phone..

![http://lh4.ggpht.com/_DCpjkyIUFB0/TLZvihXj2rI/AAAAAAAAAF4/RuzrnwSmHGc/s400/Photo%20Oct%2013%2C%207%2045%2013%20PM.jpg](http://lh4.ggpht.com/_DCpjkyIUFB0/TLZvihXj2rI/AAAAAAAAAF4/RuzrnwSmHGc/s400/Photo%20Oct%2013%2C%207%2045%2013%20PM.jpg)

While in the future, I may end up adding a configuration GUI, for now the end-user is expected to be able to edit the commands file ("cmds.xml"), write/edit the the underlying shell scripts (or apple script, or batch files), and find/make cool icon files :-)

# Setup #

## Prerequisites ##
Before you begin you need to install some python packages.  Fortunately this is super-easy on Macs now:

```
sudo easy_install tornado==1.1
sudo easy_install elementtree
```


On OS X 10.6 you can optionally also do this:
```
sudo easy_install pil
```

PIL is the Python Imaging Library, which will allow ButtonBoard to auto-resize your icons for faster serving.  This is an optional requirement.

By default, installing this on 10.6 should provide support for PNG images.  If you already have a libjpeg installed (i.e. via Mac Ports), PIL should be able to handle JPG images too.

_(For OS X 10.5 you may optionally download and install PIL manually. Here is a blog entry detailing how: http://passingcuriosity.com/2009/installing-pil-on-mac-os-x-leopard/  )_

### Download and Run ###

Once this is done,  download the dmg file from the Google Code site (http://code.google.com/p/buttonboard), and extract the app.  The app bundle was generated by the very handy "Platypus" app.  Run the app, and a window should open up.   You should now be able to navigate to `http://{hostname}:8888`, and the default password is "changeme"

Many of the default commands probably won't do anything on your system, but the iTunes buttons should work.

# Configuring #

The first time it is run, the app created a folder: `~/Library/Application Support/ButtonBoard`.

```


~/Library/
	|
	Application Support/
		|
		----ButtonBoard/
			  |
			  |--default/
			  |    |----cmds.xml
			  |    |----images/
			  |    |----scripts/
			  |
			  |--user/
			  |    |----settings.xml
			  |    |----cmds.xml
			  |    |----images/
			  |    |----scripts/
```

All reference to folder names below are relative to this `ButtonBoard` folder.

## Settings ##
You first want to edit `user/settings.xml` to change the password, and probably the port.

## Commands ##
To add commands, first have a look at `default/cmds.xml` .  This should give a good idea of the structure of the XML, and the file is well-documented.  To add new commands, edit the XML in **`user`**`/cmds.xml`.  This file has two parts: the details of each command, and then a layout, defining which command button goes in which row.

Here is sample command definition for playing a random album on iTunes, using some applescript I found on the net:

```
	<cmd name="random_album_itunes">
		<label>Random Album</label>
		<exec>itunes_random_album.applescript</exec>
		<icon>itunes.png</icon>
		<badge>shuffle-red.png</badge>
	</cmd>
```

**All customizations should be done in the user folder, as the Mac version of the app will overwrite the other folders on every start-up**


### Scripts ###
Any kind of script you can launch from the command-line is fair game.  The XML supports passing in parameters if you want.  You can put your scripts into `user/scripts` or just reference by absolute path anywhere on your filesystem.  You can also call binaries directly, but this can be limiting since the commands are not then run in the context of shell.

Don't forget to make your new scripts executable (i.e. "`chmod a+x scriptfile`")

See [SampleScripts](SampleScripts.md) for examples

### Icons ###

Plunk your icons into `user/images`.  ButtonBoard supports all type of icon images that be displayed on your web browser, and can be any size, but best to start with a square PNG  images with transparencies.  If you have PIL installed, when the app runs, it will automatically resize your images down to 128x128. The browser will take care of of the "button-ification" of the image, rounding the corners, and overlaying the mask, so no image editing needed.

A great site for free icons is: http://icons.mysitemyway.com/