#!/bin/bash

name_to_kill=$1
name_to_start=$2

if [ "$2" = "" ]
then
	name_to_start=$1
fi

killall -9 $name_to_kill
sleep 2
osascript -e "tell application \"$name_to_start\" to open"
osascript -e "tell application \"$name_to_start\" to activate"

