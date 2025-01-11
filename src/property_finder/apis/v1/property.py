from django_microservice_common.api.class_responses.error_response import ErrorResponse, MessageResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from property_finder.usecases.propetry import GetPropertyUseCase
from src.property_finder.apis.v1.serializers.property import CreatePropertyInputSerializer, PropertyOutputSerializer, \
    SearchPropertyInputSerializer, SearchPropertyOutputSerializer, UpdatePropertyInputSerializer
from src.property_finder.usecases.propetry import CreatePropertyUseCase, DeletePropertyUseCase, SearchPropertyUseCase, \
    UpdatePropertyUseCase


class CreatePropertyApi(APIView):
    def __init__(self, **kwargs):
        super(CreatePropertyApi, self).__init__(**kwargs)
        self.usecase = CreatePropertyUseCase()

    @extend_schema(request=CreatePropertyInputSerializer, responses=PropertyOutputSerializer, tags=['Property'])
    def post(self, request):
        try:
            serializer = CreatePropertyInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.usecase.execute(**request.data)
            response = PropertyOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class UpdatePropertyApi(APIView):
    def __init__(self, **kwargs):
        super(UpdatePropertyApi, self).__init__(**kwargs)
        self.usecase = UpdatePropertyUseCase()

    @extend_schema(request=UpdatePropertyInputSerializer, responses=PropertyOutputSerializer, tags=['Property'])
    def patch(self, request, property_id):
        try:
            serializer = UpdatePropertyInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.usecase.execute(pk=property_id, updates=serializer.validated_data)
            response = PropertyOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class DeletePropertyApi(APIView):
    def __init__(self, **kwargs):
        super(DeletePropertyApi, self).__init__(**kwargs)
        self.usecase = DeletePropertyUseCase()

    @extend_schema(request=UpdatePropertyInputSerializer, responses=PropertyOutputSerializer, tags=['Property'])
    def delete(self, request, property_id: int):
        try:
            self.usecase.execute(pk=property_id)
            return MessageResponse("Property successfully deleted.")
        except Exception as exception:
            return ErrorResponse(exception=exception)


class GetPropertyApi(APIView):
    def __init__(self, **kwargs):
        super(GetPropertyApi, self).__init__(**kwargs)
        self.usecase = GetPropertyUseCase()

    @extend_schema(responses=PropertyOutputSerializer, tags=['Property'])
    def get(self, request, property_id: int):
        try:
            instance = self.usecase.execute(pk=property_id)
            response = PropertyOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class SearchPropertyApi(APIView):
    def __init__(self, **kwargs):
        super(SearchPropertyApi, self).__init__(**kwargs)
        self.usecase = SearchPropertyUseCase()

    @extend_schema(parameters=[SearchPropertyInputSerializer], responses=SearchPropertyOutputSerializer, tags=['Property'])
    def get(self, request):
        try:

            serializer = SearchPropertyInputSerializer(data=request.query_params.dict())
            serializer.is_valid(raise_exception=True)
            result = self.usecase.execute(**serializer.validated_data)
            response = SearchPropertyOutputSerializer(data=result, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)
