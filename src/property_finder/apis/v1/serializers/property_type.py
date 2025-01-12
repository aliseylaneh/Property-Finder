from rest_framework import serializers

from src.property_finder.models import PropertyType


class PropertyTypeOutputSerializer(serializers.ModelSerializer):
    """
    This serializer acts as output serializer for retrieving one or more than on Property Type.
    """
    depth = serializers.SerializerMethodField()

    def get_depth(self, obj):
        """
        Depth fields is a models.IntegerField so it's need to be represented in string format to end users.
        """
        return obj.get_depth_display()

    class Meta:
        model = PropertyType
        fields = '__all__'


class PropertyTypeBriefOutputSerializer(serializers.ModelSerializer):
    """
    Brief serializer is used for representing limited fields. For example, it would be used as relationship serializer.
    """

    class Meta:
        model = PropertyType
        fields = ('id', 'title')
