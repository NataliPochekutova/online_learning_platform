from django.urls import path
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentListAPIView, UserCreateAPIView,
                         UserDestroyApiView, UserListApiView,
                         UserRetrieveApiView, UserUpdateApiView, UserViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("users", UserListApiView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserRetrieveApiView.as_view(), name="user_retrieve"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("users/<int:pk>/update/", UserUpdateApiView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", UserDestroyApiView.as_view(), name="user_delete"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
