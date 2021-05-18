import typing as tp

from httpserver import BaseHTTPRequestHandler, HTTPServer

from .request import WSGIRequest
from .response import WSGIResponse

ApplicationType = tp.Any


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: tp.Optional[ApplicationType] = None

    def set_app(self, app: ApplicationType) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[ApplicationType]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        # сформировать словарь с переменными окружения
        # дополнить словарь информацией о сервере
        # вызвать приложение передав ему словарь с переменными окружения и callback'ом
        # ответ приложения представить в виде байтовой строки
        # вернуть объект класса WSGIResponse
        environ = request.to_environ()
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '5000'
        app = self.server.get_app()
        result = app(environ, self.response_klass().start_response)
        response = self.response_klass()
        response.body = b"".join(result)
        print(environ)
        return response
