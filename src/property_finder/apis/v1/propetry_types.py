from django_microservice_common.api.class_responses.error_response import ErrorResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from property_finder.apis.v1.serializers.property_type import PropertyTypeOutputSerializer
from property_finder.usecases.propetry import GetPropertyTypes


class GetAllPropertyTypeApi(APIView):
    def __init__(self, **kwargs):
        super(GetAllPropertyTypeApi, self).__init__(**kwargs)
        self.usecase = GetPropertyTypes()

    @extend_schema(responses=PropertyTypeOutputSerializer, tags=['Property Types'])
    def post(self, request):
        try:
            result = self.usecase.execute()
            response = PropertyTypeOutputSerializer(instance=result, context={'request': request}, many=True).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)
