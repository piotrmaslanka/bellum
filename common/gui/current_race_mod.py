'''Inserts race information to the template'''
from bellum.common.session import getRace
      
def plug_in(primaryguiobject):
    primaryguiobject.registerObject('race', getRace(primaryguiobject._request))
    
