from sqlalchemy.orm import Session
from models.models import Project

def create_project(db: Session, data: dict):
    project = Project(**data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_all_projects(db: Session):
    return db.query(Project).all()

def get_project_by_id(db: Session, id: int):
    return db.query(Project).filter(Project.id == id).first()

def get_project_by_title(db: Session, title: str):
    return db.query(Project).filter(Project.title == title).first()

def get_projects_by_owner(db: Session, owner_id: int):
    return db.query(Project).filter(Project.owner_id == owner_id).all()

def delete_project_by_id(db: Session, id: int):
    project = db.get(Project, id)
    if not project:
        return None
    db.delete(project)
    db.commit()
    return project

def update_project_by_id(db: Session, id: int, data: dict):
    project = db.get(Project, id)
    if not project:
        return None
    for key, value in data.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project