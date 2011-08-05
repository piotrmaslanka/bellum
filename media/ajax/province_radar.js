/* radar and scanner */
function radar(pid)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4)
		{
                    alert('OK! Sprawdź skrzynkę odbiorczą!');
		}
	}

	var url="/province/ajax/radar?pp="+pid;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}


function scanner_unHighlight() {
    document.getElementById('scan_button').src = '/media/gfx/planetview/scan.png';
}

function scanner(pid)       /* target province id */
{
    ajaxToolkitGET('/province/ajax/scanner/?p='+pid, function(xmlhttp) {});
    document.getElementById('scan_button').src = '/media/gfx/planetview/hl_scan.gif';
    setTimeout('scanner_unHighlight()', 2500);
}