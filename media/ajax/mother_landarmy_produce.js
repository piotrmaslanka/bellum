function produce(what)
{
    howmuch = parseInt(document.getElementById('make'+what).value);
    var f = function(xmlhttp)
    {
        if (xmlhttp.responseText=='OK')	location.reload();
        else if (xmlhttp.responseText=='COSTS') alert('Nie stać cię');
        else alert('Inny błąd');
    }
    ajaxToolkitGET("/mother/ajax/latools/?what="+what+"&amount="+howmuch, f);
}