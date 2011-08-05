def cacheContactEID(request, id, empire):
    try:
        request.session['ChatCache'][id]
    except:
        request.session['ChatCache'][id] = empire
        request.session.modified = True

def cacheContactAcc(request, account_object):
    cacheContactEID(request, account_object.id, account_object.empire)
    