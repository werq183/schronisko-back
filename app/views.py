from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from app.models import UserProfile
from app.serializers import GroupSerializer, UserSerializer, UserProfileSerializer

# OOTB
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

# OOTB
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]
    
@api_view(['POST'])
def login(request):
    # either bad password or username, return same response
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)

# idk czy potrzebne, wyglada na opcje ponownego otrzymania tokenu np na podstawie sesji, jesli poprzedni wygasl 
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def test_token(request):
    return Response({"success": True, "user": [request.user.username, request.user.pk]})

# the following will create/update profile, regardless if it exists (try - catch)
# @api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# def profile(request):
#     # if exists, update
#     try:
#         user_profile = UserProfile.objects.get(user=request.user)
#         serializer = UserProfileSerializer(user_profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"success": True, "profile": serializer.data})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # if does not exist, create
#     except UserProfile.DoesNotExist:
#         serializer = UserProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response({"success": True, "profile": serializer.data})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'PUT', 'GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    # if exists, update
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "profile": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
    # if does not exist, create
    if request.method == 'PUT':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"success": True, "profile": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if UserProfile.objects.filter(user=request.user).exists():
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# def update_kot(request):
#     return Response("test")

# class UpdateKot(generics.RetrieveUpdateAPIView):
#     queryset = Kot.objects.all()
#     serializer_class = KotSerializer
#     # permission_classes = [permissions.IsAuthenticated]