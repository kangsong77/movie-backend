# DRF(Django Rest Framework) 에서 제공해주는 API 제너릭 뷰 참조
from rest_framework import generics
from .serializers import NowMovieListSerializer
from .serializers import IntroMovieTodaySerializer
from .serializers import MovieDetailSerializer
from .serializers import MovieCastSerializer
from django.shortcuts import render
from movie.models import NowMovie, MovieDetail, SimulaMovie, MovieGallery, MovieCast
from movie.models import IntroMovie
from django.views.generic import TemplateView
import requests
from datetime import datetime

from movie.key import API_KEY, API_KEY_GALLERY
from random import *

BACKDROP_PATH = 'https://image.tmdb.org/t/p/original'
POSTER_PATH = 'https://image.tmdb.org/t/p/w500'
IMG_EMPTY = 'https://ssl.pstatic.net/static/movie/2012/06/dft_img77x96_1.png'
BASE_URL = 'https://api.themoviedb.org/3/movie/'

INTRO_URL = 'https://api.themoviedb.org/3/trending/movie/week'


# class MovieCastView(generics.ListCreateAPIView):
#     queryset = MovieCast.objects.all()
#     serializer_class = MovieCastSerializer


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieDetail.objects.all()
    serializer_class = MovieDetailSerializer


class NowMovieList(generics.ListCreateAPIView):
    today = datetime.today().strftime("%Y%m%d")
    # ORM 을 이용해 데이터를 모델에 담아 조회한다.
    queryset = NowMovie.objects.filter(create_date=today)

    # 모델에 담긴 조회결과를 하기 설정한 직렬화 클래스를 통해 JSON포맷으로 변환한다.
    serializer_class = NowMovieListSerializer


class IntroMovieToday(generics.ListCreateAPIView):
    today = datetime.today().strftime("%Y%m%d")
    q = IntroMovie.objects.filter(create_date=today)

    if q.count() > 0:
        key = randint(0, q.count()-1)  # 1부터 100 사이의 임의의 정수
        # print("IntroMovieToday" + str(key))
        todayid = q[key].id
        queryset = IntroMovie.objects.filter(pk=todayid)
        # 모델에 담긴 조회결과를 하기 설정한 직렬화 클래스를 통해 JSON포맷으로 변환한다.
        serializer_class = IntroMovieTodaySerializer


class savedbView(TemplateView):
    template_name = 'movie/savedb.html'


def setMovieGallery(tmdbid, detail):

    url = BASE_URL + str(tmdbid) + '/images' + API_KEY_GALLERY
    response = requests.get(url)
    # 응답 실패시 리턴
    if(response.status_code != 200):
        return
    # json 결과
    data = response.json()

    for m in data['backdrops']:
        MovieGallery(tmdb_id=detail, backdrop_path=(
            BACKDROP_PATH+m['file_path'])).save()


def setSimilar(tmdbid, detail):
    url = BASE_URL + str(tmdbid) + '/similar' + API_KEY
    response = requests.get(url)
    # 응답 실패시 리턴
    if(response.status_code != 200):
        return
    # json 결과
    data = response.json()
    count = 0
    for m in data['results']:
        if(count > 9):
            break
        count += 1
        print("setSimilar: " + str(m['id']))
        img_path = ""
        if(m['backdrop_path']):
            SimulaMovie(simula_id=m['id'], title=m['title'],
                        backdrop_path=(POSTER_PATH + m['backdrop_path']),
                        tmdb_id=detail).save()
            # 영화 상세정보 저장
            setMovieDetail(m['id'])


def setMovieCast(tmdbid, detail):
    url = BASE_URL + str(tmdbid) + '/credits' + API_KEY
    response = requests.get(url)
    # 응답 실패시 리턴
    if(response.status_code != 200):
        return
    # json 결과
    data = response.json()
    profilePath = ""
    count = 0
    for m in data['cast']:
        if(count > 14):
            break
        count += 1

        if (m['profile_path']):
            profilePath = POSTER_PATH + m['profile_path']
        else:
            profilePath = IMG_EMPTY

        # print("m['character']: "+m['character'])
        # MovieCast(cast_name=m['name'], cast_role="",
        #           cast_image=profilePath, tmdb_id=detail).save()

        MovieCast(cast_name=m['name'], cast_role=m['character'],
                  cast_image=profilePath, tmdb_id=detail).save()


def setMovieDetail(tmdbid):
    if not MovieDetail.objects.filter(tm_id=tmdbid):
        url_detail = BASE_URL + str(tmdbid) + API_KEY
        response_detail = requests.get(url_detail)
        # 응답 실패시 리턴
        if(response_detail.status_code != 200):
            return
        # json 결과
        m = response_detail.json()
        genreList = ""
        for genre in m['genres']:
            genreList = genreList + '|' + genre['name']
        genreList = genreList[1:]

        backdropPath = ""
        if (m['backdrop_path']):
            backdropPath = BACKDROP_PATH + m['backdrop_path']
        else:
            backdropPath = IMG_EMPTY

        posterPath = ""
        if (m['poster_path']):
            posterPath = POSTER_PATH + m['poster_path']
        else:
            posterPath = IMG_EMPTY

        detail = MovieDetail(tm_id=m['id'], title=m['title'], backdrop_path=backdropPath,
                             overview=m['overview'], tagline=m['tagline'], release_date=m[
            'release_date'], runtime=m['runtime'], rating=m['vote_average'],
            genre=genreList, poster=posterPath)
        detail.save()

        # 영화갤러리 저장
        setMovieGallery(m['id'], detail)
        # 비슷한 영화정보 저장
        setSimilar(m['id'], detail)
        # 배우 정보 저장
        setMovieCast(m['id'], detail)


def setIntroMovie():
    today = datetime.today().strftime("%Y%m%d")
    # 주간 트렌딩 영화
    url = BASE_URL+'popular' + API_KEY
    response = requests.get(url)

    if(response.status_code == 200):
        data = response.json()
        movielist = data['results']

        for m in movielist:
            if (m['overview']):
                if not IntroMovie.objects.filter(tm_id=m['id'], create_date=today):
                    IntroMovie(tm_id=m['id'], title=m['title'], backdrop_path=(BACKDROP_PATH+m['backdrop_path']),
                               overview=m['overview'], create_date=today).save()

                # 영화 상세정보 저장
                setMovieDetail(m['id'])


def savedb(request):
    setIntroMovie()
    today = datetime.today().strftime("%Y%m%d")

    # q = NowMovie.objects.filter(create_date=today)

    # if (q.count()):
    #     return render(request, 'movie/result.html', {'result': "오늘DB가 이미 있습니다."})
    # 인기도 순 현재 상영영화 url
    url = BASE_URL+'popular' + API_KEY
    response = requests.get(url)

    # 응답 실패시 에러코드 페이지로 넘어가기
    if(response.status_code != 200):
        return render(request, 'movie/result.html', {'result': "DB적용실패!!", 'error_message': response.status_code})
    # json 결과
    data = response.json()
    popular = data['results']
    for p in popular:
        if not NowMovie.objects.filter(tm_id=p['id'], create_date=today):
            NowMovie(tm_id=p['id'], title=p['title'], backdrop_path=(BACKDROP_PATH+p['backdrop_path']),
                     rating=p['vote_average'], release_date=p['release_date'], overview=p['overview'],
                     create_date=today).save()

        # 영화 상세정보 저장
        setMovieDetail(p['id'])

    return render(request, 'movie/result.html', {'result': "DB적용완료"})
