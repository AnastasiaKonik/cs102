import dataclasses
import sys
import io
import typing as tp
from urllib.parse import urlparse

from httpserver import HTTPRequest


@dataclasses.dataclass
class WSGIRequest(HTTPRequest):
    def to_environ(self) -> tp.Dict[str, tp.Any]:
        query_str = urlparse(HTTPRequest.url).query
        path = urlparse(HTTPRequest.url).path
        environ = {
            'REQUEST_METHOD': self.method.decode(),
            'SCRIPT_NAME': '',
            'PATH_INFO': path.decode(),
            'QUERY_STRING': query_str.decode(),
            'CONTENT_TYPE': self.headers.get(b"Content-Type", b"").decode(),
            'CONTENT_LENGTH': self.headers.get(b"Content-Length", b"").decode(),
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': io.BytesIO(self.body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': True,
            'wsgi.multiprocess': False,
            'wsgi.run_once': True
        }

        for header in self.headers:
            environ["HTTP_" + header.decode().upper()] = self.headers[header].decode()

        return environ
