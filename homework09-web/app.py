import datetime as dt
import typing as tp

import jwt

from slowapi import JsonResponse, Request, Response, SlowAPI
from slowapi.middlewares import CORSMiddleware

app = SlowAPI()
notes: tp.Dict[int, tp.Dict[str, tp.Any]] = {}
users: tp.Set[str] = set()

JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 300


def dt_json_serializer(o: tp.Any):
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()


@app.post("/api/jwt-auth/")
def login(request: Request) -> Response:
    user_data = request.json()
    if user_data is None:
        return Response(400, body="Bad request")

    users.add(user_data["email"])
    payload = {
        "email": user_data["email"],
        "exp": dt.datetime.utcnow() + dt.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return JsonResponse(data={"token": jwt_token})


@app.post("/api/notes")
def add_note(request: Request) -> Response:
    note = request.json()
    if note is None:
        return Response(400, body="Bad request")

    note_id = len(notes) + 1
    note["id"] = note_id
    note["pub_date"] = dt.datetime.now()
    notes[note_id] = note
    return JsonResponse(data=note, serializer=dt_json_serializer)


@app.get("/api/notes")
def get_notes(request: Request) -> JsonResponse:
    notes_list = list(notes.values())
    return JsonResponse(data={"notes": notes_list}, serializer=dt_json_serializer)


@app.get("/api/notes/{id:d}")
def get_note(request: Request, id: int) -> JsonResponse:
    note_id = id
    return JsonResponse(data=notes[note_id], serializer=dt_json_serializer)


@app.patch("/api/notes/{id:d}")
def update_note(request: Request, id: int) -> Response:
    note_id = id
    data = request.json()
    if data is None:
        return Response(400, body="Bad request")

    note = notes[note_id]
    note["title"] = data["title"]
    note["body"] = data["body"]
    return JsonResponse(data={})


app.add_middleware(CORSMiddleware)


def main():
    from wsgiserver import WSGIRequestHandler, WSGIServer

    server = WSGIServer(port=8080, request_handler_cls=WSGIRequestHandler)
    server.set_app(app)
    server.serve_forever()


if __name__ == "__main__":
    main()
