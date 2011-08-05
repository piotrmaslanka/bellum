def ensure(id, objtype):
    '''If ID is a int or long, will make a Django
       model instance of class objtype with given ID.
       Else, will return ID'''
    if (type(id)==int) or (type(id)==long):
        return objtype.objects.get(id=id)
    else:
        return id

def ensureID(id):
    '''Does something like ensure(), but gets ID'''
    if (type(id)==int) or (type(id)==long):
        return id
    else:
        return id.id

