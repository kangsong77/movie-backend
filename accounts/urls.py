from django.urls import path
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
from . import views

urlpatterns = [

    path("token/", obtain_jwt_token),
    path("token/refresh/", refresh_jwt_token),
    path("token/verify/", verify_jwt_token),

    path('signup/', views.createUser),
    path('login/', views.login),
    path('favorite/', views.FavoriteList.as_view()),
    path('favorite/<int:pk>/', views.FavoriteDetail.as_view()),

]
