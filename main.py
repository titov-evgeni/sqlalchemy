import os
import database

from database import DATABASE_NAME, Session
from models import (
    Lesson,
    Student,
    Group,
    Teacher,
    association_table1,
    association_table2,
    association_table3,
)

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        database.create_db()
