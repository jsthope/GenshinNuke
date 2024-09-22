from django.contrib import admin

# Register your models here.

from .models import Room, Character, Weapon, Profile

admin.site.register(Room)
admin.site.register(Character)
admin.site.register(Weapon)
admin.site.register(Profile)
