'''Inserts resource information to the template'''
from bellum.common.session import getAccount
      
def plug_in(primaryguiobject):
    primaryguiobject.registerObject('account', getAccount(primaryguiobject._request))
    
