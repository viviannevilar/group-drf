from django.contrib import admin
from .models import Collection, Item


class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    list_display = ['title','id','user','archived','date_created','attribute1','attribute2', 'attribute3', 'attribute4','attribute5']

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ['name','id','user','collection','date_created','attribute1','attribute2', 'attribute3', 'attribute4','attribute5']

admin.site.register(Collection,CollectionAdmin)
admin.site.register(Item,ItemAdmin)

