from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TokenObtainPersonalizadoSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        token['activo'] = user.is_active
        token['email'] = user.email
        token['ultimo login'] = str(user.last_login)
        return token