from django.urls import path

from . import views

urlpatterns = [
    path("", views.NotificationCreatAPIView.as_view()),
    path("lists/", views.NotificationListAllAPIView.as_view()),
    path("<int:pk>/", views.NotificationDetailAPIView.as_view()),
    path("update/<int:pk>/",views.NotificationUpdateAPIView.as_view()),
    path("delete/<int:pk>/",views.NotificationDestroyAPIView.as_view()),
    path("test/",views.NotificationTestAPIView.as_view()),
]