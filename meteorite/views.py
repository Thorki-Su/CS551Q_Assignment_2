from django.shortcuts import render, get_object_or_404, redirect
from .models import Meteorite
import random
from django.core.paginator import Paginator
from faker import Faker
from django.contrib import messages

fake = Faker()

# Create your views here.
def homepage(request):
    meteorites = Meteorite.objects.all()
    random_meteorites = random.sample(list(meteorites), 10)
    context = {
        'random_meteorites': random_meteorites,
    }
    return render(request,'meteorite/homepage.html', context=context)

def meteorite_list(request):
    search_query = request.GET.get('search', '')
    meteorites = Meteorite.objects.all().order_by('id')
    sort_by = request.GET.get('sort', '')
    fall_filter = request.GET.get('fall', '')
    nametype_filter = request.GET.get('nametype', '')
    year_filter = request.GET.get('year', '')
    mass_filter = request.GET.get('mass', '')
    #search
    if search_query:
        meteorites = meteorites.filter(name__icontains=search_query)
    #sort
    if sort_by == 'mass_asc':
        meteorites = meteorites.order_by('mass')
    elif sort_by == 'mass_desc':
        meteorites = meteorites.order_by('-mass')
    elif sort_by == 'name_asc':
        meteorites = meteorites.order_by('name')
    elif sort_by == 'name_desc':
        meteorites = meteorites.order_by('-name')
    elif sort_by == 'id_asc':
        meteorites = meteorites.order_by('id')
    elif sort_by == 'id_desc':
        meteorites = meteorites.order_by('-id')
    else:
        meteorites = meteorites.order_by('id')
    #filter
    #by fall
    if fall_filter:
        meteorites = meteorites.filter(fall=fall_filter)
    #by nametype
    if nametype_filter:
        meteorites = meteorites.filter(nametype=nametype_filter)
    #by year
    if year_filter == 'before_2000':
        meteorites = meteorites.filter(year__lte=1999)
    elif year_filter == 'after_2000':
        meteorites = meteorites.filter(year__gte=2000)
    #by mass
    if mass_filter == 'small':
        meteorites = meteorites.filter(mass__lte=100)
    elif mass_filter == 'medium':
        meteorites = meteorites.filter(mass__gt=100, mass__lte=1000)
    elif mass_filter == 'large':
        meteorites = meteorites.filter(mass__gt=1000)
    #page
    paginator = Paginator(meteorites, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'fall_filter': fall_filter,
        'sort_by': sort_by,
    }
    return render(request,'meteorite/list.html', context=context)

def meteorite_detail(request, meteorite_id):
    meteorite = get_object_or_404(Meteorite, id=meteorite_id)
    #get similar meteorites
    similar_meteorites = Meteorite.objects.filter(
        recclass=meteorite.recclass
    ).exclude(id=meteorite.id)[:5]
    #get story for fell-meteorite
    background_story = None
    background_story = generate_meteorite_story(meteorite)
    context = {
        'meteorite': meteorite,
        'similar_meteorites': similar_meteorites,
        'background_story': background_story,
    }
    return render(request,'meteorite/detail.html', context=context)

def generate_meteorite_story(meteorite):
    seasons = ['spring', 'summer', 'autumn', 'winter']
    witnesses = ['farmer', 'shepherd', 'traveler', 'villager', 'hunter']
    legends = [
        'the guardian of the village',
        'a miracle for scientific research',
        'a legend passed down for generations',
        'a treasure in the museum',
        'the hero story of local children'
    ]

    year = meteorite.year
    season = random.choice(seasons)
    location = fake.city()
    witness = random.choice(witnesses)
    legend = random.choice(legends)
    name = fake.name()
    job = fake.job()
    if meteorite.fall == "Fell":
        story = (
            f"In the {season} of {year}, a dazzling light streaked across the sky over {location}. "
            f"The meteorite \"{meteorite.name}\" descended and was witnessed by a {witness}. "
            f"Since then, it has become known as {legend}."
        )
    else:
        story = (
            f"In the {season} of {year}, the meteorite \"{meteorite.name}\" was found in {location}."
            f"A {job} named {name} found it, and then sent it to laboratory."
        )
    return story

def set_marked(request, meteorite_id):
    request.session['marked_id'] = meteorite_id
    return redirect('meteorite:meteorite_detail', meteorite_id=meteorite_id)

def compare_with_marked(request, meteorite_id):
    meteorite = get_object_or_404(Meteorite, id=meteorite_id)
    marked_id = request.session.get('marked_id')
    if not marked_id:
        messages.warning(request, "No meteorite has been marked for comparison.")
        return redirect('meteorite:meteorite_detail', meteorite_id=meteorite_id)
    if marked_id == meteorite_id:
        messages.info(request, "You're comparing the same meteorite.")
        return redirect('meteorite:meteorite_detail', meteorite_id=meteorite_id)
    marked_meteorite = get_object_or_404(Meteorite, id=marked_id)
    print(f"Comparing: {marked_meteorite.name} vs {meteorite.name} one")
    return render(request, 'meteorite/compare.html', {
        'meteorite1': marked_meteorite,
        'meteorite2': meteorite
    })

def compare(request, id1, id2):
    meteorite1 = get_object_or_404(Meteorite, id=id1)
    meteorite2 = get_object_or_404(Meteorite, id=id2)
    print(f"Comparing: {meteorite1.name} vs {meteorite2.name} two")
    return render(request, 'meteorite/compare.html', {
        'meteorite1': meteorite1,
        'meteorite2': meteorite2
    })

def clear_marked(request):
    if 'marked_id' in request.session:
        del request.session['marked_id']
    return redirect('meteorite:meteorite_list')