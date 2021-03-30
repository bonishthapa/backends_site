from django.urls import path,include
from rest_framework.routers import DefaultRouter
from backendapp import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()

router.register('maintitle', views.MaintitleApi, basename='maintitle')
router.register('subtitle', views.SubtitleApi, basename='subtitle')


urlpatterns = [
    path('api/',include(router.urls)),
    path('api/register', views.RegisterAPIView.as_view()),
    path('email-verify',views.Verify_Email.as_view(),name='email-verify'),
    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
