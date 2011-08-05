function disband()
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4)
                    window.location = '/stats/empire/';
	}

        var url = "/alliance/disband/";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);   
}

function kick(membership_id)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4) location.reload(true);
	}

        var url = "/alliance/kick/"+membership_id+"/";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}

function toggle(membership_id, priv)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4)
                {
                    var dohl = xmlhttp.responseText;
                    if ((dohl != 1) && (dohl != 0)) location.reload(true);
                    if (priv == 1)  // teamsite
                    {
                        if (dohl == 1) document.getElementById('p_edit'+membership_id).src = '/media/gfx/alliance_memberlist/hl_edit.png';
                        if (dohl == 0) document.getElementById('p_edit'+membership_id).src = '/media/gfx/alliance_memberlist/edit.png';
                    }
                    if (priv == 2)  // privilege
                    {
                        if (dohl == 1) document.getElementById('p_rank'+membership_id).src = '/media/gfx/alliance_memberlist/hl_rank.png';
                        if (dohl == 0) document.getElementById('p_rank'+membership_id).src = '/media/gfx/alliance_memberlist/rank.png';
                    }
                    if (priv == 4)  // kick
                    {
                        if (dohl == 1) document.getElementById('p_kick'+membership_id).src = '/media/gfx/alliance_memberlist/hl_dis.png';
                        if (dohl == 0) document.getElementById('p_kick'+membership_id).src = '/media/gfx/alliance_memberlist/dis.png';
                    }
                    if (priv == 8)  // accept
                    {
                        if (dohl == 1) document.getElementById('p_acpt'+membership_id).src = '/media/gfx/alliance_memberlist/hl_acpt.png';
                        if (dohl == 0) document.getElementById('p_acpt'+membership_id).src = '/media/gfx/alliance_memberlist/acpt.png';
                    }
                    if (priv == 16)  // moderate
                    {
                        if (dohl == 1) document.getElementById('p_mod'+membership_id).src = '/media/gfx/alliance_memberlist/hl_mod.png';
                        if (dohl == 0) document.getElementById('p_mod'+membership_id).src = '/media/gfx/alliance_memberlist/mod.png';
                    }
                }
	}

        var url = "/alliance/privileges/"+membership_id+"/toggle/"+priv+"/";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}

function leave()
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4)
                    window.location = '/stats/empire/';
	}

        var url = "/alliance/leave/";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}

function cancel_application(alliance_id)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4)
                    window.location = '/alliance/view/'+alliance_id+'/';
	}

        var url = "/alliance/apply/cancel/";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}

function rank_modify(entry_id)
{
    var currentRank = document.getElementById('d_rank'+entry_id).innerHTML;

    var newRank = prompt("Nowa ranga", currentRank);


    var xmlhttp = getXmlHttp();
    xmlhttp.onreadystatechange=function()
    {
            if (xmlhttp.readyState==4)
                document.getElementById('d_rank'+entry_id).innerHTML = xmlhttp.responseText;
    }

    var url = "/alliance/privileges/"+entry_id+"/rank/?rank="+encodeURIComponent(newRank);
    xmlhttp.open("GET",url,true);
    xmlhttp.send(null);
}

function application_reject(appid)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4) location.reload(true);
	}

        var url = "/alliance/accept/decline/"+appid+"/";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}
function application_accept(appid)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4) location.reload(true);
	}

        var url = "/alliance/accept/approve/"+appid+"/";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}

function makeleader(entid)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4) location.reload(true);
	}

        var url = "/alliance/makeleader/"+entid+"/";
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}