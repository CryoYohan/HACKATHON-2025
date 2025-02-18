from .hashpw import PasswordHashing
from ..databasehelper.dbhelper import Databasehelper

class Authorization:
    def __init__(self):
        self.encrypt = PasswordHashing()
        self.db = Databasehelper()

    def login(self, **kwargs):
        """Check if a student account exists and return a Student instance if valid."""
        email = kwargs.get('email')
        password = kwargs.get('password')  # Get password from kwargs
        try:
            student_exists = self.db.find_record('user', email=email)

            if student_exists:
                user_data = student_exists[0]  # Access the first (and only) user record
                try:
                    password_correct = self.encrypt.check_password(password, user_data['password'])
                    if password_correct:
                        return {
                            'success': True,
                            'name': user_data['name'],
                            'email': user_data['email'],
                        }
                    else:
                        return {'success': False, 'error': 'Password incorrect!'}
                except Exception as e:
                    return {'success': False, 'error': str(e)}           
            else:
                return {'success': False, 'error': 'User does not exist.'}

        except Exception as e:
            return {'success': False, 'error': str(e)}

                

    def register(self, **kwargs):
        email = kwargs.get('email')
        existing_user = self.db.find_record('user', email=email)

        if not existing_user:
            hashed_password = self.encrypt.hashpassword(kwargs.get('password'))
            volunteer_data = {k: v for k, v in kwargs.items() if k != 'password'}

            volunteer_data['password'] = hashed_password  # Store hashed password
            self.db.add_record(table='user', **volunteer_data)

            del volunteer_data['password']

            volunteer_data['success'] = True
            return volunteer_data
        else:
            return {'success': False, 'error': 'Email already exists!'}
