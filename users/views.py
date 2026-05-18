from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)

            return Response({
                "access_token": str(refresh.access_token),  # 🔥 access token
                "refresh_token": str(refresh),              # 🔥 refresh token
                "role": user.role,                          # 🔥 role
                "username": user.username                   # optional (useful)
            })

        return Response({"error": "Invalid credentials"}, status=400)