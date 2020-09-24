from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    # Example: /blog/
    path('', views.PostList.as_view()),

    # Example: /blog/post/ (same as /blog/)
    path('<int:pk>/', views.PostDetail.as_view()),

]
