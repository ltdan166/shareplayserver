from django.contrib import admin

# Register your models here.
from .models import sp_event, sp_address, sp_location, sp_person, sp_player

admin.site.register(sp_event)
admin.site.register(sp_location)
admin.site.register(sp_person)
admin.site.register(sp_address)
admin.site.register(sp_player)