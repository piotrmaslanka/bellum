from bellum.alliance.models import AllianceMembership
from bellum.common.session import getAccountId
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

def mine_alliance(process):
    '''Swaps province_id for province object'''
    def mine_alliance_decorator(*args, **kwargs):
        accid = getAccountId(args[0])
        try:
           amb = AllianceMembership.objects.get(account=accid)
        except ObjectDoesNotExist:
            return redirect('/register/login/')

        return process(*((args[0], ) + (amb, ) + args[2:]), **kwargs)
    return mine_alliance_decorator

def has_not_alliance(process):
    '''Swaps province_id for province object'''
    def has_not_alliance_decorator(*args, **kwargs):
        accid = getAccountId(args[0])
        try:
           amb = AllianceMembership.objects.get(account=accid)
        except ObjectDoesNotExist:
            return process(*args, **kwargs)
        else:
            return redirect('/register/login/')

        return process(*args, **kwargs)
    return has_not_alliance_decorator