from database.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()  # откатываем транзакцию если что-то пошло не так
        raise
    finally:
        db.close()
