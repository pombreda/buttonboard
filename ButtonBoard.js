//----------------------------------------
//Set up a request object to use to launch commands
var http_cmd = false;

if(navigator.appName == "Microsoft Internet Explorer") 
{
	http_cmd = new ActiveXObject("Microsoft.XMLHTTP");
} 
else 
{
	http_cmd = new XMLHttpRequest();
}

//----------------------------------------
//Run the command indicated by the caller

function run_cmd(cmd, conf) 
{
	if (conf != "true" || (conf == "true" && confirm("Are you sure?")))
	{
		document.getElementById('launcher_stat').style.display='block';
		document.getElementById('launcher_stat').innerHTML="<img src=\"images/loading.gif\" alt=\"Loading\"/> Processing";
		
		http_cmd.open("GET", "launcher.php?cmd="+cmd, true);
		http_cmd.onreadystatechange=function() 
			{
				if(http_cmd.readyState == 4) 
				{
					document.getElementById('launcher_stat').innerHTML =  ""; 
				}
			}
		http_cmd.send(null);
	}
}
//----------------------------------------------------------------