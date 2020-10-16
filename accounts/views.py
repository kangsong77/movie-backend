from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .serializers import UserCreateSerializer
from .models import User
from .serializers import UserLoginSerializer
# DRF(Django Rest Framework) 에서 제공해주는 API 제너릭 뷰 참조
from rest_framework import generics

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

# class FavoriteView(generics.ListAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer

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

#     def get(self, request, format=None):
#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)


# class UserView(generics.ListAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         queryset = User.objects.all()
#         id = self.request.user.id
#         return User.objects.filter(id=id)