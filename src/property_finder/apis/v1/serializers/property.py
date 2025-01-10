from rest_framework import serializers

from src.property_finder.models import Property


class CreatePropertyInputSerializer(serializers.Serializer):
    main_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    sub_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    agent = serializers.IntegerField(required=True, allow_null=False, min_value=1)


class UpdatePropertyInputSerializer(serializers.Serializer):
    main_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    sub_type = serializers.IntegerField(required=True, allow_null=False, min_value=1)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(required=True, allow_null=False, allow_blank=True)
    agent = serializers.IntegerField(required=True, allow_null=False, min_value=1)


class PropertyOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
