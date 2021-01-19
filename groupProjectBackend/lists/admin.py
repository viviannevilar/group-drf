from django.contrib import admin
from .models import Collection, Item

# @admin.register(Ranking)    
# class RankingAdmin(admin.ModelAdmin):
#    model = Ranking
#    list_display = ['id', 'collection', 'item', 'rank']
#    list_filter = ('collection',)

# class RankingAdminInline(admin.TabularInline):
#    model = Collection.ranking.through

#@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    list_display = ['title','id','user','is_active','date_created','attribute1','attribute2', 'attribute3', 'attribute4']
    list_filter = ('is_active','user')
    fields = ('title','user','is_active','attribute1','attribute2', 'attribute3', 'attribute4','date_created','last_updated','allowed_users',)
    readonly_fields = ('last_updated','date_created')
    filter_horizontal = ('allowed_users',)



class ItemAdmin(admin.ModelAdmin):
    list_display = ['name','id','user','collection', 'is_active', 'ranking', 'last_updated']
    list_filter = ('is_active', 'user', 'collection')





admin.site.register(Item,ItemAdmin)
admin.site.register(Collection,CollectionAdmin)


