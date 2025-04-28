from django.shortcuts import render, get_object_or_404
from .models import Meteorite

# Create your views here.
def homepage(request):
    return render(request,'meteorite/homepage.html')

def meteorite_list(request):
    meteorites = Meteorite.objects.all()
    context = {
        'meteorites': meteorites,
    }
    return render(request,'meteorite/list.html', context=context)

def meteorite_detail(request, meteorite_id):
    meteorite = get_object_or_404(Meteorite, id=meteorite_id)
    # meteorites = Meteorite.objects.all()
    context = {
        'meteorite': meteorite,
        # 'meteorites': meteorites,
    }
    return render(request,'meteorite/detail.html', context=context)