 <?php 
# Accept a command code and if it is in the list, execute it on the server

include 'cmds.php';

$cmd = $_GET["cmd"] ;
if ($cmd != "")
{ 
	foreach ($cmd_list as $c) 
	{
		if ( $c[CMD_NAME] == $cmd )
		{
			echo exec($c[CMD_SCRIPT]);
			break;		
		}		
	}
}

?>

