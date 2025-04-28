from django.shortcuts import render, get_object_or_404
from .models import Meteorite
import random

# Create your views here.
def homepage(request):
    meteorites = Meteorite.objects.all()
    random_meteorites = random.sample(list(meteorites), 10)
    context = {
        'random_meteorites': random_meteorites,
    }
    return render(request,'meteorite/homepage.html', context=context)

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