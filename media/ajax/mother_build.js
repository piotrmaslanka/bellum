function startBuildMother(id)
{
    ajaxToolkitGET("/mother/ajax/btools/order/?what="+id, function(xmlhttp) { location.reload(); })
}
function cancelBuildMother(id)
{
    ajaxToolkitGET("/mother/ajax/btools/cancel/?what="+id, function(xmlhttp) { location.reload(); })
}