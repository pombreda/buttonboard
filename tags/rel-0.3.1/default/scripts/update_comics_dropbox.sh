#!/bin/bash
touch /tmp/comics_update
ls -l /tmp/comics_update

ARCHIVE_TIME=10  #days

#Delete files older than Y days
find /Users/tony/Dropbox/comics -mtime +$ARCHIVE_TIME -name \*.cb[zr] -exec rm {} \;

#Copy in files newer than Y days
find /data/torrents/torrents/trans -mtime -$ARCHIVE_TIME -name \*.cb[zr] -exec cp -n -a {} /Users/tony/Dropbox/comics \;

#Delete leftover torrent .part files
find /data/torrents/torrents/trans -mtime +2 -name \*.part -exec rm {} \;

