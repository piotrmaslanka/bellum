var currentlySpeakingTo = 0;
var chatcache = [];                 /* entries list(account_ID, account_EMPIRE) */
var chatO_open = false;
var chatX_open = false;
var msg_id = false;     /* currently opened message */
var isRelaying = false;

function _create_namedDiv(name)
{
    var div = document.createElement('div');
    div.setAttribute('id', name);
    return div;
}

function _teardown(what) {      // 0 - global chat hierarcyh
                                // 1 - just chat_X
                                // 2 - chat_C
    if (what==0) var cell = document.getElementById('chat_fixroot');
    if (what==1) var cell = document.getElementById('chat_X');
    if (what==2) var cell = document.getElementById('chat_C');
    if ( cell.hasChildNodes() )
        while ( cell.childNodes.length >= 1 )
            cell.removeChild( cell.firstChild );
    if (what == 0) document.body.removeChild(cell);
    if (what == 1) document.getElementById('chat_fixrootf').removeChild(cell);
    if (what == 2) document.body.removeChild(cell);
}

function _setup_fixroot()
{
    var chat_fixroot = _create_namedDiv('chat_fixroot');
    var chat_fixrootm = _create_namedDiv('chat_fixrootm');
    var chat_fixrootf = _create_namedDiv('chat_fixrootf');   
    chat_fixrootm.appendChild(chat_fixrootf);
    chat_fixroot.appendChild(chat_fixrootm);
    document.body.appendChild(chat_fixroot);
    return chat_fixrootf;
}

function _chat_open_chatO() {
    if (chatO_open) _teardown(0);
    var chat_O = _create_namedDiv('chat_O');
    _setup_fixroot().appendChild(chat_O);
    chatO_open = true;
    document.global_allowReload = false;
    return chat_O;
}

function _show_chatO() { document.getElementById('chat_O').style.display = 'block'; }
function _hide_chatO() { document.getElementById('chat_O').style.display = 'none'; }

function _chat_close_chatO() {
    _teardown(0);
    chatO_open = false;
    document.global_allowReload = true;
    if (document.global_requireReload) location.reload();
}

function _chat_close_chatX()
{
   _teardown(1);
   chatX_open = false;
   if (chatO_open) _show_chatO();
   else {
        _teardown(0);
        document.global_allowReload = true;
        if (document.global_requireReload) location.reload();
   }
}

function _chat_open_chatX() {
    if (chatX_open)
        if (chatO_open) _teardown(1);
        else _teardown(0);

    var chatX = _create_namedDiv('chat_X');
    if (!chatO_open) _setup_fixroot().appendChild(chatX);
    else { _hide_chatO(); document.getElementById('chat_fixrootf').appendChild(chatX); }
    chatX_open = true;
    document.global_allowReload = false;
    return chatX;
}

function chat_relay() { /* get info from select box */
    if (isRelaying) return;
    var target_user = document.getElementById('relay_to').value;
    var f = function(xmlhttp) {
        alert('Poszło!');
        isRelaying = false;
    }
    ajaxToolkitGET("/chat/relay/"+msg_id+"/"+target_user+"/", f);
    isRelaying = false;
}

