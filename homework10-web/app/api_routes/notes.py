from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from app import app
from app.models import Note, User
from app.services.auth import get_current_user


class NoteModel(BaseModel):
    text: str


@app.put("/note/")
async def add_note(note: NoteModel, current_user: User = Depends(get_current_user)):
    return (await Note.create(text=note.text, author=current_user)).to_dict()


@app.get("/note/{note_id}")
async def get_note_by_id(note_id: int, current_user: User = Depends(get_current_user)):
    note = await Note.filter(author=current_user, id=note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note with that id not found",
        )
    return note.to_dict()


@app.patch("/note/{note_id}")
async def edit_note(
    note_id: int, note: NoteModel, current_user: User = Depends(get_current_user)
):
    note_db = await Note.filter(id=note_id, author=current_user).first()
    if not note_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note with that id not found",
        )
    note_db.text = note.text  # type:ignore
    await note_db.save()
    return note_db.to_dict()


@app.get("/note")
async def get_list_notes(current_user: User = Depends(get_current_user)):
    return [i.to_dict() for i in await Note.filter(author=current_user)]


@app.delete("/note/{note_id}")
async def delete_note(note_id: int, current_user: User = Depends(get_current_user)):
    await Note.filter(id=note_id, author=current_user).delete()
