import socket
import threading
import typing as tp

from httpserver.httpserver.handlers import BaseRequestHandler


class TCPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.server_address = (host, port)
        # @see: https://stackoverflow.com/questions/36594400/what-is-backlog-in-tcp-connections
        self.backlog_size = backlog_size
        self.request_handler_cls = request_handler_cls
        self.max_workers = max_workers
        self.timeout = timeout
        self._threads: tp.List[threading.Thread] = []

    def serve_forever(self) -> None:
        # @see: http://veithen.io/2014/01/01/how-tcp-backlog-works-in-linux.html
        # @see: https://en.wikipedia.org/wiki/Thundering_herd_problem
        # @see: https://stackoverflow.com/questions/17630416/calling-accept-from-multiple-threads

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.backlog_size)

        print(f"Server is working on {self.host}:{self.port}")

        for thread in range(self.max_workers + 1):
            self._threads.append(threading.Thread(target=self.handle_accept, args=(server_socket,)))
            self._threads[thread].start()

        try:
            for i in self._threads:
                i.join()
        except KeyboardInterrupt:
            print("Stopped")
            server_socket.close()

    def handle_accept(self, server_socket: socket.socket) -> None:
        while True:
            client_socket, client_address = server_socket.accept()
            client_socket.settimeout(self.timeout)
            handler = self.request_handler_cls(client_socket, client_address, self)
            print(f"New connection from {client_socket}")
            handler.handle()


class HTTPServer(TCPServer):
    pass
