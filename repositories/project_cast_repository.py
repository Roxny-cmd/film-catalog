from sqlalchemy.orm import Session
from models.models import ProjectCast

def create_project_cast(db:Session, project_id:int, actor_id:int, role:str):
    cast = ProjectCast(project_id=project_id, actor_id=actor_id, role=role)
    db.add(cast)
    db.commit()
    db.refresh(cast)
    return cast

def get_project_cast(db:Session, project_id:int):
    return db.query(ProjectCast).filter(ProjectCast.project_id == project_id).all()

def get_project_cast_member(db:Session, project_id:int,actor_id:int):
    return db.query(ProjectCast).filter(ProjectCast.project_id == project_id, ProjectCast.actor_id == actor_id).first()

def delete_project_cast_member(db:Session, project_id:int, actor_id:int):
    cast = get_project_cast_member(db, project_id, actor_id)
    db.delete(cast)
    db.commit()
    return cast

def update_project_cast_member_role(db:Session, project_id:int, actor_id:int, role:str):
    cast = get_project_cast_member(db, project_id, actor_id)
    if not cast:
        return None
    cast.role = role
    db.commit()
    db.refresh(cast)
    return cast