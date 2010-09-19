#!/bin/bash

/usr/bin/sudo -u username /usr/bin/osascript <<EOF

on run this_script
	set input_app to  "$1"
	tell application "System Events" to set app_name to name of the first process whose frontmost is true 
	if app_name is equal input_app then 
		tell application "System Events" to set visible of process input_app to false
	else 
		tell application "System Events" to set visible of process input_app to true
		tell application input_app to activate
	end if
end run
