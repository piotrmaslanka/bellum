function checkUsernameAvailable()
{
	var username = document.getElementById('id_login').value;
	if (username=='')
	{
		alert('Pole puste!'); 
		return;
	}
	
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4)
		{
			if (xmlhttp.responseText == "Y") { alert('Dostępne'); }
			if (xmlhttp.responseText == "N") { alert('Niedostępne'); }
			if (xmlhttp.responseText == "?") { alert('Błąd wewnętrzny'); }
		}
	}
	
	var url="/register/ajax/username_available/?login="+username;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}