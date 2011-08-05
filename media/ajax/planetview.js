function reload_province() {
    switch_province(currentProvinceId, currentPcId, true);
}

function cancel_drop(dropid) {
    ajaxToolkitGET("/space/troopmove/cancel/drop/?id="+dropid, reload_province);
}

function cancel_strike(strid) {
    ajaxToolkitGET("/space/troopmove/cancel/strike/?id="+strid, reload_province);
}


function switch_province(number, pcid, keep_highlight)  // number being province ID, pcid being planet_count_number
{
    var f = function(xmlhttp) {
        if (xmlhttp.responseText.length > 20)   // oh, c'mon
        {
            // set text, execute JS
            document.getElementById('province_specific_contents').innerHTML = xmlhttp.responseText;
            var x = document.getElementById('province_specific_contents').getElementsByTagName('script');
            for(var i=0; i<x.length; i++) eval(x[i].text);
            if (keep_highlight == null)
            {
                // change highlight
                i = 0;
                while (true)
                {
                    img = document.getElementById('psimg'+i);
                    if (img==null) break;
                    ssrc = img.src;
                    if (pcid != i) ssrc = ssrc.replace(/h.png/, '.png');
                    if (pcid == i) ssrc = ssrc.replace(/.png/, 'h.png');
                    img.src = ssrc;
                    i++;
                }
            }
            currentPcId = pcid;
            currentProvinceId = number;
        }
    }
    ajaxToolkitGET("/space/ajax/pinfo/html/?p="+number, f);
}

function planetview_cancelBuildProvince(pv, pid, slot)  // pid is provintional presence id, pv is province id
{
    cancelBuildProvince(pid, slot, function() { switch_province(pv, null, true); });
    tooltip.hide();
}
function planetview_startBuildProvince(pv, pid, slot)
{
    startBuildProvince(pid, slot, function() { switch_province(pv, null, true); });
    tooltip.hide();
}
function planetview_startErectProvince(pv, pid, what)
{
    startErectProvince(pid, what, function() { switch_province(pv, null, true); });
    tooltip.hide();
}
function relocate(pid)
{
	var xmlhttp = getXmlHttp();
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4)
		{
                    if (xmlhttp.responseText == 'OK')
                        document.getElementById('nrpos').removeChild(document.getElementById('reloc_button'));
		}
	}
	var url="/mother/ajax/relocate/?p="+pid;
	xmlhttp.open("GET",url,true);
	xmlhttp.send(null);
}