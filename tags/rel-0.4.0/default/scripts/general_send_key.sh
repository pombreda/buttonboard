#!/bin/bash

#Takes up to 2 args:
# key to send
# optional "using" 

if [ "$2" != "" ]
then
	USING="using ($2)"
else
	USING=""
fi

/usr/bin/osascript <<EOF

tell application "System Events" to keystroke $1 $USING

