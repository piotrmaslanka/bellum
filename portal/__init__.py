from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session import getAccount
from bellum.common.session.mother import getCurrentMother
from django.http import HttpResponse
from mako.template import Template

def process(request, path):
    from bellum.portal.models import Page
    try:
        this = Page.objects.get(path=path)
    except:
        this = Page.objects.get(path=r'/')

    try:
        account = getAccount(request)
        mother = getCurrentMother(request)
    except:
        account = None
        mother = None

    # construct backway routing:
    br = []
    br_i = this
    try:
        while True:
            br.append(br_i)
            br_i = br_i.getParent()
    except:
        pass

    # construct alongside-peerlist:
    ap = []
    for i in br:
        ap.append(i.getPeers())

    # construct rendering tree:

    rt_p = zip(br, ap)      # rendering tree, proto

    # wait, does this element have children?
    try:
        if this.getChildren().count > 0:
            rt_p = [(None, this.getChildren())] + rt_p
    except:
        pass

    rtext = u''     # render outmost layer
    b_counter = len(rt_p)
    for elem, peers in rt_p:
        x = u''
        for peer in peers:
            if peer.path[:8] == u'special:':
                x += u'<h'+str(b_counter)+' onclick="window.location=\''+peer.path[8:]+'\'"'
            else:
                x += u'<h'+str(b_counter)+' onclick="window.location=\'/portal/'+peer.path+'\'"'
            if peer == elem:
                x += ' style="color: white"'
            x += u'>'+peer.title+'</h'+str(b_counter)+'>'
            if peer == elem:
                x += rtext
        rtext = '<div id="container_h'+str(b_counter)+'">'+x+'</div>'
        b_counter -= 1

    content = Template(this.content).render_unicode(this=this, account=account, mother=mother)
    css = Template(this.head).render_unicode(this=this, account=account, mother=mother)

    return render_to_response('portal.html', {'menu':rtext, 'content':content, 'head':css, 'this':this, 'account':account, 'mother':mother})