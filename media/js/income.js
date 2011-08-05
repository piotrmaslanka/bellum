
var miniobj = new Object();

function minimax(planet_id)
{
    if (miniobj['p'+planet_id] == null) /* this object is maximized */
    {
        var i = 0;
        while (true)
        {
            var dc = document.getElementById('pi'+planet_id+'i'+i);
            if (dc == null) break;
            dc.style.display = 'none';
            i++;
        }
        miniobj['p'+planet_id] = true;
        document.getElementById('mb'+planet_id).src = '/media/gfx/income/maximize.png';
    } else
    {
        var i = 0;
        while (true)
        {
            var dc = document.getElementById('pi'+planet_id+'i'+i);
            if (dc == null) break;
            dc.style.display = 'table-row';
            i++;
        }
        miniobj['p'+planet_id] = null;
        document.getElementById('mb'+planet_id).src = '/media/gfx/income/minimize.png';
    }
}