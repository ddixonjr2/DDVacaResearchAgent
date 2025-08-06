from vaca_user_context import UserContext

class PrefsManager():
    def __init__(self):
        self.user_context = UserContext()
    
    def set_name(self, name: str):
        print(f'Updating name to {name}')
        self.user_context.name = name

    def set_cur_location(self, location: str):
        print(f'Updating current location to {location}')
        self.user_context.current_location = location

    def set_prefs(self, preferences: str):
        print(f'Updating preferences to {preferences}')
        self.user_context.preferences = preferences


