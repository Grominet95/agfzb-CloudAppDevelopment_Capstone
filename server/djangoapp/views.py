from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer
from .restapis import get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
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

    
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://b00813372-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

def get_dealer_details(request, dealer_id):
    url = "https://b00813372-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={}"
    reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
    review_content = ' '.join([f"Review: {review.review}, Sentiment: {review.sentiment}" for review in reviews])
    return HttpResponse(review_content)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

