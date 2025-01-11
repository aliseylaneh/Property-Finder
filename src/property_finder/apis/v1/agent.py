from django_microservice_common.api.class_responses.error_response import ErrorResponse, MessageResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from property_finder.usecases.agent import GetAgentUseCase
from property_finder.apis.v1.serializers.drf.agent import AgentOutputSerializer, CreateAgentInputSerializer, \
    SearchAgentInputSerializer, UpdateAgentInputSerializer
from src.property_finder.usecases.agent import CreateAgentUseCase, DeleteAgentUseCase, SearchAgentUseCase, UpdateAgentUseCase


class CreateAgentApi(APIView):
    def __init__(self, **kwargs):
        super(CreateAgentApi, self).__init__(**kwargs)
        self.usecase = CreateAgentUseCase()

    @extend_schema(request=CreateAgentInputSerializer, responses=AgentOutputSerializer, tags=['Agent'])
    def post(self, request):
        try:
            serializer = CreateAgentInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.usecase.execute(**request.data)
            response = AgentOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class UpdateAgentApi(APIView):
    def __init__(self, **kwargs):
        super(UpdateAgentApi, self).__init__(**kwargs)
        self.usecase = UpdateAgentUseCase()

    @extend_schema(request=UpdateAgentInputSerializer, responses=AgentOutputSerializer, tags=['Agent'])
    def patch(self, request, agent_id):
        try:
            serializer = UpdateAgentInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.usecase.execute(pk=agent_id, updates=serializer.validated_data)
            response = AgentOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class DeleteAgentApi(APIView):
    def __init__(self, **kwargs):
        super(DeleteAgentApi, self).__init__(**kwargs)
        self.usecase = DeleteAgentUseCase()

    @extend_schema(request=UpdateAgentInputSerializer, responses=AgentOutputSerializer, tags=['Agent'])
    def delete(self, request, agent_id: int):
        try:
            self.usecase.execute(pk=agent_id)
            return MessageResponse("Agent successfully deleted.")
        except Exception as exception:
            return ErrorResponse(exception=exception)


class GetAgentApi(APIView):
    def __init__(self, **kwargs):
        super(GetAgentApi, self).__init__(**kwargs)
        self.usecase = GetAgentUseCase()

    @extend_schema(responses=AgentOutputSerializer, tags=['Agent'])
    def get(self, request, agent_id: int):
        try:
            instance = self.usecase.execute(pk=agent_id)
            response = AgentOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class SearchAgentApi(APIView):
    def __init__(self, **kwargs):
        super(SearchAgentApi, self).__init__(**kwargs)
        self.usecase = SearchAgentUseCase()

    @extend_schema(request=SearchAgentInputSerializer, responses=AgentOutputSerializer, tags=['Agent'])
    def get(self, request):
        try:
            instance = self.usecase.execute()
            response = AgentOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)