function chat_open_msg(msgid) {
    var f = function(xmlhttp)
    {
        var msgs = eval(xmlhttp.responseText);
        msg_id = msgs[0];
        var msg_type = msgs[1];
        var msg = msgs[2];
        if (msg_type == 0)              // PRIVATE MESSAGE
        {
            var acc_id = msgs[3];
            var acc_empire = msgs[4];
            currentlySpeakingTo = acc_id;
            var chatO = _chat_open_chatO();
            var chats = '<div class="pl"></div><div class="pr"></div>';
            chats += '<div class="chat_O_row"><div class="pl"></div><div class="pr"></div><div class="pinleft">Rozmawiasz z <a href="/uprofile/view/'+acc_id+'/">'+acc_empire+'</a></div><div class="pinright"><a class="button" href="javascript:_chat_close_chatO()">ZAMKNIJ</a></div></div>';
            chats += '<div id="chat_O_msg">'+msg+'</div>';
            chats += '<textarea id="chat_O_txta" rows="6"></textarea>';
            chats += '<div class="clear"></div>';
            chats += '<div class="chat_O_row"><div class="pl"></div><div class="pr"></div><div class="pinleft"><a class="button" href="javascript:chat_open_archive('+acc_id+')">ARCHIWUM</a></div><div class="pinright"><a class="button" href="javascript:chat_submit()">WYŚLIJ</a></div></div>';
            chatO.innerHTML = chats;
        }
        else               // REPORT
        {
            var title = msgs[3];
            var wasRelayed = msgs[4];
            var chatX = _chat_open_chatX();
            var chats = '<div id="chat_XX">';
            chats += '<div class="pl"></div><div class="pr"></div>';
            chats += '<div class="chat_X_row"><div class="pl"></div><div class="pr"></div><div class="pinleft">'+title+'</div><div class="pinright"><a class="button" href="javascript:_chat_close_chatX()">ZAMKNIJ</a></div></div>';
            chats += '<div id="chat_X_row_b"><div class="chat_X_row"><div class="pl"></div><div class="pr"></div><div class="pinleft"><a class="button" href="javascript:chat_open_report_archive()">ARCHIWUM</a></div></div></div>';
            chats += '<div id="chat_X_txt">';
            if (wasRelayed) chats += 'Przekazane od: <a href="/uprofile/view/'+msgs[5]+'/">'+msgs[6]+'</a><br>';
            chats += msg;
            chatX.innerHTML = chats + '</div></div>';           
        }
    }
    ajaxToolkitGET('/chat/retr/'+msgid+'/', f);
}

function chat_open_report_archive()
{
    var f = function(xmlhttp) {
        var msgs = eval(xmlhttp.responseText);
        var chatX = _chat_open_chatX();
        var chats = '<div id="chat_XX">';
        chats += '<div class="pl"></div><div class="pr"></div>';
        chats += '<div class="chat_X_row"><div class="pl"></div><div class="pr"></div><div class="pinleft">RAPORTY</div><div class="pinright"><a class="button" href="javascript:_chat_close_chatX()">ZAMKNIJ</a></div></div>';
        chats += '<div id="chat_X_row_b"><div class="chat_X_row"><div class="pl"></div><div class="pr"></div></div></div>';
        chats += '<div id="chat_X_txt">';
        for (key in msgs) {
            var msg = msgs[key];
            var msg_id = msg[0];
            var msg_title = msg[1];
            var sent_on = msg[2];
            var relayed = msg[3];
            chats += '<span class="c_when">'+sent_on+'</span>';
            if (relayed) chats += 'Przekazane od <a href="/uprofile/view/'+msg[4]+'/">'+msg[5]+'</a><br>';
            chats += '<a href="javascript:chat_open_msg('+msg_id+')">'+msg_title+'</a>';
            chats += '<div class="clear"></div>'
        }
        chatX.innerHTML = chats + '</div></div>';
    }
    ajaxToolkitGET("/chat/convr/", f);
}

function chat_open_archive(aid) {
    var f = function(xmlhttp) {
        var msgs = eval(xmlhttp.responseText);
        var empire = msgs[0];
        msgs = msgs[1];         /* proper list of messages */

        var chatX = _chat_open_chatX();
        var chats = '<div id="chat_XX">';
        chats += '<div class="pl"></div><div class="pr"></div>';
        chats += '<div class="chat_X_row"><div class="pl"></div><div class="pr"></div><div class="pinleft">ARCHIWUM</div><div class="pinright"><a class="button" href="javascript:_chat_close_chatX()">ZAMKNIJ</a></div></div>';
        chats += '<div id="chat_X_row_b"><div class="chat_X_row"><div class="pl"></div><div class="pr"></div></div></div>';
        chats += '<div id="chat_X_txt">';
        for (key in msgs)
        {
            var msg = msgs[key];
            if (msg[0]) chats += '<div class="c_mine">';
            else chats += '<div class="c_others">';
            chats += '<span class="c_when">'+msg[2]+'</span>';
            chats += '<div class="clear"></div>'
            chats += msg[1];
            chats += '</div>'
            
        }
        chatX.innerHTML = chats + '</div></div>';
    }
    ajaxToolkitGET('/chat/convp/'+aid+'/', f);
}

