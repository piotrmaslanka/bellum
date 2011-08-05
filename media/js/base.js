function startUpdatingResource() {
    g_glbl_titan += g_glbl_ratio_titan * 4;
    g_glbl_pluton += g_glbl_ratio_pluton * 4;
    g_glbl_men += g_glbl_ratio_men * 4;
    document.getElementById('resources_titan').innerHTML = Math.round(g_glbl_titan);
    document.getElementById('resources_pluton').innerHTML = Math.round(g_glbl_pluton);
    document.getElementById('resources_men').innerHTML = Math.round(g_glbl_men);
    setTimeout("startUpdatingResource()", 4000);
}
function resourceDeduct(titan, pluton, manpower) {
    g_glbl_titan -= titan;
    g_glbl_pluton -= pluton;
    g_glbl_men -= manpower;
    document.getElementById('resources_titan').innerHTML = Math.round(g_glbl_titan);
    document.getElementById('resources_pluton').innerHTML = Math.round(g_glbl_pluton);
    document.getElementById('resources_men').innerHTML = Math.round(g_glbl_men);
}