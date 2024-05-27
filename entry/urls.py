from django.urls import path

from . import views
from .views import SearchResultsView

app_name = "entries"

urlpatterns = [
    path("create/", views.index, name="create"),
    path("post/", views.submit_entry, name="post"),
    path("/<str:title>/", views.read_entry, name="read"),
    path("/random/", views.random_entry, name="random"),
    path("/update/", views.edit_entry, name="edit"),
    path("/search/<str:title>/", views.subQuery, name="search_results")
]
