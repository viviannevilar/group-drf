from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid
from datetime import datetime
from django.core.signing import Signer
from django.urls import reverse
import os

# Create your models here.
User = get_user_model()


class Collection(models.Model):
    title = models.CharField(max_length=30) 
    attribute1 = models.CharField(max_length = 15,blank=True, null=True)
    attribute2 = models.CharField(max_length = 15,blank=True, null=True)
    attribute3 = models.CharField(max_length = 15,blank=True, null=True)
    attribute4 = models.CharField(max_length = 15,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    #ranking = models.ManyToManyField('Item', related_name='items_ranking',)
    user = models.ForeignKey(
      User,
      on_delete = models.CASCADE,
      related_name = 'owner_collections',
    )
    signer = Signer(sep='/', salt='collection')
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, 
      related_name='shared_collections', blank=True)

    @property
    def signed_pk(self):
        return self.signer.sign(self.pk)

    def __str__(self):
        return self.title
    
    
class Item(models.Model):
    def upload_image_to(instance, filename):   
        filename_base, filename_ext = os.path.splitext(filename)        
        u = uuid.uuid4()
        #datetime.now().strftime("%Y%m%d")
        return'uploads/%s_%s' % (filename_base, u.hex) 

    name = models.CharField(max_length= 30)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    attribute1 = models.CharField(max_length = 15,blank=True, null=True)
    attribute2 = models.CharField(max_length = 15,blank=True, null=True)
    attribute3 = models.CharField(max_length = 15,blank=True, null=True)
    attribute4 = models.CharField(max_length = 15,blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)
    sale_amount = models.IntegerField(blank=True, null=True)
    sale_end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(max_length = 100, blank=True)
    collection = models.ForeignKey(
        Collection,
        on_delete = models.CASCADE,
        related_name = 'collection_items'
    )

    image = models.ImageField(upload_to=upload_image_to, editable=True, blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'owner_items',
    )


# class Ranking(models.Model):
#    collection = models.ForeignKey(
#       Collection,
#       on_delete = models.CASCADE,
#       related_name = "ranking_collections"
#    )
#    item = models.ForeignKey(
#       Item,
#       on_delete=models.CASCADE,
#       related_name = "ranking_items"
#    )
#    rank = models.IntegerField(blank=True, null=True)
      
#    class Meta:
#       unique_together = ('collection', 'item')
