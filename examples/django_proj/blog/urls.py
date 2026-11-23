from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index),
    path("articles/<int:year>/<slug:slug>/", views.article),
    path("search/", views.search),
    path("create/", views.create),
    path("items/<int:pk>/", views.detail),
    path("both/", views.both),
    path("go/", views.go),
    path("notes/", views.Notes.as_view()),
    path("notes/<int:pk>/", views.NoteDetail.as_view()),
    path("agent/", views.agent),
    re_path(r"^archive/(?P<year>[0-9]{4})/$", views.archive),
]
