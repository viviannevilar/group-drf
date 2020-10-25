from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Collection(models.Model):
    title = models.CharField(max_length=30) 
    attribute1 = models.CharField(max_length = 15)
    attribute2 = models.CharField(max_length = 15)
    attribute3 = models.CharField(max_length = 15)
    attribute4 = models.CharField(max_length = 15)
    attribute5 = models.CharField(max_length = 15)
    archived = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'owner_collections',
    )
    

class Item(models.Model):
    name = models.CharField(max_length= 30)
    is_active = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    attribute1 = models.CharField(max_length = 15)
    attribute2 = models.CharField(max_length = 15)
    attribute3 = models.CharField(max_length = 15)
    attribute4 = models.CharField(max_length = 15)
    attribute5 = models.CharField(max_length = 15)
    notes = models.TextField(max_length = 100)
    collection = models.ForeignKey(
        Collection,
        on_delete = models.CASCADE,
        related_name = 'collection_items'
    )
    image = models.URLField()
    ranking = models.IntegerField()
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'owner_items',
    )