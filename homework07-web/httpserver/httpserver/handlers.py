from __future__ import annotations

import socket
import typing as tp

from httptools import (
    HttpParserCallbackError,
    HttpParserError,
    HttpParserInvalidMethodError,
    HttpParserInvalidStatusError,
    HttpParserInvalidURLError,
    HttpParserUpgrade,
    HttpRequestParser,
)

from httpserver.httpserver import request, response

if tp.TYPE_CHECKING:
    from .server import TCPServer

Address = tp.Tuple[str, int]


class BaseRequestHandler:
    def __init__(self, socket: socket.socket, address: Address, server: TCPServer) -> None:
        self.socket = socket
        self.address = address
        self.server = server

    def handle(self) -> None:
        self.close()

    def close(self) -> None:
        self.socket.close()


class EchoRequestHandler(BaseRequestHandler):
    def handle(self) -> None:
        try:
            data = self.socket.recv(1024)
        except (socket.timeout, BlockingIOError):
            pass
        else:
            self.socket.sendall(data)
        finally:
            self.close()


class BaseHTTPRequestHandler(BaseRequestHandler):
    request_klass = request.HTTPRequest
    response_klass = response.HTTPResponse

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parser = HttpRequestParser(self)

        self._url: bytes = b""
        self._headers: tp.Dict[bytes, bytes] = {}
        self._body: bytes = b""
        self._parsed = False

    def handle(self) -> None:
        request = self.parse_request()
        response = self.response_klass(status=500, headers={}, body=b"")
        if request is not None:
            try:
                response = self.handle_request(request)
            except Exception as e:
                print("Failed to handle request", e)
        else:
            response = self.response_klass(status=400, headers={}, body=b"")
        self.handle_response(response)
        self.close()

    def parse_request(self) -> tp.Optional[request.HTTPRequest]:
        while not self._parsed:
            try:
                data = self.socket.recv(1024)
                if data == b"":
                    break
                self.parser.feed_data(data)
            except socket.timeout:
                print(f"Connection {self.address} timeout")
                break
            except (
                HttpParserError,
                HttpParserCallbackError,
                HttpParserInvalidStatusError,
                HttpParserInvalidMethodError,
                HttpParserInvalidURLError,
                HttpParserUpgrade,
            ) as exc:
                print(f"Parser error {self.address} - {exc}")
                break
        if self._parsed:
            request = self.request_klass(
                method=self.parser.get_method(),
                url=self._url,
                headers=self._headers,
                body=self._body,
            )
            return request
        return None

    @tp.no_type_check
    def handle_request(
        self, request: request.HTTPRequest, status: int = 405
    ) -> response.HTTPResponse:
        return self.response_klass(status=status, headers=request.headers, body=request.body)

    def handle_response(self, response: response.HTTPResponse) -> None:
        self.socket.sendall(response.to_http1())

    def on_url(self, url: bytes) -> None:
        self._url = url
        print("on_url complete", url)

    def on_header(self, name: bytes, value: bytes) -> None:
        self._headers[name] = value
        print("on_header complete", name, value)

    def on_body(self, body: bytes) -> None:
        self._body = body
        print("on_body complete", body)

    def on_message_complete(self) -> None:
        self._parsed = True
        print("on_message_complete complete")
