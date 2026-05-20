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

def get_project_by_name(db: Session, name: str):
    return db.query(Project).filter(Project.name == name).first()

def delete_project_by_id(db:Session, id:int):
    project = db.get(Project, id)
    db.delete(project)
    db.commit()
    return project

def update_project_by_id(db:Session, id:int, name:str):
    project = db.get(Project, id)
    if not project:
        return None
    project.name = name
    db.commit()
    db.refresh(project)
    return project