from user import User

class Admin(User):
    def __init__(self,name:str, email:str, role='Admin'):
        super.__init__(name:str, email:str)
        self.role = role
    
    def add():
        pass

    def delete():
        pass

    def edit():
        pass