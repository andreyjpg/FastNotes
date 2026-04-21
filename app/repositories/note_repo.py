from sqlmodel import Session, select
from app.models.note_model import Note
from app.dto.note_dto import NoteUpdate

class NoteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, user_id: int):
        statement = select(Note).where(Note.user_id == user_id)
        return self.session.exec(statement).all()

    def get_by_id(self, note_id: int, user_id: id):
        print(user_id)
        statement = select(Note).where(Note.id ==note_id).where(Note.user_id == user_id)
        return self.session.exec(statement).first()
    
    def create(self, db_note: Note):
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return db_note
    
    def update(self, db_note: Note, updated_note: NoteUpdate):
        obj_note = updated_note.model_dump(exclude_unset=True)

        for key, value in obj_note.items():
            setattr(db_note, key, value)

        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return db_note
    
    def delete(self, db_note: Note):
        self.session.delete(db_note)
        self.session.commit()
        return True