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
		launcher_stat.innerHTML="<img src=\"images/loading2.gif\" alt=\"Loading\"/>";
				
		try
		{
			http_cmd.open("GET", "/cmd/"+cmd, true);
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
					}
					
				}
			}
		http_cmd.send(null);
	}
}




var xmlhttp  = new XMLHttpRequest();

/*
//----------------------------------------------------------------
function parse_xml()
{
	if (xmlhttp.readyState == 4) 
	{
		//alert("Readystate:" + xmlhttp.readyState + "  xmlhttp.status =" + xmlhttp.status );
		
		//alert(typeof xmlhttp.responseXML)  ;
		if (xmlhttp.responseXML == null)
		{
			alert("No XML data :-( ");
		}
		else
		{
			xmlDoc=xmlhttp.responseXML ; 
			buttonrows=xmlDoc.getElementsByTagName("buttonrow");
			cmd_list=xmlDoc.getElementsByTagName("cmd");
			
			tableHTML = "<table>\n";
			//walk through the layout, find each command
			for (row =0 ; row < buttonrows.length; row++)
			{
				// go twice for each layout row
				for(part = 0; part < 2; part++)
				{
					tableHTML += "\t<tr>\n";
					rownode=buttonrows.item(row);
					for (i = 0; i < rownode.childNodes.length; i++)
					{
						thisnode = rownode.childNodes.item(i);

						if (thisnode.tagName == "item")
						{
							cmd_name = thisnode.attributes.getNamedItem("n").nodeValue;

							// find the command with this name
							found = false;
							var cmd_node;

							for ( c= 0; c < cmd_list.length; c++)
							{
								cmd_node = cmd_list.item(c);
								if (cmd_node.attributes.getNamedItem("name").nodeValue == cmd_name)
								{
									found = true;

									break;
								}
							}

							var elementHTML = "";
							if (found)
							{	
								if (part == 0)
								{								
									elementHTML += "<a href=\"#\"><img src=\"";
									elementHTML += cmd_node.getElementsByTagName("icon")[0].childNodes[0].nodeValue;
									elementHTML += "\" onclick=\"run_cmd('" ;
									elementHTML += cmd_name ;
									elementHTML += "','" ;
									elementHTML += cmd_node.getElementsByTagName("confirm")[0].childNodes[0].nodeValue ;
									elementHTML += "')\" /></a></td>\n" ;	
								}
								else
								{
									elementHTML += cmd_node.getElementsByTagName("label")[0].childNodes[0].nodeValue;
								}
							}
							
							tableHTML += "\t\t<td>" + elementHTML + "</td>\n";
						}
					}
					tableHTML += "\t</tr>\n";
				}
			}
			tableHTML += "</table>\n";
			
			document.getElementById('button_table').innerHTML = tableHTML;
		}
	}
}
//----------------------------------------
*/
function make_table() 
{
	xmlhttp.open("GET", "cmds.xml", true);
	xmlhttp.onreadystatechange=parse_xml;
	xmlhttp.send(null);
}


