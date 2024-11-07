from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet to handle user operations.
    """

    def create(self, request):
        """
        POST endpoint to create a new user.
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        PUT endpoint to update user details.
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        DELETE endpoint to delete a user.
        """
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='verify-password')
    def verify_password(self, request):
        """
        POST endpoint to verify if the provided password is correct.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = get_object_or_404(User, username=username)
        if user.check_password(password):
            return Response({"message": "Password is correct"}, status=status.HTTP_200_OK)
        return Response({"message": "Password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], url_path='details-by-uuid/(?P<uuid>[^/.]+)')
    def details_by_uuid(self, request, uuid=None):
        """
        GET endpoint to get user details by UUID.
        """
        user = get_object_or_404(User, id=uuid)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='details-by-username/(?P<username>[^/.]+)')
    def details_by_username(self, request, username=None):
        """
        GET endpoint to get user details by username.
        """
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='details-by-email/(?P<email>[^/.]+)')
    def details_by_email(self, request, email=None):
        """
        GET endpoint to get user details by email address.
        """
        user = get_object_or_404(User, email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
