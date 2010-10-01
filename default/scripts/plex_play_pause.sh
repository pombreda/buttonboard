#!/bin/bash
#curl localhost:3000/xbmcCmds/xbmcHttp?command=SendKey\(0xF10D\)
curl http://localhost:32400/system/players/$HOSTNAME/playback/play
