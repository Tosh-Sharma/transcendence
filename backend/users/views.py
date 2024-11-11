from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Game, User, PlayerSettings
from .serializers import UserSerializer, GameSerializer, PlayerSettingsSerializer

class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet to handle user operations.
    """

    @extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        description="POST endpoint to create a new user.",
        examples=[
            OpenApiExample(
                'Example 1',
                summary='Create User Example',
                description='Example of creating a user',
                value={
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'password': 'password123'
                }
            )
        ]
    )
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        description="PUT endpoint to update user details."
    )
    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={204: OpenApiExample('User deleted successfully')},
        description="DELETE endpoint to delete a user."
    )
    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses={200: OpenApiExample('Password is correct'), 401: OpenApiExample('Password is incorrect')},
        description="POST endpoint to verify if the provided password is correct.",
        examples=[
            OpenApiExample(
                'Example 1',
                summary='Verify Password Example',
                description='Example of verifying a password',
                value={
                    'username': 'john_doe',
                    'password': 'password123'
                }
            )
        ]
    )
    @action(detail=False, methods=['post'], url_path='verify-password')
    def verify_password(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = get_object_or_404(User, username=username)
        if user.check_password(password):
            return Response({"message": "Password is correct"}, status=status.HTTP_200_OK)
        return Response({"message": "Password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        parameters=[OpenApiParameter(name='uuid', description='UUID of the user', required=True, type=str)],
        responses=UserSerializer,
        description="GET endpoint to get user details by UUID."
    )
    @action(detail=False, methods=['get'], url_path='details-by-uuid/(?P<uuid>[^/.]+)')
    def details_by_uuid(self, request, uuid=None):
        user = get_object_or_404(User, uuid=uuid)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[OpenApiParameter(name='username', description='Username of the user', required=True, type=str)],
        responses=UserSerializer,
        description="GET endpoint to get user details by username."
    )
    @action(detail=False, methods=['get'], url_path='details-by-username/(?P<username>[^/.]+)')
    def details_by_username(self, request, username=None):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GameViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing game data.
    """

    @extend_schema(
        request=GameSerializer,
        responses=GameSerializer,
        description="POST endpoint to create a new game record.",
        examples=[
            OpenApiExample(
                'Example 1',
                summary='Create Game Example',
                description='Example of creating a game',
                value={
                    'player1': 'uuid-of-player1',
                    'player2': 'uuid-of-player2',
                    'score1': 10,
                    'score2': 8,
                    'is_tournament': False
                }
            )
        ]
    )
    def create(self, request):
        serializer = GameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[OpenApiParameter(name='uuid', description='UUID of the player', required=True, type=str)],
        responses=GameSerializer(many=True),
        description="GET endpoint to retrieve all games for a given player UUID."
    )
    @action(detail=False, methods=['get'], url_path='all-by-player/(?P<uuid>[^/.]+)')
    def get_all_by_player(self, request, uuid=None):
        player = get_object_or_404(User, id=uuid)
        games_as_player1 = Game.objects.filter(player1=player)
        games_as_player2 = Game.objects.filter(player2=player)
        games = games_as_player1.union(games_as_player2)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlayerSettingsViewSet(viewsets.ViewSet):
    """
    A ViewSet to manage player settings.
    """

    @extend_schema(
        request=PlayerSettingsSerializer,
        responses=PlayerSettingsSerializer,
        description="POST endpoint to create a new settings record.",
        examples=[
            OpenApiExample(
                'Example 1',
                summary='Create Player Settings Example',
                description='Example of creating player settings',
                value={
                    'player': 'uuid-of-player',
                    'background_color': 'blue',
                    'paddle_color': 'red'
                }
            )
        ]
    )
    def create(self, request):
        serializer = PlayerSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses=PlayerSettingsSerializer(many=True),
        description="GET endpoint to list all player settings."
    )
    def list(self, request):
        settings = PlayerSettings.objects.all()
        serializer = PlayerSettingsSerializer(settings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[OpenApiParameter(name='uuid', description='UUID of the player', required=True, type=str)],
        responses=PlayerSettingsSerializer(many=True),
        description="GET endpoint to retrieve settings for a specific player by UUID."
    )
    @action(detail=False, methods=['get'], url_path='by-player/(?P<uuid>[^/.]+)')
    def get_by_player(self, request, uuid=None):
        player = get_object_or_404(User, id=uuid)
        settings = PlayerSettings.objects.filter(player=player)
        serializer = PlayerSettingsSerializer(settings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)