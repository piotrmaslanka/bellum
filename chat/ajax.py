from djangomako.shortcuts import render_to_string
from bellum.common.session.login import must_be_logged_ajax
from bellum.common.session import getAccount, getRace
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from bellum.alliance.models import AllianceMembership
from bellum.register.models import Account
from json import dumps
from datetime import timedelta, datetime
from bellum.chat.models import LCDMessage, PrivateMessage, Report, LCDMT_PRIVATE, LCDMT_UR, LCDMT_SR
from bellum.chat import cacheContactEID, cacheContactAcc
from django.db.models import Q
from django.utils.html import escape
from bellum.stats.reports.codebase import WarfareReport, ScanReportv01, RadarReportv01

@must_be_logged_ajax
def query(request):
    '''Get list of unreaded messages'''

    acc = getAccount(request)

    msgs = LCDMessage.objects.filter(recipient=acc).filter(readed=0)

    tab = []
    for msg in msgs:
        if msg.msgtype == LCDMT_PRIVATE:
            tab.append((msg.id, LCDMT_PRIVATE, msg.author.id, msg.author.empire))
        elif msg.msgtype in (LCDMT_UR, LCDMT_SR):
            tab.append((msg.id, msg.msgtype))

    f = []
    for id, empire in request.session['ChatCache'].iteritems():
        f.append((id, empire))

    return HttpResponse(dumps((tab, f)))

def obtain_id(request):
    '''nickname passed by GET in empire. Autocache.'''
    try:
        acc = Account.objects.get(empire=request.GET['empire'])
    except:
        return HttpResponse(dumps(None))

    cacheContactAcc(request, acc)

    return HttpResponse(dumps((acc.id, acc.empire)))

def retr(request, pvmsg_id):        # retrieve a message/report
    acc = getAccount(request)

    try:
        pmsg = LCDMessage.objects.get(id=pvmsg_id)
    except ObjectDoesNotExist:
        return HttpResponse(dumps(None))

    if pmsg.recipient != acc: return HttpResponse('NOT YOURS HACKER')
    msg_cont = pmsg.mapRef()           # extract reference - a Report object in this case
    if pmsg.msgtype != LCDMT_PRIVATE:       # this is not a private message, this is a REPORT
        try:
            am = AllianceMembership.objects.get(account=getAccount(request))
        except:
            am = None
        
        if isinstance(msg_cont.data, WarfareReport):
            f = render_to_string('stats/reports/WarfareReport/report.html', {'r':msg_cont.data, 'membership':am})
        if isinstance(msg_cont.data, ScanReportv01):
            f = render_to_string('stats/reports/ScanReportv01/report.html', {'r':msg_cont.data, 'membership':am})
        if isinstance(msg_cont.data, RadarReportv01):
            f = render_to_string('stats/reports/RadarReportv01/report.html', {'r':msg_cont.data, 'membership':am})

        if pmsg.relayed != None:
            rp = (pmsg.id, pmsg.msgtype, f, msg_cont.title, True, pmsg.relayed.id, pmsg.relayed.empire)
        else:
            rp = (pmsg.id, pmsg.msgtype, f, msg_cont.title, False)

    else:           # this is a private message
        rp = (pmsg.id, pmsg.msgtype, escape(msg_cont.text).replace('\n', '<br>'), pmsg.author.id, pmsg.author.empire)
        cacheContactAcc(request, pmsg.author)

    if pmsg.readed == 0:
        pmsg.readed = 1
        pmsg.save()

    return HttpResponse(dumps(rp))

def push(request):          # send a private message to target player. Target's ID is in POST
    try:
        target = Account.objects.get(id=int(request.POST['target']))
    except:
        return HttpResponse(dumps(None))

    m = PrivateMessage(text=request.POST['content'], references=1)
    try:
        m.save()
    except:
        pass

    pm = LCDMessage(recipient=target, author=getAccount(request), msgtype=LCDMT_PRIVATE, message_ref=m.id)
    pm.save()

    cacheContactAcc(request, target)

    return HttpResponse(dumps(True))

def cache(request):
    accid = int(request.GET['accid'])
    empire = request.GET['empire']

    cacheContactEID(request, accid, empire)

    return HttpResponse('')

def convr(request):
    '''Long-term report library'''
    acc = getAccount(request)

    for dmsg in LCDMessage.objects.filter(recipient=acc).filter(senton__lt=datetime.now()-timedelta(14)):
        dmsg.delete()

    rmsgs = LCDMessage.objects.filter(recipient=acc).exclude(msgtype=LCDMT_PRIVATE).order_by('-senton')

    msga = []
    for rmsg in rmsgs:
        if rmsg.relayed == None:
            msga.append((rmsg.id, rmsg.mapRef().title, rmsg.senton.strftime('%H:%M %d.%m.%Y'), False))
        else:
            msga.append((rmsg.id, rmsg.mapRef().title, rmsg.senton.strftime('%H:%M %d.%m.%Y'), True, rmsg.relayed.id, rmsg.relayed.empire))
    return HttpResponse(dumps(msga))

def convp(request, acc_id):
    '''Long-term conversation with a Particular player'''
    acc = getAccount(request)
    try:
        target = Account.objects.get(id=acc_id)
    except:
        return HttpResponse(dumps(None))

    for dmsg in LCDMessage.objects.filter((Q(author=acc) & Q(recipient=target)) | (Q(author=target) & Q(recipient=acc))).filter(msgtype=LCDMT_PRIVATE).filter(senton__lt=datetime.now()-timedelta(14)):
        dmsg.delete()

    pmsgs = LCDMessage.objects.filter((Q(author=acc) & Q(recipient=target)) | (Q(author=target) & Q(recipient=acc))).filter(msgtype=LCDMT_PRIVATE).order_by('-senton')

    msga = []
    for msg in pmsgs:
        x = (msg.author != target, escape(msg.mapRef().text).replace('\n', '<br>'), msg.senton.strftime('%H:%M %d.%m.%Y'))
        msga.append(x)
    return HttpResponse(dumps((target.empire, msga)))


def relay(request, msg_id, acc_id):
    '''relay a message to specified account. Must be a report'''
    acc = getAccount(request)
    try:
        target = Account.objects.get(id=acc_id)
    except:
        return HttpResponse(dumps(None))

    try:
        rmsg = LCDMessage.objects.get(id=msg_id)
    except ObjectDoesNotExist:
        return HttpResponse(dumps(None))

    if rmsg.msgtype == LCDMT_PRIVATE: return HttpResponse(dumps(None))  # it's a private message

    rmsg.mapRef().link()

    newmsg = LCDMessage(recipient=target, author=rmsg.author, msgtype=rmsg.msgtype, \
                        senton=rmsg.senton, message_ref=rmsg.message_ref, relayed=acc)
    newmsg.save()
    return HttpResponse('OK')
    