from django.shortcuts import render

# DRF(Django Rest Framework) 에서 제공해주는 API 제너릭 뷰 참조
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# 전체 예약목록 데이터 제공 API 서비스 뷰
# ListCreateAPIView는 get/여러건조회 API 및 post api 2개를 동시에 제공한다.
# api/bookings-get방식 조회리턴, api/booking -post
class PostList(generics.ListCreateAPIView):
    # ORM 을 이용해 데이터를 모델에 담아 조회한다.
    queryset = Post.objects.all()

    # 모델에 담긴 조회결과를 하기 설정한 직렬화 클래스를 통해 JSON포맷으로 변환한다.
    serializer_class = PostSerializer


# 단일예약정보 조회/수정/삭제 OPEN API 서비스 제공 API 뷰
class PostDetail(generics.RetrieveUpdateDestroyAPIView):

    # 인증방식을 결정합니다- 토큰인증 방식적용
    #authentication_classes = (TokenAuthentication,)

    # 인증방식 적용여부- 인증된 사용자만이 API를 호출할수 있게한다.
    #permission_classes = (IsAuthenticated,)

    queryset = Post.objects.all()
    serializer_class = PostSerializer
