def getCurrentMother(request):
    from bellum.mother.models import Mother
    return Mother.objects.get(id=request.session['Mother.id'])