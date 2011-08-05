'''Inserts resource information to the template'''
from bellum.mother.models import Mother
from bellum.common.session import getAccount
      
def plug_in(primaryguiobject):
    primaryguiobject.registerObject('my_mothers', Mother.objects.filter(owner=getAccount(primaryguiobject._request)))
    
