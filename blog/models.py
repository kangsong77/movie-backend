from django.db import models

# 장고프레임워크의 설정 정보를 참조한다.
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
# 게시글 모델 정의 : Post


class Post(models.Model):
    # verbose_name은 별칭으로 어드민 폼화면에서 라벨명으로 사용
    comment = models.TextField(verbose_name='COMMENT', max_length=200)

    # 글쓴사람
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='OWNER', related_name='posts')
    # 영화별점
    movie_rating = models.CharField(max_length=5)
    # 영화제목
    movie_title = models.CharField(max_length=50)

    # auto_now_add 객체가생성될떄의 시간 일시기록
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)

    # auto_now 객체가 db에 저장될때의 시간 저장
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    # Post 테이블 컬럼외 부수적인 정보 정의시 사용
    # 단수형 별칭과 복수형 별칭 정의
    # 기본테이블명 구조: 앱명_모델클래스명: blog_post
    # 기본 내림차순 컬럼정의:최신 게시글 수정순으로
    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'blog_posts'
        ordering = ('-modify_dt',)

    def __str__(self):
        return self.owner.username+""+self.movie_title

    # url 조회 리턴/reverse를 호출함
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail', args=(self.pk,))

    # 현재 보고있는 게시글 이전 게시글 조회
    def get_previous(self):
        return self.get_previous_by_modify_dt()

    # 현재 보고있는 게시글 다음 게시글 조회
    def get_next(self):
        return self.get_next_by_modify_dt()
