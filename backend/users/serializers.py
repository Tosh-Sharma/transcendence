from rest_framework import serializers
from .models import Game, User, PlayerSettings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'password', 'profile_photo']
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be returned
            'profile_photo': {'required': False},  # Avatar is optional
        }

    def create(self, validated_data):
        # Create user and hash the password
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Handle password hashing on update
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)

class GameSerializer(serializers.ModelSerializer):
    player1_username = serializers.CharField(source='player1.username', read_only=True)
    player2_username = serializers.CharField(source='player2.username', read_only=True)

    class Meta:
        model = Game
        fields = [
            'id', 'player1', 'player1_username', 'player2', 'player2_username',
            'score1', 'score2', 'is_tournament'
        ]

    def validate(self, data):
        # Ensure player1 and player2 are not the same
        if data['player1'] == data['player2']:
            raise serializers.ValidationError("Player1 and Player2 must be different users.")
        return data

class PlayerSettingsSerializer(serializers.ModelSerializer):
    player_username = serializers.CharField(source='player.username', read_only=True)

    class Meta:
        model = PlayerSettings
        fields = ['id', 'player', 'player_username', 'background_color', 'paddle_color']

    def validate(self, data):
        # Add any custom validation if required
        return data