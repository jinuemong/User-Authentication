from django.urls import path,include
from .views import RegistrationAPIView,LoginAPIView,UserRetrieveUpdateAPIView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router_user = DefaultRouter()
# router_user.register('register',RegistrationAPIView)
# router_user.register('login',LoginAPIView)
# router_user.register('current',RegistrationAPIView)
urlpatterns = [
    path('register/',RegistrationAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('current/',UserRetrieveUpdateAPIView.as_view()),
    path('',include(router_user.urls)),

    # for token
    path("auth/refresh/",TokenRefreshView.as_view()),
    path("auth/token/",TokenObtainPairView.as_view())
]
