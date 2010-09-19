<!DOCTYPE html>

<html>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;">
	<meta name="apple-mobile-web-app-capable" content="yes">
	<title>ButtonBoard</title>
	<link rel="apple-touch-icon" href="images/button.jpg"/>
	<link rel="icon" href="images/button.jpg" />	
	<script language="javascript" type="text/javascript" src="ButtonBoard.js"></script>
	<link rel="stylesheet" type="text/css" href="ButtonBoard.css">

</head>

<body> 

<div class="ButtonBoardArea">

<table>

<?php
include 'cmds.php';

$buttons = array();
$labels = array();

# Build each table element of labels and buttons
foreach ($cmd_list as $cmd) 
{
	if ($cmd[CMD_NAME] == "blank")
	{
		$buttons[] = "\t<td><a href=\"#\"><img src=\"images/blank.png\" /></a></td>\n";
		$labels[] = "\t<td></td>\n";	
	}
	else
	{
		$buttons[] = "\t<td><a href=\"#\"><img src=\"".$cmd[CMD_ICON]."\" onclick=\"run_cmd('".$cmd[CMD_NAME]."','".$cmd[CMD_CONFIRM]."')\" /></a></td>\n";
		$labels[] = "\t<td>".$cmd[CMD_LABEL]."</td>\n";
	}
}

# Now lay them out in sets of 4
for($i = 0; $i < count($cmd_list); $i+=4)
{
	echo "<tr>\n";
	for($j = 0; $j < 4; $j++)
	{
		echo $buttons[$i+$j];
	}
	echo "</tr>\n";
	echo "<tr>\n";
	for($j = 0; $j < 4; $j++)
	{
		echo $labels[$i+$j];
	}
	echo "</tr>\n";
} 
?>

</table>
<div id="launcher_stat"></div>
</div>

</body>
</html>

