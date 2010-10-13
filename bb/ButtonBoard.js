//----------------------------------------
//Set up a request object to use to launch commands
var http_cmd = false;
http_cmd = new XMLHttpRequest();


function run_cmd(cmd, conf, output) 
{
	if (conf != "true" || (conf == "true" && confirm("Are you sure?")))
	{
		launcher_stat = document.getElementById('launcher_stat');
		launcher_stat.style.display='block';

		//Do the math to put the swirly circle in the middle of the screen
		scrollX = window.pageXOffset; //scrollX;
		scrollY = window.pageYOffset; //scrollY;
		winWidth = window.innerWidth;
		winHeight = window.innerHeight;
		elementHeight = launcher_stat.offsetHeight ;
		elementWidth =  launcher_stat.offsetWidth;
		
		myTop = (winHeight/2 + scrollY) - (elementHeight/2);
		myLeft = (winWidth/2 + scrollX) - (elementWidth/2);
	
		launcher_stat.style.pixelTop = myTop;
		launcher_stat.style.pixelLeft = myLeft;
        launcher_stat.style.top = myTop+"px";  //for mozilla
        launcher_stat.style.left = myLeft+"px";  //for mozilla
		launcher_stat.innerHTML="<img src=\"images/loading2.gif\" alt=\"Loading\"/>";
				
		try
		{
			if (navigator.appName == "Microsoft Internet Explorer") 
			{
				//add a random (more or less) string to prevent the over-agressive caching of IE
				http_cmd.open("GET", "/cmd/"+cmd+"?foo="+new Date().getTime(), true);
			}
			else
			{
				http_cmd.open("GET", "/cmd/"+cmd, true);
			}
		}
		catch (err)
		{
			alert("ERROR: " + err.description);
		}
		http_cmd.onreadystatechange=function() 
			{
				if(http_cmd.readyState == 4) 
				{
					launcher_stat.style.display='none';
					if (http_cmd.status != 200)
					{
						alert("Could not run command.  Remote server may be down.");
					}
					else
					{
						// parse out buttonboard status header
						items = http_cmd.responseText.split("::", 2);
						if (output == "true" || items[0] == "Fail")
						{
							alert(items[1]);
						}
						else if (items[0] != "Done")
						{
							//something went wrong.  do we need to login again?
							//See if we got the Login Page
							if (http_cmd.responseText.indexOf("<title>ButtonBoard Login</title>")!=-1)
							{	
								//Got it.  Redirect to show login page
								window.location = '/login'
							}
							else
							{
								alert("Something has gone wrong.  Clear your cache and check your password!");
							}
						}
					}
					
				}
			}
		http_cmd.send(null);
	}
}

