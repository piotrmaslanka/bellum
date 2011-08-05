# coding=UTF-8
from django.db import models
from bellum.register.models import Account
from bellum.stats.models import Report
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

LCDMT_PRIVATE = 0
LCDMT_UR = 1
LCDMT_SR = 2

LCDMT = ((LCDMT_PRIVATE, 'Private message'), (LCDMT_UR, 'Unsolicited report'), (LCDMT_SR, 'Solicited report'))

class PrivateMessage(models.Model):
    text = models.TextField()
    references = models.PositiveIntegerField()

    def link(self):
        self.references += 1
        self.save()

    def unlink(self):
        self.references -= 1
        if self.references == 0:
            self.delete()
        else:
            self.save()

class LCDMessage(models.Model):
    '''Lowest common denominator for all messagy-like objects'''
    recipient = models.ForeignKey(Account, related_name='lcdmessage_received')
    author = models.ForeignKey(Account, related_name='lcdmessage_sent', null=True)
    msgtype = models.PositiveSmallIntegerField(choices=LCDMT)
    senton = models.DateTimeField(default=datetime.now)
    readed = models.PositiveSmallIntegerField(default=0) # 0 - not readed, 1 - readed
    message_ref = models.PositiveIntegerField()
    relayed = models.ForeignKey(Account, null=True, default=None, related_name='relayers')


    def delete(self):
        self.mapRef().unlink()
        models.Model.delete(self)

    def mapRef(self):
        try:
            self.__msgcache
        except:
            if self.msgtype == LCDMT_PRIVATE:
                self.__msgcache = PrivateMessage.objects.get(id=self.message_ref)
            else:
                self.__msgcache = Report.objects.get(id=self.message_ref)
        return self.__msgcache