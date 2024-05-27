from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("create", views.index, name="create"),
    path("post", views.submit_entry, name="post"),
    path("read/<str:title>/", views.read_entry, name="read")
]
