from django.contrib import admin
from .models import Favorite, User

# 어드민 사이트에 개발자가 추가한 모델을 등록해준다.
admin.site.register(Favorite)
admin.site.register(User)
