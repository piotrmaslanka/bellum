// graphics options
function go_unselect_provinces()
{
    var i = 0;
    while (true)
    {
        img = document.getElementById('psimg'+i);
        if (img==null) break;
        ssrc = img.src;
        ssrc = ssrc.replace(/h.png/, '.png');
        img.src = ssrc;
        i++;
    }
}
function go_select_province(i)
{
    go_unselect_provinces();
    var img = document.getElementById('psimg'+i);
    var ssrc = img.src;
    ssrc = ssrc.replace(/.png/, 'h.png');
    img.src = ssrc;
}

function go_unborderify()
{
    var tds = document.getElementsByTagName('td');
    document.getElementById('j_mothership').style.border = 'none';
    for (i in tds) if (tds[i].className == 'pll_list_entry') tds[i].style.border = 'none';
}
function go_borderify_planet(plid)
{
    go_unborderify();
    document.getElementById('j_pla_p'+plid).style.border = '1px solid rgb(124, 124, 124)';
}
function go_borderify_mothership()
{
    go_unborderify();
    document.getElementById('j_mothership').style.border = '1px solid rgb(124, 124, 124)';
}
// click-response stuff
function cr_pla_ms_selected()
{
//    if (g_selected_province == null) return;    /* ms already selected */
    var f = function(xmlhttp) {
        var resp = eval(xmlhttp.responseText);
        document.getElementById('pla_map').innerHTML = resp[0];
        document.getElementById('garrison').innerHTML = resp[1];
        document.getElementById('commands').innerHTML = resp[2];

        g_current_planet_id = resp[3];
        g_selected_province = null;
        go_borderify_mothership();
    }
    ajaxToolkitGET("/space/ajax/tdinfo/planetpick/mothership/", f);
}

function cr_pla_planet_selected(pid)
{
    var f = function(xmlhttp)
    {
        var resp = eval(xmlhttp.responseText);
        if (resp == null) return;    /* script returned error */
        document.getElementById('pla_map').innerHTML = resp[0];
        document.getElementById('garrison').innerHTML = resp[1];
        document.getElementById('commands').innerHTML = resp[2];

        g_current_planet_id = resp[3];
        g_selected_province = resp[4];
        go_borderify_planet(pid);
    }
    ajaxToolkitGET("/space/ajax/tdinfo/planetpick/"+pid+"/", f);
}

function cr_province_selected(provid)
{
    var f = function(xmlhttp) {
        var resp = eval(xmlhttp.responseText);
        if (resp == null) return;    /* script returned error */
        document.getElementById('garrison').innerHTML = resp[0];
        document.getElementById('commands').innerHTML = resp[1];

        g_selected_province = provid;
        go_select_province(resp[2]);
    }
    ajaxToolkitGET("/space/ajax/tdinfo/provincepick/?p="+provid, f);
}
function cr_setall(max)
{
    /* if max = true, set all to max. Else set all to zero */
    var inps = document.getElementsByTagName('input');
    for(var i=0; i<inps.length; i++)
            if (inps[i].id.match(/^box_st\d+$/))   // starts with box_st, and latter part is a number, after a number there's nothing
            {
                if (max) inps[i].value = inps[i].getAttribute('max');
                else inps[i].value = 0;
            }
}
function cr_submit()
{
    if (!g_can_press_launch) return;
    var f = function(xmlhttp) {
        var rt = xmlhttp.responseText;
        if (rt == 'OK')
        {
            if (g_selected_province == null) window.location = '/space/troopmove/mother/';
            else window.location = '/space/troopmove/'+g_selected_province+'/';
        } else g_can_press_launch = true;
        if (rt == 'ZERO') alert('Pusty oddział!');
        if (rt == 'HQNT') alert('HQ nie nad planetą!');
        if (rt == 'RELOC') alert('Trwa relokacja HQ!');
    }

    var request_string = "";
    /* designation */
    request_string += "?designation="+g_current_designation;
    /* process garrison */
    var inps = document.getElementsByTagName('input');
    for(var i=0; i<inps.length; i++)
        if (inps[i].id.match(/^box_st\d+$/))   // starts with box_st, and latter part is a number, after a number there's nothing
            request_string += "&"+inps[i].name+"="+inps[i].value;

    /* source province */
    // g_selected_province - if null, we are striking from mother.
    var s_target = document.getElementById('j_target').value;
    request_string += "&target="+(s_target == 'mothership' ? null : s_target);
    /* source
     * if mothership, None, else province id */
    request_string += "&source="+g_selected_province;
    ajaxToolkitGET("/space/troopmove/submit/"+request_string, f);
    g_can_press_launch = false; /* lock the button after pressing to avoid dumb situations where you send sth twice */
}
function cr_select_designation(dsid)
{
    /* 0 - attack, 1 - reinforce/attak, 2 - reinforce/fallback */
    g_current_designation = dsid;

    gmbUnhighlight(document.getElementById('j_des_0'));
    gmbUnhighlight(document.getElementById('j_des_1'));
    gmbUnhighlight(document.getElementById('j_des_2'));
    gmbHighlight(document.getElementById('j_des_'+dsid));
}