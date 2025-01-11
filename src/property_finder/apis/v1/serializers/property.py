from rest_framework import serializers

from property_finder.apis.v1.serializers.agent import AgentOutputSerializer
from property_finder.apis.v1.serializers.property_type import PropertyTypeBriefOutputSerializer
from src.property_finder.models import Property


class CreatePropertyInputSerializer(serializers.Serializer):
    main_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    sub_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    agent = serializers.IntegerField(required=True, allow_null=False, min_value=1)


class UpdatePropertyInputSerializer(serializers.Serializer):
    main_type_id = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    sub_type_id = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    agent_id = serializers.IntegerField(required=True, allow_null=False, min_value=1)


class SearchPropertyInputSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    size = serializers.IntegerField(required=False, allow_null=False, min_value=1)
    page = serializers.IntegerField(required=False, allow_null=False, min_value=1)


class SearchPropertyOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    score = serializers.FloatField(required=True, allow_null=False, min_value=0.0)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class PropertyOutputSerializer(serializers.ModelSerializer):
    main_type = PropertyTypeBriefOutputSerializer()
    sub_type = PropertyTypeBriefOutputSerializer()
    agent = AgentOutputSerializer()

    class Meta:
        model = Property
        fields = '__all__'
