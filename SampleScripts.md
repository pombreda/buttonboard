



# Mac OS X #


## app\_send\_key.sh ##
Very generic AppleScript/Bash to send keystrokes to any app.  Takes a app name and key as argument, and sends a character as a keystroke

```
#!/bin/bash

#Takes up to 3 args:
# App name
# key to send
# optional "using" 

if [ "$3" != "" ]
then
    USING="using ($3)"
else
    USING=""
fi
echo using=$USING

/usr/bin/osascript <<EOF

tell application "$1"
    activate
    tell application "System Events" to keystroke $2 $USING
end tell

```


command-line usage:
```
app_send_key.sh "Hulu Desktop" space
app_send_key.sh "Hulu Desktop" \"f\" "command down"
```

Sample XML command usage:

```

    <cmd name="pause_hulu">
        <label>Pause Hulu</label>
        <exec>app_send_key.sh</exec>
        <param>Hulu Desktop</param>
        <param>space</param>
        <icon>hulu.png</icon>
        <badge>pause-red.png</badge>
    </cmd>

    <cmd name="toggle_fs_hulu">
        <label>Hulu FS Toggle</label>
        <exec>app_send_key.sh</exec>
        <param>Hulu Desktop</param>
        <param>"f"</param>
        <param>command down</param>
        <icon>hulu.png</icon>
        <badge>square-red.png</badge>
    </cmd>
	
```

## tv\_power.sh ##

Example of a very specific script designed to turn on and off a Philips TV, using ribsu and the USB-UIRT device.  It just sends a recorded IR sequence to the TV.

```
#!/bin/bash
/bin/echo "0000 0074 0000 0015 005F 0020 0010 0020 0010 0010 0010 \
0010 0010 0020 0020 0010 0010 0010 0010 0010 0010 0010 0010 0010 \
0010 0010 0010 0010 0010 0010 0010 0010 0010 0010 0010 0010 0010 \
0010 0020 0010 0010 0020 0010 0010 0010 0BAB" | /usr/local/bin/ribsu
```

A possible command entry in cmds.xml looks like this:
```
    <cmd name="tv_power">
           <label>TV Power</label>
            <exec>tv_power.sh</exec>
            <icon>tv.png</icon>
            <badge>power-red.png</badge>
    </cmd>
```