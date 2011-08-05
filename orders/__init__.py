'''This module contains code to deal with orders, giving orders and their execution'''

class DontRemoveGOT(Exception):
    '''Instructs middleware NOT to automatically remove GOT'''
