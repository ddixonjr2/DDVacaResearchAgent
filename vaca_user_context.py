from agents import SQLiteSession, function_tool
from typing_extensions import TypedDict, NotRequired
from random import randint

KEY_NAME = 'name'
KEY_CURRENT_LOCATION = 'current_location'
KEY_PREFERENCES = 'preferences'

class UserContext():
    def __init__(self, name: str = '', current_location: str = '', preferences: list[str] = []):
        self.name = name
        self.current_location = current_location
        self.preferences = preferences
    
    def context_augmented_request(self, request: str) -> str:
        """
        Augments the request with user context information.
        
        Args:
        - request: The original request string.
        
        Returns:
        - A string that includes the user's name and preferences in the request.
        """
        user_context_string = ''
        user_context_string += f'my name is {self.name or ''}, ' if self.name or None else ''
        user_context_string += f'my current location is {self.current_location or ''}, ' if self.current_location or None else ''
        user_context_string += f'my vacation and travel preferences are {', '.join(self.preferences or [])}.' if self.preferences or None else ''
        return f'Given that {user_context_string} -- Please provide a response to my following request: {request}'

class VacationResearchSession(SQLiteSession):
    '''
    Data store for vacation research agent conversations.
    
    Args:
    - db_path: The file path of the database that persists the session conversations.
    
    '''

    def __init__(self, db_path='vacation_research.db'):
        # unique_id = randint(1001, 1000000)
        # super().__init__(session_id=f'vacares{unique_id}', db_path='vacation_research.db')

        # Override hardcoded session to test whether this would provide permanent conversation persistence.
        # I believe so but I'm sure this would then exceed the context window at some point. :(
        super().__init__(session_id=f'vacares9999998', db_path='vacation_research.db')
