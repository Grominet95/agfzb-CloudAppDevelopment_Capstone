from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    path('', views.get_dealerships, name='index'),

    path('dealerships/', views.get_dealerships, name='dealerships'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
