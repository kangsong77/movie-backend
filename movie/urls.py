from django.urls import path
from movie import views

app_name = 'movie'

urlpatterns = [
    # Example: /blog/
    path('', views.savedbView.as_view()),

    path('savedb/', views.savedb, name='savedb')

]
