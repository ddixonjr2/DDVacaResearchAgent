from agents import SQLiteSession
from typing_extensions import TypedDict, NotRequired
from random import randint

class UserContext(TypedDict, total=False):
    name: NotRequired[str]
    current_location: str
    preferences: list[str]

class VacationResearchSession(SQLiteSession):
    '''
    Data store for vacation research agent conversations.
    
    Args:
    - db_path: The file path of the database that persists the session conversations.
    
    '''

    def __init__(self, db_path='vacation_research.db'):
        unique_id = randint(1001, 1000000)
        super().__init__(session_id=f'vacares{unique_id}', db_path='vacation_research.db')
