# coding=UTF-8
'''Handles logging out'''
from django.shortcuts import redirect
from bellum.common.session.login import sessLogout, must_be_logged

@must_be_logged
def process(request):
    sessLogout(request)
    return redirect('/')    
    
