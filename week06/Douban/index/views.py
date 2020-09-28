from django.shortcuts import render

from .models import Commentinfo


# Create your views here.
def index(request):
    comments = Commentinfo.objects.filter(star__gt=3)
    return render(request, 'index.html', context={'comments': comments})