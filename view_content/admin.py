from django.contrib import admin
from .models import Room, Zone, Obstruction, Tag, Connection, Session, TagLocation

# Register your models here.
admin.site.register(Room)
admin.site.register(Zone)
admin.site.register(Obstruction)
admin.site.register(Tag)
admin.site.register(Connection)
admin.site.register(Session)
admin.site.register(TagLocation)
