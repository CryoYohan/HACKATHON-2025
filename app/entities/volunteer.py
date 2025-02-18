from .user import User

class Volunteer(User):
    def __init__(self, name: str, email: str, role='Volunteer'):
        super().__init__(name, email)  # Correct the super() call with parentheses
        self.role = role
    
    def add(self):
        pass

    def delete(self):
        pass

    def edit(self):
        pass

    def __str__(self):
        return f"{self.name.title()}"  # Ensure 'self' is used for accessing attributes