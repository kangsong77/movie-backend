from django.urls import path
from movie import views

app_name = 'movie'

urlpatterns = [
    # Example: /movie/
    path('now/', views.NowMovieList.as_view()),
    path('intro/', views.IntroMovieToday.as_view()),
    path('<int:pk>', views.MovieDetailView.as_view()),
    # path('cast/', views.MovieCastView.as_view()),

    path('db/', views.savedbView.as_view()),
    path('savedb/', views.savedb, name='savedb'),
    # path('now/', views.NowMovieList.as_view()),
]
