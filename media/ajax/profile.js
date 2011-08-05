function send_resource()
{
    var tit = document.getElementById('titan').value;
    var plu = document.getElementById('pluton').value;
    var men = document.getElementById('men').value;

	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4) location.reload();
	}

        var url = "/mother/ajax/sendres/?titan="+tit+"&pluton="+plu+"&men="+men+"&target="+currentlyViewing;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}
