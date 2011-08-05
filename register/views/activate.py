from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import RegisterConfirmation

def process(request):
    from bellum.common.register.activate import activate
    
    try:
        request.GET['key']
    except:
        return redirect('/')
    
    try:
        rc = RegisterConfirmation.objects.get(key=request.GET['key'])
    except ValueError:
        return render_to_response('register/activate/failed.html', {})
        
    acc = rc.account
    rc.delete()
    
    activate(acc)
    
    return render_to_response('register/activate/success.html', {})
    
