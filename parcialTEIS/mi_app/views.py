from django.shortcuts import render, redirect
from .forms import FlightForm
from .models import Flight
from django.db.models import Avg

def home(request):
    return render(request, 'home.html')

def register_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_flights')
    else:
        form = FlightForm()
    return render(request, 'register.html', {'form': form})

def list_flights(request):
    flights = Flight.objects.all().order_by('price')
    return render(request, 'list.html', {'flights': flights})

def flight_stats(request):
    nacional_count = Flight.objects.filter(flight_type="Nacional").count()
    internacional_count = Flight.objects.filter(flight_type="Internacional").count()
    avg_price = Flight.objects.filter(flight_type="Nacional").aggregate(Avg('price'))['price__avg'] or 0

    return render(request, 'stats.html', {
        'nacional_count': nacional_count,
        'internacional_count': internacional_count,
        'avg_price': avg_price
    })