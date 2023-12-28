from src.model.user import User

class BasicDb:
    def __init__(self):
        self.users = dict()
        
    
    def create(self, user: User) -> None:
        if user.email in self.users:
            raise ValueError
        self.users[user.email] = user
        
        
    def save (self, user: User) -> None:
        self.users[user.email] = user
    
    
    def get_by_id(self, user_id: str) -> User:
        return self.users[user_id]
    
    
    