from django.urls import include, path

urlpatterns = [
    path("", include("tasks.urls")),
]

handler404 = "tasks.exceptions.not_found_view"
handler500 = "tasks.exceptions.server_error_view"
