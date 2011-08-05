# coding=UTF-8
from django.db import models
from django import forms
from datetime import datetime

class Page(models.Model):
    '''A portal page'''
    title = models.CharField(max_length=80)
    path = models.TextField()
    content = models.TextField()
    head = models.TextField()

    ordering = models.IntegerField()
    menugroup = models.IntegerField()
    parent_for = models.IntegerField()      # specifies menugroup which this page is a parent for

    def getParent(self):
        if self.menugroup == 0:
            raise Exception, 'Root has no parent'
        return Page.objects.get(parent_for=self.menugroup)

    def getPeers(self):
        return Page.objects.filter(menugroup=self.menugroup).order_by('ordering')

    def getChildren(self):
        if self.parent_for == 0:
            return ()
        return Page.objects.filter(menugroup=self.parent_for).order_by('ordering')

    @staticmethod
    def getRoots(self):
        return Page.objects.filter(menugroup=0).order_by('ordering')

    def __repr__(self):
        return u'Page '+self.title