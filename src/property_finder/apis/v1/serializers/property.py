from rest_framework import serializers

from src.property_finder.apis.v1.serializers.agent import AgentOutputSerializer
from src.property_finder.apis.v1.serializers.property_type import PropertyTypeBriefOutputSerializer
from src.property_finder.models import Property


class CreatePropertyInputSerializer(serializers.Serializer):
    """
    This serializer acts as an input serializer for new values in order to create a Property.
    """
    main_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    sub_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    agent = serializers.IntegerField(required=True, allow_null=False, min_value=1)


class UpdatePropertyInputSerializer(serializers.Serializer):
    """
    This serializer acts as an input serializer for updating values in order to update a Property.
    """
    main_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    sub_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    agent = serializers.IntegerField(required=True, allow_null=False, min_value=1)


class SearchPropertyInputSerializer(serializers.Serializer):
    """
    This serializer acts as an input serializer for searching Properties.
    """
    query = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    size = serializers.IntegerField(required=False, allow_null=False, min_value=1)
    page = serializers.IntegerField(required=False, allow_null=False, min_value=1)


class SearchPropertyOutputSerializer(serializers.Serializer):
    """
    This serializer acts as an output serializer for retrieved Properties.
    """
    id = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    score = serializers.FloatField(required=True, allow_null=False, min_value=0.0)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    main_type = serializers.CharField(required=True, allow_null=False, )
    sub_type = serializers.CharField(required=True, allow_null=False, )
    agent = serializers.CharField(required=True, allow_null=False, )


class PropertyOutputSerializer(serializers.ModelSerializer):
    """
    Model serializer for a Property, with all fields.
    """
    main_type = PropertyTypeBriefOutputSerializer()  # Maintype must be serialized through its relevant serializer
    sub_type = PropertyTypeBriefOutputSerializer()  # Subtype must be serialized through its relevant serializer
    agent = AgentOutputSerializer()  # Agent must be serialized through its relevant serializer

    class Meta:
        model = Property
        fields = '__all__'
