from django.http import Http404, JsonResponse
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import exception_handler


def json_exception_handler(exc, context):
    """Единый формат ошибок API: {"error": "<сообщение>", "details": {...}}."""
    response = exception_handler(exc, context)
    if response is None:
        return None  # необработанное исключение -> handler500

    if isinstance(exc, ValidationError):
        response.data = {"error": "Некорректные данные.", "details": response.data}
    elif isinstance(exc, (Http404, NotFound)):
        response.data = {"error": "Задача не найдена."}
    else:
        response.data = {"error": str(response.data.get("detail", response.data))}
    return response


def _json_error(message, status):
    return JsonResponse({"error": message}, status=status, json_dumps_params={"ensure_ascii": False})


def not_found_view(request, exception=None):
    return _json_error("Ресурс не найден.", 404)


def server_error_view(request):
    return _json_error("Внутренняя ошибка сервера.", 500)
