from rest_framework import serializers
from .models import Collection, Item

class CollectionSerialiser(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    date_created = serializers.ReadOnlyField()
    last_updated = serializers.ReadOnlyField()

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
    collection_items = ItemSerialiser(many=True, read_only=True)


