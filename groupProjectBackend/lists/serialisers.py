from rest_framework import serializers
from .models import Collection, Item
from django.db.models import F 

class CollectionSerialiser(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    date_created = serializers.ReadOnlyField()
    last_updated = serializers.ReadOnlyField()
    signed_pk = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = '__all__'


class ItemSerialiser(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    date_created = serializers.ReadOnlyField()
    last_updated = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = '__all__'


class CollectionDetailSerialiser(CollectionSerialiser):
   collection_items = serializers.SerializerMethodField()

   # overrides the default method to get the items for a collection
   # because I want to order it in a different way
   # first by ranking, with null items last, then by the most recently updated
   def get_collection_items(self, instance):
     items = instance.collection_items.all().order_by(F('ranking').asc(nulls_last=True), '-last_updated')
     return ItemSerialiser(items,many=True).data





