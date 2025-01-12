from rest_framework import serializers

from src.property_finder.models import Agent


class CreateAgentInputSerializer(serializers.Serializer):
    """
    This serializer acts as an input serializer for new values in order to create an Agent.
    """
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class UpdateAgentInputSerializer(serializers.Serializer):
    """
    This serializer acts as an input serializer for updated values of an Agent.
    """
    name = serializers.CharField(required=False, allow_null=False, allow_blank=False)
    email = serializers.EmailField(required=False, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=False, allow_null=False, allow_blank=False)


class SearchAgentInputSerializer(serializers.Serializer):
    """
    This serializer acts as an input serializer for searching Agents.
    """
    query = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    size = serializers.IntegerField(required=False, allow_null=False, min_value=1)
    page = serializers.IntegerField(required=False, allow_null=False, min_value=1)


class SearchAgentOutputSerializer(serializers.Serializer):
    """
    This serializer acts as an output serializer for retrieved Agents.
    """
    id = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class AgentOutputSerializer(serializers.ModelSerializer):
    """
    Model serializer of an Agent model, which represents all fields.
    """

    class Meta:
        model = Agent
        fields = "__all__"
