from sqlalchemy.orm import Session

from models.models import ProjectGenre


def create_project_genre(db: Session,project_id: int,genre_id: int):
    project_genre = ProjectGenre(project_id=project_id,genre_id=genre_id)
    db.add(project_genre)
    db.commit()
    db.refresh(project_genre)
    return project_genre

def get_project_genres(db: Session,project_id: int):
    return db.query(ProjectGenre).filter(ProjectGenre.project_id == project_id).all()

def get_project_genre(db: Session,project_id: int,genre_id: int):
    return db.query(ProjectGenre).filter(ProjectGenre.project_id == project_id,ProjectGenre.genre_id == genre_id).first()

def delete_project_genre(db: Session,project_id: int,genre_id: int):
    project_genre = get_project_genre(db,project_id,genre_id)
    db.delete(project_genre)
    db.commit()
    return project_genre