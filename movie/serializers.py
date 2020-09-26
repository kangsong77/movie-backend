from rest_framework import serializers
from .models import NowMovie, IntroMovie, MovieDetail, MovieGallery, MovieCast, SimulaMovie


class NowMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NowMovie
        fields = ['tm_id', 'title', 'backdrop_path',
                  'rating', 'release_date', 'overview']


class IntroMovieTodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroMovie
        fields = ['tm_id', 'title', 'backdrop_path', 'overview']


class MovieGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGallery
        fields = ['backdrop_path']


class MovieCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCast
        fields = ['cast_name', 'cast_role', 'cast_image']


class SimulaMovieSerializer (serializers.ModelSerializer):
    class Meta:
        model = SimulaMovie
        fields = ['simula_id', 'title', 'backdrop_path']


class DetailMovieSerializer(serializers.ModelSerializer):
    cast = MovieCastSerializer(many=True, read_only=True)
    gallery = MovieGallerySerializer(many=True, read_only=True)
    simula = SimulaMovieSerializer(many=True, read_only=True)

    class Meta:
        model = MovieDetail
        fields = ['tm_id', 'title', 'backdrop_path', 'overview', 'tagline', 'release_date',
                  'runtime', 'rating', 'genre', 'poster', 'cast', 'gallery', 'simula']
