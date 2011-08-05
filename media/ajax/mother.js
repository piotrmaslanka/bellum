function renameMothership()
{
    var mname = document.getElementById('mothername_ib').value;
    if (mname=='') location.reload();

    var f = function(xmlhttp)
    {
        if (xmlhttp.responseText=='')
        {
                alert('Wystąpił błąd');
                location.reload();
        }
        else
            document.getElementById('mothername_holder').innerHTML = "<span class=\"kword\" id=\"mothername_value\">"+mname+"</span> <span onclick=\"startRenameMothership()\">[Zmień]</span>";
    }
    ajaxToolkitGET("/mother/ajax/namechange/?name="+encodeURIComponent(mname), f);
}

function startRenameMothership()
{
    var mname = document.getElementById('mothername_value').innerHTML;
    document.getElementById('mothername_holder').innerHTML = "<input type=\"text\" id=\"mothername_ib\" value=\""+mname+"\" onkeydown=\"if (event.keyCode==13) renameMothership();\">";
}