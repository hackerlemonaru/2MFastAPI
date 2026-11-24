from django.urls import path, include

urlpatterns = [
    path("", include("blog.urls")),
    path("v2/", include("blog.urls")),
]
