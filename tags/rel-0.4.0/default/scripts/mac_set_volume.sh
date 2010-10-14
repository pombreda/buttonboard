#!/bin/bash

#----------------------------------------------
function vol_up()
{
	/usr/bin/osascript <<EOAS1

	set current_volume to output volume of (get volume settings)
	
	if current_volume is less than 100 then
		set current_volume to current_volume + 10
	end if
	
	set volume output volume current_volume
EOAS1
}

#----------------------------------------------
function vol_down()
{
	/usr/bin/osascript <<EOAS2

	set current_volume to output volume of (get volume settings)
	
	if current_volume is greater than 0 then
		set current_volume to current_volume - 10
	end if
	
	set volume output volume current_volume
EOAS2
}
#----------------------------------------------
function vol_mute()
{
	/usr/bin/osascript <<EOAS3

	set isMuted to output muted of (get volume settings)
	-- invert it
	set newMuted to not isMuted
	-- and set it back
	set volume output muted newMuted
EOAS3
}
#----------------------------------------------

if [ "$1" == "up" ]
then
	vol_up	
elif [ "$1" == "down" ]
then
	vol_down	
elif [ "$1" == "mute" ]
then
	vol_mute
fi
