from django.contrib import admin
from .models import CarMake, CarModel

# Inline CarModelAdmin to use with CarMakeAdmin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # How many extra forms to display

# CarMakeAdmin which incorporates the CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register your models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
