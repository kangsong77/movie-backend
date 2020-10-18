
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.authtoken import views
from movie.views import savedbView

schema_view = get_schema_view(
    openapi.Info(
        title="My Site OPEN API 명세서",
        default_version='v1',
        description="영화 어플리케이션 관리 OPEN API 입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', savedbView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    # 사용자 아이디와 암호를 전달받아 토큰을 발급해주는 레스트프레임워크 기능
    # path('api/get_token/', views.obtain_auth_token),
    path('accounts/', include('accounts.urls')),
    path('movie/', include('movie.urls')),
    path('blog/', include('blog.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
