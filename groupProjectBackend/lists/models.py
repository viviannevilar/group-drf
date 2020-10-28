from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Collection(models.Model):
    title = models.CharField(max_length=30) 
    attribute1 = models.CharField(max_length = 15,blank=True, null=True)
    attribute2 = models.CharField(max_length = 15,blank=True, null=True)
    attribute3 = models.CharField(max_length = 15,blank=True, null=True)
    attribute4 = models.CharField(max_length = 15,blank=True, null=True)
    attribute5 = models.CharField(max_length = 15,blank=True, null=True)
    is_active = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'owner_collections',
    )

    def __str__(self):
        return self.title
    

class Item(models.Model):
    name = models.CharField(max_length= 30)
    is_active = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    attribute1 = models.CharField(max_length = 15,blank=True, null=True)
    attribute2 = models.CharField(max_length = 15,blank=True, null=True)
    attribute3 = models.CharField(max_length = 15,blank=True, null=True)
    attribute4 = models.CharField(max_length = 15,blank=True, null=True)
    attribute5 = models.CharField(max_length = 15,blank=True, null=True)
    notes = models.TextField(max_length = 100)
    collection = models.ForeignKey(
        Collection,
        on_delete = models.CASCADE,
        related_name = 'collection_items'
    )
    image = models.URLField(blank=True)
    ranking = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'owner_items',
    )