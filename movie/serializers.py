from rest_framework import serializers
from .models import NowMovie, MovieDetail, MovieGallery, MovieCast, SimulaMovie
# ksong
from .models import MovieIntro


class NowMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NowMovie
        fields = ['tm_id', 'title', 'backdrop_path','rating', 'release_date', 'overview']


# ksong
class MovieIntroListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieIntro
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


class MovieDetailSerializer(serializers.ModelSerializer):
    cast = MovieCastSerializer(many=True, read_only=True)
    gallery = MovieGallerySerializer(many=True, read_only=True)
    simula = SimulaMovieSerializer(many=True, read_only=True)

    class Meta:
        model = MovieDetail
        # fields = ['tm_id', 'title', 'backdrop_path', 'overview', 'tagline', 'release_date',
        #           'runtime', 'rating', 'genre', 'poster', 'cast', 'gallery', 'simula']
        fields = ['tm_id', 'title', 'backdrop_path', 'overview', 'tagline', 'release_date',
                  'runtime', 'rating', 'genre', 'poster', 'cast', 'gallery', 'simula']
