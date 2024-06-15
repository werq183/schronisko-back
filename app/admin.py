from django.contrib import admin

# Register your models here.
from .models import UserProfile, Kot, Ogloszenie, Zdjecie, Rezerwacja

admin.site.register(UserProfile)
admin.site.register(Kot)
admin.site.register(Ogloszenie)
admin.site.register(Zdjecie)
admin.site.register(Rezerwacja)