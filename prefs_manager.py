import os

from vaca_user_context import UserContext, KEY_NAME, KEY_CURRENT_LOCATION, KEY_PREFERENCES
from json import dumps, loads

DEFAULT_CONTEXT_FILENAME = 'user_ctx.json'


class PrefsManager():
    def __init__(self):
        self.user_context = UserContext()
        
    def context_repo_exists(self) -> bool:
        return os.path.exists(os.path.join(os.getcwd(), DEFAULT_CONTEXT_FILENAME))

    def save_user_context(
        self,
        name: str = None,
        current_location: str = None,
        preferences: list[str] = None
        ):
        
        operation = 'w+' if self.context_repo_exists() else 'w'
        try:
            with open(DEFAULT_CONTEXT_FILENAME, operation) as ctxfile:
                ctx = {
                    KEY_NAME: name or self.user_context.name,
                    KEY_CURRENT_LOCATION: current_location or self.user_context.current_location,
                    KEY_PREFERENCES: preferences or self.user_context.preferences
                }
                ctxfile.write(dumps(ctx))
            print(f'User context saved to {DEFAULT_CONTEXT_FILENAME}')
        except Exception as e:
            print(f'Failed to save user context to {DEFAULT_CONTEXT_FILENAME}\n{e}')

    def load_user_context(self):
        if self.context_repo_exists():
            try:
                with open(DEFAULT_CONTEXT_FILENAME, 'r') as ctxfile:
                    json_dict = ctxfile.read()
                    ctx = loads(json_dict)
                    self.user_context.name = ctx.get(KEY_NAME, '')
                    self.user_context.current_location = ctx.get(KEY_CURRENT_LOCATION, '')
                    self.user_context.preferences = ctx.get(KEY_PREFERENCES, [])
                print('User context loaded from user_ctx.json')
            except Exception as e:
                print(f'Failed to load existing user context {DEFAULT_CONTEXT_FILENAME}\n{e}')
        else:
            self.user_context.name = ''
            self.user_context.current_location = ''         
            self.user_context.preferences = []
            self.save_user_context()


    def set_name(self, name: str):
        print(f'Updating name to {name}')
        self.user_context.name = name

    def set_cur_location(self, location: str):
        print(f'Updating current location to {location}')
        self.user_context.current_location = location

    def set_prefs(self, preferences: str):
        print(f'Updating preferences to {preferences}')
        self.user_context.preferences = preferences


