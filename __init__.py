'''Bellum is a sci-fi MMO. Read README for details'''

from django.http import HttpResponse

def robots(request):
    return HttpResponse('''User-agent: *
Disallow: /register/''')