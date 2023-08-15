from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserCreatAPIView.as_view()),
    path("lists/", views.UserListCreatedAPIView.as_view()),
    path("<int:pk>/", views.UserDetailAPIView.as_view()),
    path("update/<int:pk>/",views.UserUpdateAPIView.as_view()),
    path("delete/<int:pk>/",views.UserDestroyAPIView.as_view())
]