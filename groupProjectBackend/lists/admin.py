from django.contrib import admin
from .models import Collection, Item, Ranking


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    list_display = ['title','id','user','is_active','date_created','attribute1','attribute2', 'attribute3', 'attribute4']
    list_filter = ('is_active','user')

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name','id','user','collection', 'is_active']
    list_filter = ('is_active', 'user', 'collection')



@admin.register(Ranking)    
class RankingAdmin(admin.ModelAdmin):
   model = Ranking
   list_display = ['id', 'collection', 'item', 'rank']
   list_filter = ('collection')

admin.site.register(Item,ItemAdmin)

