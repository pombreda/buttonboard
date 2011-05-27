#!/usr/bin/osascript

(*
"Play Random Album" for iTunes
originally written by Paul Withey
updated by Doug Adams
dougscripts@mac.com

v2.0 apr 14 '10
-- maintenance release
-- universal binary
-- will include un-track numbered tracks (sort of)
-- selects only a single disc from multi-disc albums

v1.0-1.5 aug 11 '02
-- initial release

Get more free AppleScripts and info on writing your own
at Doug's AppleScripts for iTunes
dougscripts.com

This program is free software released "as-is"; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

Get a copy of the GNU General Public License by writing to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

or visit http://www.gnu.org/copyleft/gpl.html

*)

-- if you like, you can change this:
property randomAlbumName : "Some Random Albums"

tell application "iTunes"
	set myMusicLibrary to (some playlist whose special kind is Music)
	if exists (some user playlist whose name is randomAlbumName) then
		delete every track of playlist randomAlbumName
	else
		make new playlist with properties {name:randomAlbumName, shuffle:false}
	end if
	set new_playlist to playlist randomAlbumName
	
	tell myMusicLibrary
		repeat 5 times
			set someTrack to some track
			set play_album to album of someTrack
			set disc_number to disc number of someTrack
			set total_album_tracks to tracks whose album is play_album and disc number is disc_number
			set spareTracks to {}
			repeat with n from 1 to length of total_album_tracks
				set chk to false
				repeat with a_track in total_album_tracks
					if track number of a_track is n then
						set chk to true
						try
							duplicate a_track to new_playlist
						end try
						exit repeat
					end if
				end repeat
				if chk is false then set end of spareTracks to a_track
				-- start playing after addition of first song
				try
					if n = 1 then play new_playlist
				end try
			end repeat
			if spareTracks is not {} then
				repeat with a_track in spareTracks
					duplicate a_track to new_playlist
				end repeat
			end if
		end repeat
	end tell
end tell
