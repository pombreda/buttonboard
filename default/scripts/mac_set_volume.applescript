#!/usr/bin/osascript


on run argv

	if  item 1 of argv = "up" then
		vol_up()	
	else if  item 1 of argv = "down" then
		vol_down()	
	else if  item 1 of argv = "mute" then
		vol_mute()
	end if
	
end run
------------------------------------------
on vol_up()
	
	set current_volume to output volume of (get volume settings)
	
	if current_volume is less than 100 then
		set current_volume to current_volume + 10
	end if
	
	set volume output volume current_volume
	
end vol_up

------------------------------------------
on vol_down()
	
	set current_volume to output volume of (get volume settings)
	
	if current_volume is greater than 0 then
		set current_volume to current_volume - 10
	end if
	
	set volume output volume current_volume
	
end vol_down

------------------------------------------
on vol_mute()
	
	set isMuted to output muted of (get volume settings)
	-- invert it
	set newMuted to not isMuted
	-- and set it back
	set volume output muted newMuted
	
end vol_mute

