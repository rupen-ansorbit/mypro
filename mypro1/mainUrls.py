from django.urls import path,include
from mypro1.urls.userUrls import userUrlpatterns
from mypro1.urls.taskUrls import taskUrlpatterns

urlpatterns = [
  path("user/", include(userUrlpatterns)),
  path("task/", include(taskUrlpatterns))
] 