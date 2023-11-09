"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from api.views import (
    UserListApiView,
    UserDetailApiView,
    UserLoginApiView,
    UsernameApiView,
    LettersListApiView,
    LetterUserListApiView,
    LetterDetailApiView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Api
    # Api auth
    path("api-auth/", include("rest_framework.urls")),
    # User route
    ## User
    path("api/user", UserListApiView.as_view()),
    path("api/user/", UserListApiView.as_view()),
    ## Detail
    path("api/user/detail/<str:token>", UserDetailApiView.as_view()),
    path("api/user/detail/<str:token>/", UserDetailApiView.as_view()),
    ## Login
    path("api/user/login", UserLoginApiView.as_view()),
    path("api/user/login/", UserLoginApiView.as_view()),
    ## Username
    path("api/user/username/<str:username>", UsernameApiView.as_view()),
    path("api/user/username/<str:username>/", UsernameApiView.as_view()),
    # Letter route
    ## Letter
    path("api/letter", LettersListApiView.as_view()),
    path("api/letter/", LettersListApiView.as_view()),
    ## Detail
    path("api/letter/detail/<str:letter_token>", LetterDetailApiView.as_view()),
    path("api/letter/detail/<str:letter_token>/", LetterDetailApiView.as_view()),
    ## User
    path("api/letter/user", LetterUserListApiView.as_view()),
    path("api/letter/user/", LetterUserListApiView.as_view()),
]
