'''Inserts resource information to the template'''
from bellum.common.session.mother import getCurrentMother
from bellum.common.session import getAccount
      
def plug_in(primaryguiobject):
    primaryguiobject.registerObject('mother', getCurrentMother(primaryguiobject._request))
    
