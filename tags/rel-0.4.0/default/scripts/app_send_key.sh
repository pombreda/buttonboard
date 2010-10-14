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

/usr/bin/osascript <<EOF

tell application "$1"
	activate
	tell application "System Events" to keystroke $2 $USING
end tell

