<?php
/*
This is the file to customize, adding your own commands, scripts and icons.

Each line of code below defines a command set:

CMD_NAME:    A unique command name

CMD_LABEL:   The label for the command shown below the icon

CMD_SCRIPT:  The script to run on the server (path can be anywhere in the host system).  
            Permissions are a tricky subject. I have my webserver set up to run as the primary user,
			and in certain scripts I preface some commands with "sudo -u {username}"  Use 
			caution if exposing this web app on the internet!!  

CMD_ICON:    The icon to display. A good site to check out for making nice iPhone-y icons is:
             http://www.quirco.com/iPhoneIcon/

CMD_CONFIRM: True if a confirmation dialog is needed

Since the buttons are layed out in lines of 4, they are grouped here that way for
clarity's sake.  Please note the use of the special reserved command, "blank", used
as a space filler on the grid.

*/

// You will most likely need to change this!
$scripts_dir="/Applications/xampp/htdocs/buttonboard/scripts/";


define(CMD_NAME,0);    
define(CMD_LABEL,1);  
define(CMD_SCRIPT,2); 
define(CMD_ICON,3);   
define(CMD_CONFIRM,4); 

$cmd_list = array( 
#----		
	array( "tv_power",        "TV Power",      $scripts_dir."tv_power.sh",          "images/tv_power.png", "false"),
	array( "stereo_power",    "Stereo Power",  $scripts_dir."stereo_power.sh",      "images/stereo_power.png", "false"),
	array( "blank"),
	array( "stereo_vol_up",   "Vol +",         $scripts_dir."stereo_vol_up.sh",     "images/vol_up.png", "false"),
#----		
	array( "blank"),
	array( "blank"),
	array( "blank"),
	array( "stereo_vol_down",  "Vol -",         $scripts_dir."stereo_vol_down.sh",    "images/vol_down.png", "false"),
#----		
	array( "update_comix",     "Update Comics", $scripts_dir."update_comics_dropbox.sh", "images/update_comix.png", "false"),
	array( "rescan_plex",      "Rescan Plex",   $scripts_dir."rescan_plex.sh",        "images/pms.png", "true"),
	array( "show_hide_plex",   "Show/Hide Plex",$scripts_dir."show_hide_app.sh Plex", "images/show_hide_plex.png", "false"),
	array( "blank"),
#----		
	array( "restart_plex",     "Restart Plex",  $scripts_dir."restart_app.sh Plex /Applications/Plex.app",                   "images/restart_plex.png", "true"),
	array( "restart_trans",    "Restart Transmission",  $scripts_dir."restart_app.sh Transmission /Applications/Transmission.app",                   "images/restart_transmission.png", "true"),
	
); 
?>