function chat_refresh_P()           /* called periodically to refresh chat bar at the bottom */
{
        var f = function(xmlhttp) {
            var msgs = eval(xmlhttp.responseText);
            chatcache = msgs[1];
            msgs = msgs[0];
            var divt = '';
            for (key in msgs)
            {
                var msg_id = msgs[key][0];
                var msgtype = msgs[key][1];
                                
                if (msgtype == 0) {  // private message
                    var accid = msgs[key][2];
                    var empire = msgs[key][3];
                    divt += '<div id="chat_PCE_'+msg_id+'" class="chat_PCE chat_PCE_privmsg" onclick="chat_open_msg('+msg_id+')">'+empire+'</div>';
                }
                if (msgtype == 1) {  // unsolicited response
                    divt += '<div id="chat_PCE_'+msg_id+'" class="chat_PCE chat_PCE_ur" onclick="chat_open_msg('+msg_id+')">RAPORT</div>';
                }
                if (msgtype == 2) {  // solicited response
                    divt += '<div id="chat_PCE_'+msg_id+'" class="chat_PCE chat_PCE_sr" onclick="chat_open_msg('+msg_id+')">RAPORT</div>';
                }

            }
            document.getElementById('chat_PC').innerHTML = divt;
            setTimeout("chat_refresh_P()", 5000);
        }
        ajaxToolkitGET('/chat/query/', f);
}

function chat_submit()
{
    var xmlhttp = getXmlHttp();
    var url = "/chat/push/";
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xmlhttp.onreadystatechange=function() {
            if (xmlhttp.readyState==4) _chat_close_chatO();
    }

    var params = "content="+encodeURIComponent(document.getElementById('chat_O_txta').value);
    params += "&target="+currentlySpeakingTo;
    xmlhttp.send(params);
}

function chat_opensend(id, empire)  // opens a chat message directly to an user by his ID/empire
{
    currentlySpeakingTo = id;
    var chatO = _chat_open_chatO();
    var chats = '<div class="pl"></div><div class="pr"></div>';
    chats += '<div class="chat_O_row"><div class="pl"></div><div class="pr"></div><div class="pinleft">Rozmawiasz z <a href="/uprofile/view/'+id+'/">'+empire+'</a></div><div class="pinright"><a class="button" href="javascript:_chat_close_chatO()">ZAMKNIJ</a></div></div>';
    chats += '<textarea id="chat_O_txta" rows="6"></textarea>';
    chats += '<div class="clear"></div>';
    chats += '<div class="chat_O_row"><div class="pl"></div><div class="pr"></div><div class="pinleft"><a class="button" href="javascript:chat_open_archive('+id+')">ARCHIWUM</a></div><div class="pinright"><a class="button" href="javascript:chat_submit()">WYŚLIJ</a></div></div>';
    chatO.innerHTML = chats;
}

function chat_opensend_inputbox()   // opens a chat message by data from inputbox
{
    var f = function(xmlhttp)
    {
        var res = eval(xmlhttp.responseText);
        if (res == null) {
            alert('Taki gracz nie istnieje!');
            return;
        }
        chat_opensend(res[0], res[1]);
    }
    ajaxToolkitGET("/chat/getid/?empire="+encodeURIComponent(document.getElementById('chat_openchannel_box').value), f);
}

function chat_open_cache() {}
function chat_close_cache() {}