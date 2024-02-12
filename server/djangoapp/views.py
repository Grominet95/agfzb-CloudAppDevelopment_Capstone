from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer
from .restapis import get_dealers_from_cf
from .restapis import post_request
from .restapis import get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('djangoapp:index')
        else:
            # Return an error message.
            messages.error(request, 'Invalid username or password.')
            return redirect('djangoapp:login')
    return render(request, 'djangoapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('djangoapp:index')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        # Add validation for input data as needed
        
        user = User.objects.create_user(username, '', password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)  # Automatically log the user in after registration
        return redirect('djangoapp:index')
    return render(request, 'djangoapp/registration.html')

    
def get_dealerships(request):
    if request.method == "GET":
        url = "https://b00813372-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Update context with dealership list
        context = {'dealership_list': dealerships}
        # Use render to pass the dealership data to the index.html template
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    url = "https://b00813372-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={}".format(dealer_id)
    reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
    context = {'reviews': reviews, 'dealer_id': dealer_id}
    return render(request, 'djangoapp/dealer_details.html', context)



@login_required
def add_review(request, dealer_id):
    if request.method == 'POST':
        review = {
            "time": datetime.utcnow().isoformat(),
            "dealership": dealer_id,
            "review": request.POST.get('review', ''),
            "purchase": request.POST.get('purchase', False),
            "purchase_date": request.POST.get('purchase_date', None),
            "car_make": request.POST.get('car_make', None),
            "car_model": request.POST.get('car_model', None),
            "car_year": request.POST.get('car_year', None),
            "name": request.user.username
        }

        json_payload = {"review": review}
        url = 'Your API endpoint here'  # Replace with your actual endpoint URL
        response = post_request(url, json_payload, dealerId=dealer_id)

        # Optionally, log the response or handle it as needed
        print(response)
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)