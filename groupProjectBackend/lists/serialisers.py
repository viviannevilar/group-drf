from rest_framework import serializers
from .models import Collection, Item
from django.db.models import F 
from users.serializers import UserShareSerialiser

class CollectionSerialiser(serializers.ModelSerializer):
  ''' used by the following views:
  - CollectionsList: collections/
  - CollectionsArchiveList: archived-collections/
  - CollectionsActiveList: active-collections/
  - 

  '''
  user = serializers.ReadOnlyField(source='user.username')
  date_created = serializers.ReadOnlyField()
  last_updated = serializers.ReadOnlyField()
  signed_pk = serializers.ReadOnlyField()

  class Meta:
    model = Collection
    exclude = ['allowed_users', ]
    # fields = '__all__'


class ItemSerialiser(serializers.ModelSerializer):
  ''' used by the following views:
  - ItemsActiveList:       active-items/
  - ItemsArchiveList:      archived-items/
  - CollectionItemsCreate: collection/<int:collection>/items/
  - ItemCollectionDetail:  item/<int:collection>/<int:pk>/

  '''
  user = serializers.ReadOnlyField(source='user.username')
  date_created = serializers.ReadOnlyField()
  last_updated = serializers.ReadOnlyField()
  is_active = serializers.ReadOnlyField()

  class Meta:
    model = Item
    fields = '__all__'


class CollectionDetailSerialiser(CollectionSerialiser):
  ''' used by the following views:
  - CollectionSafe: collection/safe/<signed_pk>/
  - CollectionDetail: collection/<int:pk>/

  '''
  collection_items = serializers.SerializerMethodField()
  is_active = serializers.ReadOnlyField()

   # overrides the default method to get the items for a collection
   # because I want to order it in a different way
   # first by ranking, with null items last, then by the most recently updated
  def get_collection_items(self, instance):
    items = instance.collection_items.all().order_by(F('ranking').asc(nulls_last=True), '-last_updated')
    return ItemSerialiser(items,many=True).data


class CollectionSimpleDetailSerialiser(serializers.ModelSerializer):
  ''' used by the following views:
  - CollectionSimpleDetail: collection/simple/<int:pk>/
  - 
  '''
  user = serializers.ReadOnlyField(source='user.username')
  date_created = serializers.ReadOnlyField()
  last_updated = serializers.ReadOnlyField()

  class Meta:
    model = Collection
    fields = ['user','id', 'title', 'attribute1', 'attribute2', 'attribute3','attribute4','is_active', 'date_created', 'last_updated']


class CollectionSharedSerialiser(serializers.ModelSerializer):
  ''' used by the following views:
  - CollectionSharedUsers: collection/<int:pk>/allowed_users/

  '''
  allowed_users = UserShareSerialiser(many=True, read_only=True)
  user = serializers.ReadOnlyField(source='user.username')

  class Meta:
    model = Collection
    fields = ['user', 'id', 'title', 'allowed_users']