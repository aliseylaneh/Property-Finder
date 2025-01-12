from django_microservice_common.api.class_responses.error_response import ErrorResponse, MessageResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from src.property_finder.apis.v1.serializers.agent import AgentOutputSerializer, CreateAgentInputSerializer, \
    SearchAgentInputSerializer, SearchAgentOutputSerializer, UpdateAgentInputSerializer
from src.property_finder.usecases.agent import CreateAgentUseCase, DeleteAgentUseCase, SearchAgentUseCase, UpdateAgentUseCase
from src.property_finder.usecases.agent import GetAgentUseCase


class CreateAgentApi(APIView):
    """
    API endpoint for creating an Agent.

    This endpoint accepts input data via the `POST` method, validates it, and creates a new Agent using the
    `CreateAgentUseCase`. The response includes the details of the newly created Agent.
    """

    def __init__(self, **kwargs):
        """
        Initializes the CreateAgentApi with a dependency on CreateAgentUseCase.
        """
        super(CreateAgentApi, self).__init__(**kwargs)
        self.usecase = CreateAgentUseCase()

    @extend_schema(request=CreateAgentInputSerializer, responses=AgentOutputSerializer, tags=['Agent'])
    def post(self, request):
        """
        Handles the POST request to create an Agent.

        Validates the request data using `CreateAgentInputSerializer` and calls the use case to create an Agent.
        Returns the serialized output of the created Agent.
        """
        try:
            serializer = CreateAgentInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.usecase.execute(**request.data)
            response = AgentOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class UpdateAgentApi(APIView):
    """
    API endpoint for updating an Agent.

    This endpoint accepts input data via the `PATCH` method, validates it, and updates an existing Agent
    identified by its ID using the `UpdateAgentUseCase`. The response includes the updated Agent details.
    """

    def __init__(self, **kwargs):
        """
        Initializes the UpdateAgentApi with a dependency on UpdateAgentUseCase.
        """
        super(UpdateAgentApi, self).__init__(**kwargs)
        self.usecase = UpdateAgentUseCase()

    @extend_schema(request=UpdateAgentInputSerializer, responses=AgentOutputSerializer, tags=['Agent'])
    def patch(self, request, agent_id):
        """
        Handles the PATCH request to update an Agent.

        Validates the request data using `UpdateAgentInputSerializer` and calls the use case to update the
        Agent identified by `agent_id`. Returns the serialized output of the updated Agent.
        """
        try:
            serializer = UpdateAgentInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.usecase.execute(pk=agent_id, updates=serializer.validated_data)
            response = AgentOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class DeleteAgentApi(APIView):
    """
    API endpoint for deleting an Agent.

    This endpoint handles the deletion of an Agent identified by its ID using the `DeleteAgentUseCase`.
    """

    def __init__(self, **kwargs):
        """
        Initializes the DeleteAgentApi with a dependency on DeleteAgentUseCase.
        """
        super(DeleteAgentApi, self).__init__(**kwargs)
        self.usecase = DeleteAgentUseCase()

    @extend_schema(request=UpdateAgentInputSerializer, responses=AgentOutputSerializer, tags=['Agent'])
    def delete(self, request, agent_id: int):
        """
        Handles the DELETE request to remove an Agent.

        Deletes the Agent identified by `agent_id` and returns a success message upon completion.
        """
        try:
            self.usecase.execute(pk=agent_id)
            return MessageResponse("Agent successfully deleted.")
        except Exception as exception:
            return ErrorResponse(exception=exception)


class GetAgentApi(APIView):
    """
    API endpoint for retrieving an Agent's details.

    This endpoint fetches the details of an Agent identified by its ID using the `GetAgentUseCase`.
    """

    def __init__(self, **kwargs):
        """
        Initializes the GetAgentApi with a dependency on GetAgentUseCase.
        """
        super(GetAgentApi, self).__init__(**kwargs)
        self.usecase = GetAgentUseCase()

    @extend_schema(responses=AgentOutputSerializer, tags=['Agent'])
    def get(self, request, agent_id: int):
        """
        Handles the GET request to retrieve an Agent's details.

        Fetches the details of the Agent identified by `agent_id` and returns the serialized output.
        """
        try:
            instance = self.usecase.execute(pk=agent_id)
            response = AgentOutputSerializer(instance=instance, context={'request': request}).data
            return Response(response)
        except Exception as exception:
            return ErrorResponse(exception=exception)


class SearchAgentApi(APIView):
    """
    API endpoint for searching Agents.

    This endpoint allows searching for Agents based on query parameters using the `SearchAgentUseCase`.
    """

    def __init__(self, **kwargs):
        """
        Initializes the SearchAgentApi with a dependency on SearchAgentUseCase.
        """
        super(SearchAgentApi, self).__init__(**kwargs)
        self.usecase = SearchAgentUseCase()

    @extend_schema(parameters=[SearchAgentInputSerializer], responses=SearchAgentOutputSerializer, tags=['Agent'])
    def get(self, request):
        """
        Handles the GET request to search for Agents.

        Validates the query parameters using `SearchAgentInputSerializer` and calls the use case to perform the
        search. Returns a list of serialized Agent details matching the search criteria.
        """
        try:
            serializer = SearchAgentInputSerializer(data=request.query_params.dict())
            serializer.is_valid(raise_exception=True)

            result = self.usecase.execute(**serializer.validated_data)

            response_serializer = SearchAgentOutputSerializer(data=result, context={'request': request}, many=True)
            response_serializer.is_valid(raise_exception=True)

            return Response(response_serializer.validated_data)
        except Exception as exception:
            return ErrorResponse(exception=exception)
