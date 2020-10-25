from django.contrib import admin
from .models import Collection, Item


class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    list_display = ['title','id','user','archived']

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ['name','id','user', 'collection']

admin.site.register(Collection,CollectionAdmin)
admin.site.register(Item,ItemAdmin)
