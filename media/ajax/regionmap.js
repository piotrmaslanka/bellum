function unhighlightAll() {
    gmbUnhighlight(document.getElementById('mrks'));
    gmbUnhighlight(document.getElementById('mrkr'));
    gmbUnhighlight(document.getElementById('mrkg'));
}
function highlightSector() {
    unhighlightAll();
    gmbHighlight(document.getElementById('mrks'));
}
function highlightRegion() {
    unhighlightAll();
    gmbHighlight(document.getElementById('mrkr'));
}
function highlightGalaxy() {
    unhighlightAll();
    gmbHighlight(document.getElementById('mrkg'));
}

function maped_s()
{
   var x = g_current_x;
   var y = g_current_y;
   var f = function(xmlhttp) {
        document.getElementById('map_content').innerHTML = xmlhttp.responseText;
        document.getElementById('coords').style.display = 'block';
        document.getElementById('x').innerHTML = g_current_x;
        document.getElementById('y').innerHTML = g_current_y;
        highlightSector();
   }
    ajaxToolkitGET("/space/ajax/regionmap/sector/?x="+x+"&y="+y, f);
}
function maped_r()
{
   var x = g_current_x;
   var y = g_current_y;
   var f = function(xmlhttp) {
        document.getElementById('map_content').innerHTML = xmlhttp.responseText;
        document.getElementById('coords').style.display = 'none';
        highlightRegion();
   }
   ajaxToolkitGET("/space/ajax/regionmap/region/?x="+x+"&y="+y, f);
}
function maped_g()
{
    var f = function(xmlhttp) {
        document.getElementById('map_content').innerHTML = xmlhttp.responseText;
        document.getElementById('coords').style.display = 'none';
        highlightGalaxy();
    }
    ajaxToolkitGET("/space/ajax/regionmap/galaxy/", f);
}

function math_regC_to_secC()
{
    g_current_x = g_current_x*20 - 500 + 10;
    g_current_y = g_current_y*20 - 500 + 10;
}
function math_secC_to_regC()
{
    g_current_x = Math.floor((g_current_x+500) / 20);
    g_current_y = Math.floor((g_current_y+500) / 20);
}

function cr_g_toRegion(gx, gy)
{
    g_current_x = gx * 5 + 2;
    g_current_y = gy * 5 + 2;
    g_current_mode = 'region';
    maped_r();
}

function cr_r_toSector(sx, sy)
{
    g_current_x = sx;
    g_current_y = sy;
    math_regC_to_secC();
    g_current_mode = 'sector';
    maped_s();
}

function cr_up() {
    if (g_current_mode == 'sector') { g_current_y--; maped_s(); }
    if (g_current_mode == 'region') { g_current_y--; maped_r(); }
}
function cr_down() {
    if (g_current_mode == 'sector') { g_current_y++; maped_s(); }
    if (g_current_mode == 'region') { g_current_y++; maped_r(); }
}
function cr_left() {
    if (g_current_mode == 'sector') { g_current_x--; maped_s(); }
    if (g_current_mode == 'region') { g_current_x--; maped_r(); }
}
function cr_right() {
    if (g_current_mode == 'sector') { g_current_x++; maped_s(); }
    if (g_current_mode == 'region') { g_current_x++; maped_r(); }
}
function cr_hq() {
    g_current_x = g_mothership_x;
    g_current_y = g_mothership_y;
    if (g_current_mode == 'sector') {
        maped_s();
    }
    if (g_current_mode == 'region') {
        math_secC_to_regC();
        maped_r();
    }
}
function cr_s() {
    if (g_current_mode == 'region') {
        math_regC_to_secC();
        g_current_mode = 'sector';
        maped_s();
    }
    if (g_current_mode == 'galaxy') {
        g_current_mode = 'sector';
        maped_s();
    }
}
function cr_r() {
    if (g_current_mode == 'sector') {
        math_secC_to_regC();
        g_current_mode = 'region';
        maped_r();
    }
    if (g_current_mode == 'galaxy') {
        math_secC_to_regC();
        g_current_mode = 'region';
        maped_r();
    }
}
function cr_g() {   /* during galaxy mode coordinates are brought down to sector */
    if (g_current_mode == 'sector') {
        maped_g();
        g_current_mode = 'galaxy';
    }
    if (g_current_mode == 'region') {
        maped_g();
        math_regC_to_secC();
        g_current_mode = 'galaxy';
    }
}