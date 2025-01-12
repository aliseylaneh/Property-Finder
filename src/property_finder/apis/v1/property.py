from django_microservice_common.api.class_responses.error_response import ErrorResponse, MessageResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from src.property_finder.apis.v1.serializers.property import CreatePropertyInputSerializer, PropertyOutputSerializer, \
    SearchPropertyInputSerializer, SearchPropertyOutputSerializer, UpdatePropertyInputSerializer
from src.property_finder.usecases.propetry import GetPropertyUseCase
from src.property_finder.usecases.propetry import CreatePropertyUseCase, DeletePropertyUseCase, SearchPropertyUseCase, \
    UpdatePropertyUseCase


class CreatePropertyApi(APIView):
    """
    API endpoint for creating a Property.

    This endpoint accepts input data via the `POST` method, validates it, and creates a new Property using the
    `CreatePropertyUseCase`. The response includes the details of the newly created Property.
    """

    def __init__(self, **kwargs):
        """
        Initializes the CreatePropertyApi with a dependency on CreatePropertyUseCase.
        """
        super(CreatePropertyApi, self).__init__(**kwargs)
        self.usecase = CreatePropertyUseCase()

    @extend_schema(request=CreatePropertyInputSerializer, responses=PropertyOutputSerializer, tags=['Property'])
    def post(self, request):
        """
        Handles the POST request to create a Property.

        Validates the request data using `CreatePropertyInputSerializer` and calls the use case to create a Property.
        Returns the serialized output of the created Property.
        """
        try:
            serializer = CreatePropertyInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.usecase.execute(**request.data)
            response = PropertyOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class UpdatePropertyApi(APIView):
    """
    API endpoint for updating a Property.

    This endpoint accepts input data via the `PATCH` method, validates it, and updates an existing Property
    identified by its ID using the `UpdatePropertyUseCase`. The response includes the updated Property details.
    """

    def __init__(self, **kwargs):
        """
        Initializes the UpdatePropertyApi with a dependency on UpdatePropertyUseCase.
        """
        super(UpdatePropertyApi, self).__init__(**kwargs)
        self.usecase = UpdatePropertyUseCase()

    @extend_schema(request=UpdatePropertyInputSerializer, responses=PropertyOutputSerializer, tags=['Property'])
    def patch(self, request, property_id):
        """
        Handles the PATCH request to update a Property.

        Validates the request data using `UpdatePropertyInputSerializer` and calls the use case to update the
        Property identified by `property_id`. Returns the serialized output of the updated Property.
        """
        try:
            serializer = UpdatePropertyInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = self.usecase.execute(pk=property_id, updates=serializer.validated_data)
            return Response(result)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class DeletePropertyApi(APIView):
    """
    API endpoint for deleting a Property.

    This endpoint handles the deletion of a Property identified by its ID using the `DeletePropertyUseCase`.
    """

    def __init__(self, **kwargs):
        """
        Initializes the DeletePropertyApi with a dependency on DeletePropertyUseCase.
        """
        super(DeletePropertyApi, self).__init__(**kwargs)
        self.usecase = DeletePropertyUseCase()

    @extend_schema(request=UpdatePropertyInputSerializer, responses=PropertyOutputSerializer, tags=['Property'])
    def delete(self, request, property_id: int):
        """
        Handles the DELETE request to remove a Property.

        Deletes the Property identified by `property_id` and returns a success message upon completion.
        """
        try:
            self.usecase.execute(pk=property_id)
            return MessageResponse("Property successfully deleted.")
        except Exception as exception:
            return ErrorResponse(exception=exception)


class GetPropertyApi(APIView):
    """
    API endpoint for retrieving a Property's details.

    This endpoint fetches the details of a Property identified by its ID using the `GetPropertyUseCase`.
    """

    def __init__(self, **kwargs):
        """
        Initializes the GetPropertyApi with a dependency on GetPropertyUseCase.
        """
        super(GetPropertyApi, self).__init__(**kwargs)
        self.usecase = GetPropertyUseCase()

    @extend_schema(responses=PropertyOutputSerializer, tags=['Property'])
    def get(self, request, property_id: int):
        """
        Handles the GET request to retrieve a Property's details.

        Fetches the details of the Property identified by `property_id` and returns the serialized output.
        """
        try:
            instance = self.usecase.execute(pk=property_id)
            response = PropertyOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class SearchPropertyApi(APIView):
    """
    API endpoint for searching properties.

    This endpoint allows searching for properties based on query parameters using the `SearchPropertyUseCase`.
    """

    def __init__(self, **kwargs):
        """
        Initializes the SearchPropertyApi with a dependency on SearchPropertyUseCase.
        """
        super(SearchPropertyApi, self).__init__(**kwargs)
        self.usecase = SearchPropertyUseCase()

    @extend_schema(parameters=[SearchPropertyInputSerializer], responses=SearchPropertyOutputSerializer, tags=['Property'])
    def get(self, request):
        """
        Handles the GET request to search for properties.

        Validates the query parameters using `SearchPropertyInputSerializer` and calls the use case to perform the
        search. Returns a list of serialized Property details matching the search criteria.
        """
        try:
            serializer = SearchPropertyInputSerializer(data=request.query_params.dict())
            serializer.is_valid(raise_exception=True)

            result = self.usecase.execute(**serializer.validated_data)

            response_serializer = SearchPropertyOutputSerializer(data=result, context={'request': request}, many=True)
            response_serializer.is_valid(raise_exception=True)

            return Response(response_serializer.validated_data)
        except Exception as exception:
            return ErrorResponse(exception=exception)
