from django_microservice_common.api.class_responses.error_response import ErrorResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from src.property_finder.apis.v1.serializers.property_type import PropertyTypeOutputSerializer
from src.property_finder.usecases.propetry import GetPropertyTypes


class GetAllPropertyTypeApi(APIView):
    """
    API endpoint for retrieving all Property types.

    This endpoint handles the retrieval of all Property types using the `GetPropertyTypes` use case.
    It returns a list of available Property types.
    """

    def __init__(self, **kwargs):
        """
        Initializes the GetAllPropertyTypeApi with a dependency on GetPropertyTypes use case.
        """
        super(GetAllPropertyTypeApi, self).__init__(**kwargs)
        self.usecase = GetPropertyTypes()

    @extend_schema(responses=PropertyTypeOutputSerializer, tags=['Property Types'])
    def post(self, request):
        """
        Handles the POST request to retrieve all property types.

        Calls the `GetPropertyTypes` use case to fetch all property types and returns the list of Property types
        serialized using `PropertyTypeOutputSerializer`.
        """
        try:
            result = self.usecase.execute()
            response = PropertyTypeOutputSerializer(instance=result, context={'request': request}, many=True).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)
