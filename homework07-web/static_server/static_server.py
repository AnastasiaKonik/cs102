import mimetypes
import os
import pathlib
import re
import typing as tp
from datetime import datetime
from urllib.parse import urlparse

import url_normalize as un

from httpserver.httpserver import (
    BaseHTTPRequestHandler,
    BaseRequestHandler,
    HTTPRequest,
    HTTPResponse,
    HTTPServer,
)


def url_normalize(path: str) -> str:
    normalized_url = un.url_normalize(path)
    normalized_url = re.sub(r"%20", " ", normalized_url)
    return normalized_url


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_request(self, request: HTTPRequest, **kwargs) -> HTTPResponse:
        # NOTE: https://tools.ietf.org/html/rfc3986
        # NOTE: echo -n "GET / HTTP/1.0\r\n\r\n" | nc localhost 5000
        content: bytes = b""
        status: int = 200
        headers: tp.Dict[str, str] = dict()
        content_type: tp.Optional[str] = "text/html"

        if request.method not in [b"GET", b"HEAD"]:
            content = b"No methods available"
            status = 405
            headers = {
                "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "Server": "Custom HTTP Server",
                "Content-Length": str(len(content)),
                "Content-Type": "text/plain",
                "Allow": "GET, HEAD",
            }
        else:
            url = request.url.decode(encoding="utf-8")
            parsed_url = urlparse(url_normalize(url))
            url_path = parsed_url.path + "index.html" if parsed_url.path == "/" else parsed_url.path
            path = pathlib.Path(str(server.document_root.absolute()) + url_path)  # type: ignore
            if os.path.exists(path) and os.path.isfile(path):
                try:
                    if request.method == b"GET":
                        with open(path, "rb") as f:
                            content = f.read()
                        content_type, _ = mimetypes.guess_type(url)
                except OSError:
                    status = 404
                    print("Invalid file requested: OSError", parsed_url.path)
                except Exception as e:
                    status = 500
                    print("Unexpected error:", e)
            else:
                status = 404
                if not os.path.exists(path):
                    print("Invalid path requested: File not found", path)
                else:
                    print("Invalid path requested: Is not a file", path)

            headers = {
                "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "Server": "Custom HTTP Server",
                "Content-Length": str(len(content)),
                "Content-Type": "text/html" if content_type is None else content_type,
            }

            if request.method == b"HEAD":
                content = b""
        response = self.response_klass(status=status, headers=headers, body=content)
        return response


class StaticServer(HTTPServer):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
        document_root: pathlib.Path = pathlib.Path("static").absolute() / "root",
    ) -> None:
        super().__init__(host, port, backlog_size, max_workers, timeout, request_handler_cls)
        self.document_root = document_root


if __name__ == "__main__":
    url_normalize("https://www.example.com/~user/with space/index.html?a=1&b=2")
    document_root_path = pathlib.Path("static").absolute() / "root"
    server = StaticServer(
        timeout=4,
        document_root=document_root_path,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
