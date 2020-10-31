from django.contrib import admin
from .models import Collection, Item


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    list_display = ['title','id','user','is_active','date_created','attribute1','attribute2', 'attribute3', 'attribute4','attribute5', 'signer']
    list_filter = ('is_active','user')

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name','id','user','collection','attribute1','attribute2', 'attribute3', 'attribute4','attribute5','is_active']
    list_filter = ('is_active', 'user', 'collection')

admin.site.register(Item,ItemAdmin)

