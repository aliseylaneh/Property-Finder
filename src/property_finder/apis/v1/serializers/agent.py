from rest_framework import serializers

from src.property_finder.models import Agent


class CreateAgentInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class CreateAgentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"


class UpdateAgentInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class UpdateAgentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"
