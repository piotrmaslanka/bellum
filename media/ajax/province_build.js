function startBuildProvince(pid,slot, callback)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4) 
		{
			if (callback == null) location.reload(true);
                        else callback();
		}
	}
	
	var url="/province/ajax/btools/order/?slot="+slot+"&pp="+pid;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);		
}
function startErectProvince(pid,what, callback)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4)
		{
			if (callback == null) location.reload(true);
                        else callback();
		}
	}

	var url="/province/ajax/btools/erect/?what="+what+"&pp="+pid;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}

function cancelBuildProvince(pid, slot, callback)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4) 
		{
                        if (callback == null) location.reload(true);
                        else callback();
		}
	}
	
	var url="/province/ajax/btools/cancel/?slot="+slot+"&pp="+pid;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);		
}
