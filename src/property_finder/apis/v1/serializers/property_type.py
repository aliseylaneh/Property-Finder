from rest_framework import serializers

from property_finder.models import PropertyType


class PropertyTypeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'


class PropertyTypeBriefOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ('id', 'title')
