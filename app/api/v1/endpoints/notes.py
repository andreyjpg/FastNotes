from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.repositories.note_repo import NoteRepository
from app.services.note_service import NoteService
from app.dto.note_dto import NoteUpdate, NoteCreate
from app.dto.user_dto import UserResponse

from app.core.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_all(db: Session = Depends(get_session), current_user: UserResponse = Depends(get_current_user)):
    repo = NoteRepository(db)
    service = NoteService(repo)
    return service.get_notes(current_user.id)

@router.get("/{note_id}")
async def get_by_id(note_id: int, db: Session = Depends(get_session), current_user: UserResponse = Depends(get_current_user)):
    repo = NoteRepository(db)
    service = NoteService(repo)
    return service.get_note_by_id(note_id, current_user.id)

@router.post("/create_note")
async def create_note(body: NoteCreate, db: Session = Depends(get_session), current_user: UserResponse = Depends(get_current_user)):
    repo = NoteRepository(db)
    service = NoteService(repo)
    return service.create_note(body, current_user.id)

@router.put("/{note_id}")
async def update_node(note_id: int, body: NoteUpdate,db: Session = Depends(get_session), current_user: UserResponse = Depends(get_current_user)):
    repo = NoteRepository(db)
    service = NoteService(repo)
    return service.update_note(note_id, body, current_user.id)


@router.delete("/delete/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_session), current_user: UserResponse = Depends(get_current_user)):
    repo = NoteRepository(db)
    service = NoteService(repo)
    return service.delete_note(note_id, current_user.id)

@router.post("/prioritize")
async def prioritize(db: Session = Depends(get_session), current_user: UserResponse = Depends(get_current_user)):
    repo = NoteRepository(db)
    service = NoteService(repo)
    return service.generate_propmt(current_user.id)
