from django_microservice_common.api.class_responses.error_response import ErrorResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from src.property_finder.apis.v1.serializers.property import CreatePropertyInputSerializer, CreatePropertyOutputSerializer
from src.property_finder.usecases.propetry import CreatePropertyUseCase


class CreatePropertyApi(APIView):
    def __init__(self, **kwargs):
        super(CreatePropertyApi, self).__init__(**kwargs)
        self.usecase = CreatePropertyUseCase()

    @extend_schema(request=CreatePropertyInputSerializer, responses=CreatePropertyOutputSerializer, tags=['Property'])
    def post(self, request):
        try:
            serializer = CreatePropertyInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.usecase.execute(**request.data)
            response = CreatePropertyOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)

#
# class CreatePropertyApi(APIView):
#     def __init__(self, **kwargs):
#         super(CreatePropertyApi, self).__init__(**kwargs)
#         self.usecase = CreatePropertyUseCase()
#
#     @extend_schema(request=CreatePropertyInputSerializer, responses=CreatePropertyOutputSerializer, tags=['Property'])
#     def post(self, request):
#         try:
#             serializer = CreatePropertyInputSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             instance = self.usecase.execute(**request.data)
#             response = CreatePropertyOutputSerializer(instance=instance, context={'request': request}).data
#             return Response(response)
#         except Exception as exception:
#             return ErrorResponse(exception=exception)

#
# class CreatePropertyApi(APIView):
#     def __init__(self, **kwargs):
#         super(CreatePropertyApi, self).__init__(**kwargs)
#         self.usecase = CreatePropertyUseCase()
#
#     @extend_schema(request=CreatePropertyInputSerializer, responses=CreatePropertyOutputSerializer, tags=['Property'])
#     def post(self, request):
#         try:
#             serializer = CreatePropertyInputSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             instance =  self.usecase.execute(**request.data)
#             response = CreatePropertyOutputSerializer(instance=instance, context={'request': request}).data
#             return Response(response)
#         except Exception as exception:
#             return ErrorResponse(exception=exception)
#
# class CreatePropertyApi(APIView):
#     def __init__(self, **kwargs):
#         super(CreatePropertyApi, self).__init__(**kwargs)
#         self.usecase = CreatePropertyUseCase()
#
#     @extend_schema(request=CreatePropertyInputSerializer, responses=CreatePropertyOutputSerializer, tags=['Property'])
#     def post(self, request):
#         try:
#             serializer = CreatePropertyInputSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             instance =  self.usecase.execute(**request.data)
#             response = CreatePropertyOutputSerializer(instance=instance, context={'request': request}).data
#             return Response(response)
#         except Exception as exception:
#             return ErrorResponse(exception=exception)
