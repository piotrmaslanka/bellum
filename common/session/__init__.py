'''Handles issues which relate to sessions and their mechanisms of storage'''

from bellum.register.models import Account
from bellum.mother.models import Technology, Mother

def getRace(request):
    return request.session['Account.race']

def getAccountId(request):
    return request.session['Account.id']

def getAccount(request):
    return Account.objects.get(id=getAccountId(request))

def getTechnologyId(request):
    return request.session['Technology.id']

def getTechnology(request):
    return Technology.objects.get(id=request.session['Technology.id'])

def getResourceIndexId(request):
    return request.session['ResourceIndex.id']
    
def getResourceIndex(request):
    from bellum.common.models import ResourceIndex
    return ResourceIndex.objects.get(id=request.session['ResourceIndex.id'])