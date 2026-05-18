from src.db_manager import DBManager


class BaseService:
    db: DBManager

    def __init__(self, db: DBManager):
        self.db = db
