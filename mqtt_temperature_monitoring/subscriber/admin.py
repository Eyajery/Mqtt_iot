from django.contrib import admin

# Register your models here.

from .models import Temperature


admin.site.register(Temperature)