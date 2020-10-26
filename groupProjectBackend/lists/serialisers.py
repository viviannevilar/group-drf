from rest_framework import serializers
from .models import Collection

class CollectionSerialiser(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    date_created = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = '__all__'

