import traceback
import typing as tp
from http.client import responses as http_responses

from parse import parse

from slowapi.request import Request
from slowapi.response import Response
from slowapi.router import Route


class SlowAPI:
    def __init__(self):
        self.routes: tp.List[Route] = []
        self.middlewares = []

    def __call__(
        self,
        environ: tp.Dict[str, tp.Any],
        start_response: tp.Callable[[str, tp.List[tp.Tuple[str, str]]], None],
    ):
        environ["PATH_INFO"] = environ["PATH_INFO"]
        request = Request(environ)

        response = self.process_request(request)
        start_response(
            str(response.status) + " " + http_responses[response.status],
            [(key, value) for key, value in response.get_headers().items()],
        )

        return [response.body]

    def process_request(self, request: Request) -> Response:
        router, parsed_args = self.get_router(request)

        if router is None or parsed_args is None:
            response = Response(404, body=b"")
        else:
            try:
                response = router.func(request, **parsed_args)
            except Exception as e:
                traceback.print_exc()
                response = Response(500, body=b"")

        return response

    def get_router(
        self, request
    ) -> tp.Tuple[tp.Optional[Route], tp.Optional[tp.Dict[str, tp.Any]]]:
        method, path = request.method, request.path
        for route in self.routes:
            if route.method == method:
                parse_result = parse(route.path, path)
                if parse_result is not None:
                    return route, parse_result.named

        return None, None

    def route(self, path=None, method=None, **options):
        def inner(func):
            self.routes.append(Route(path=path, method=method, func=func))
            return func

        return inner

    def get(self, path=None, **options):
        return self.route(path, method="GET", **options)

    def post(self, path=None, **options):
        return self.route(path, method="POST", **options)

    def patch(self, path=None, **options):
        return self.route(path, method="PATCH", **options)

    def put(self, path=None, **options):
        return self.route(path, method="PUT", **options)

    def delete(self, path=None, **options):
        return self.route(path, method="DELETE", **options)

    def add_middleware(self, middleware) -> None:
        self.middlewares.append(middleware)
