from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .forms import CarForm
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse, HttpRequest,HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# Car_List
def car_list(request):
    
    cars = Car.objects.all()
    colors = Car.objects.order_by().values_list('color', flat=True).distinct()
    selected_color = request.GET.get('color','')
    if selected_color:
        cars = cars.filter(color=selected_color)
    cars = cars.order_by('position', 'id')
    paginator = Paginator(cars, 10)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    return render(request, 'car_list.html', {'cars': cars, 'colors': colors, 'selected_color': selected_color})

# basic crud

# READ - Car_detail / Display Car details
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'car_detail.html', {'car': car})

# CREATE
def car_addnew(request):
    return redirect(car_edit)

def car_new(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.save()
            return redirect('car_list') 
    else:
        form = CarForm()
    return render(request, 'car_edit.html', {'form': form})

# EDIT/UPDATE
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            car = form.save(commit=False)
            car.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'car_edit.html', {'form': form})

# DELETE
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('car_list')


#FUNCTIONS

def update_position(request):
    if request.method == 'POST':
        car_id = request.POST.get('item_id')
        reference_item_id = request.POST.get('reference_item_id')
        
        #check current and reference id
        print('car_id:'+car_id)
        print('ref_id:'+reference_item_id)

        try:
            car = Car.objects.get(pk=car_id)
            reference_item = Car.objects.get(pk=reference_item_id)

            # Swap positions of the items
            car.position, reference_item.position = reference_item.position, car.position
            
            #chect new position value
            print(car.position)
            print(reference_item.position)
            
            if car.position==reference_item.position :
                car.position+.5
                car.save()
            else :
                car.save()
                reference_item.save()
            
            return HttpResponse(status=200)
        except (Car.DoesNotExist, ValueError):
            return HttpResponse(status=400),
    else:
        return HttpResponse(status=405)


    