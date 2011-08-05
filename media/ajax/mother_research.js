function startResearchTechnology(id, callback)
{
    var f = function(xmlhttp)
    {
        if (callback == null) location.reload();
        else callback();
    }
    ajaxToolkitGET("/mother/ajax/ttools/order/?what="+id, f);
}
function cancelResearchTechnology(id, callback)
{
    var f = function(xmlhttp)
    {
        if (callback == null) location.reload();
        else callback();
    }
    ajaxToolkitGET("/mother/ajax/ttools/cancel/?what="+id, f);
}