function gmbHighlight(image)
{
    var tab = image.src.split("/");

    var relem = tab[tab.length-1];
    if (relem.substr(0, 3) == 'hl_') return;

    tab[tab.length-1] = 'hl_' + relem;
    image.src = tab.join("/");
}
function gmbUnhighlight(image)
{
    var tab = image.src.split("/");

    var relem = tab[tab.length-1];
    if (relem.substr(0, 3) != 'hl_') return;

    tab[tab.length-1] = relem.substr(3);
    image.src = tab.join("/");
}
