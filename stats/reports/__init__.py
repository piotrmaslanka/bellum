# coding=UTF-8
from time import time
from bellum.stats.models import Report

def makeReport(repdata, title):
    return Report.create(repdata, title)

def sendTo(report, account, solicited):
    '''Solicited defines whether the report was solicited or no. It affects presenting it in chat system'''
    from bellum.chat.models import LCDMessage, LCDMT_UR, LCDMT_SR
    sm = LCDMessage(recipient=account,
                    author=None,
                    msgtype={True:LCDMT_SR, False:LCDMT_UR}[solicited],
                    message_ref=report.id)
    sm.save()
    report.link()