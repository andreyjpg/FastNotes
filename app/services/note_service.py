
from app.models.note_model import Note
from app.core.exceptions import NoteNotFound, InternalError
from app.dto.note_dto import NoteCreate, NotePriority
from app.repositories.note_repo import NoteRepository
from app.core.llm import generate_content_via_llm

from fastapi.exceptions import RequestValidationError
import json

GENERAL_PROPMT ='You are an assitant, your role is to analize and assign priorities in the notes you will receive" \
                 According with the description an title of the note list, you will assing a priority like this ("low", "medium", "high)' \
                 'every note need to be priorized \
                 Answer only with the following JSON format and with the exact number of notes you received' \
                 ': [{"id": 1, "priority": "high"},...]'

class NoteService:
    def __init__(self, repo: NoteRepository):
        self.repo = repo

    def get_notes(self, user_id: int):
        notes_data = self.repo.get_all(user_id)
        return notes_data


    def get_note_by_id(self, note_id: int, user_id: int):
        note = self.repo.get_by_id(note_id, user_id)
        if not note: 
            raise NoteNotFound("Note not found with that ID")
        return note

    def create_note(self, new_note: NoteCreate, user_id: int):
        note = Note.model_validate(new_note, update={"user_id": user_id})
        note_db = self.repo.create(note)
        return note_db

    def delete_note(self, note_id: int, user_id: int):
        db_note = self.repo.get_by_id(note_id, user_id)
        if not db_note:
            raise NoteNotFound("Note not found with that ID")
        is_deleted = self.repo.delete(db_note)
        return is_deleted

    def update_note(self, note_id:int, updated_note: int, user_id: int):
        db_note = self.repo.get_by_id(note_id, user_id)
        if not db_note:
            raise NoteNotFound("Note not found with that ID")
        return self.repo.update(db_note, updated_note)

    def generate_propmt(self, user_id: int):
        db_notes = self.repo.get_all(user_id)
        notes_for_prompt = [
            {
                "id": note.id,
                "title": note.title,
                "description": note.description
            } 
            for note in db_notes
        ]
        note_json = json.dumps(notes_for_prompt)
        propmt = f"{GENERAL_PROPMT} '\n\nNotas:\n' {note_json}"
        llm_response = generate_content_via_llm(propmt)
        notes_prioritized = json.loads(llm_response.response)
        prioritize_list = [NotePriority.model_validate(item) for item in notes_prioritized]
        return prioritize_list
