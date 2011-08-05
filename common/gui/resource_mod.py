'''Inserts resource information to the template'''
from math import floor
from bellum.common.session import getResourceIndex
        
def plug_in(primaryguiobject):
    primaryguiobject.registerObject('resources', getResourceIndex(primaryguiobject._request).stateUpdate())
