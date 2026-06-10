from sqlalchemy.orm import Session

from models.models import ProjectOnPlatform


def create_project_platform(db: Session,project_id: int,platform_id: int):
    project_platform = ProjectOnPlatform(project_id=project_id,platform_id=platform_id)
    db.add(project_platform)
    db.commit()
    db.refresh(project_platform)
    return project_platform

def get_project_platforms(db: Session,project_id: int):
    return db.query(ProjectOnPlatform).filter(ProjectOnPlatform.project_id == project_id).all()

def get_project_platform(db: Session,project_id: int,platform_id: int):
    return db.query(ProjectOnPlatform).filter(ProjectOnPlatform.project_id == project_id,ProjectOnPlatform.platform_id == platform_id).first()

def delete_project_platform(db: Session,project_id: int,platform_id: int):
    project_platform = get_project_platform(db,project_id,platform_id)
    db.delete(project_platform)
    db.commit()
    return project_platform