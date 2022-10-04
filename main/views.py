from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def firstpage(request):
    return render(request, 'main/firstpage.html')

@login_required
def index(request):
    return render(request, 'main/index.html')
