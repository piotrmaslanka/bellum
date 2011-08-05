from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response

def index(request):
    return render_to_response('register/portal/index.html', {})
def contact(request):
    return render_to_response('register/portal/contact.html', {})
def regulamin(request):
    return render_to_response('register/portal/regulamin.html', {})
def about(request):
    return render_to_response('register/portal/about.html', {})



