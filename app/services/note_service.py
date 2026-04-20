
from app.models.note_model import Note
from app.core.exceptions import NoteNotFound, InternalError
from app.dto.note_dto import NoteCreate
from app.repositories.note_repo import NoteRepository

class NoteService:
    def __init__(self, repo: NoteRepository):
        self.repo = repo

    def get_notes(self):
        try:  
            notes_data = self.repo.get_all()
            return notes_data
        except:
            raise InternalError()


    def get_note_by_id(self, note_id: int):
        note = self.repo.get_by_id(note_id)
        if not note: 
            raise NoteNotFound("Note not found with that ID")
        return note

    def create_note(self, new_note: NoteCreate, user_id: int):
        note = Note.model_validate(new_note, update={"user_id": user_id})
        note_db = self.repo.create(note)
        return note_db

    def delete_note(self, note_id: int):
        db_note = self.repo.get_by_id(note_id)
        if not db_note:
            raise NoteNotFound("Note not found with that ID")
        is_deleted = self.repo.delete(db_note)
        return is_deleted

    def update_note(self, note_id:int, updated_note: int):
        db_note = self.repo.get_by_id(note_id)
        if not db_note:
            raise NoteNotFound("Note not found with that ID")
        return self.repo.update(db_note, updated_note)