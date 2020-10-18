from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .serializers import UserCreateSerializer
from .models import User, Favorite
from .serializers import UserLoginSerializer, FavoriteSerializer
from .serializers import UserSerializer
# DRF(Django Rest Framework) 에서 제공해주는 API 제너릭 뷰 참조
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly  # custom permission


# @permission_classes([AllowAny]): IsAuthenticated 설정이 되어 있기 때문에 인증이 필요없는 api이기 때문에
# permission 설정을 따로 부여하였습니다.


@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        if User.objects.filter(email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['email'] == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)

        response = {
            'success': 'True',
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)


class FavoriteList(generics.ListCreateAPIView):
    # queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        queryset = Favorite.objects.all()
        userid = self.request.user.id
        return Favorite.objects.filter(user_id=userid)


class FavoriteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # add permission


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class FavoriteView(ModelViewSet):
# class FavoriteView(generics.ListCreateAPIView):
#     serializer_class = FavoriteSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def get_queryset(self):
#         id = self.request.user.id
#         return Favorite.objects.filter(author=id)

# class FavoriteView(generics.ListAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = [permissions.IsAuthenticated]
#     # serializer_class = FavoriteSerializer

#     # def get_queryset(self):
#     #     queryset = User.objects.all()
#     #     email = self.request.user.email
#     #     return User.objects.filter(id=email)

#     def post(self, request, format=None):
#         serializer = FavoriteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAC_REQUEST)

    # def get(self, request, format=None):
    #     queryset = Favorite.objects.all()
    #     serializer = PostSerializer(queryset, many=True)
    #     return Response(serializer.data)


# 인아님 소스 유저 개인 정보 조회 뷰입니다~
# class UserView(generics.ListAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         queryset = User.objects.all()
#         id = self.request.user.id
#         return User.objects.filter(id=id)
