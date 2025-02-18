from hashpw import PasswordHashing
from ..databasehelper.dbhelper import Databasehelper

class Authorization():
    def __init__(self):
        self.encrypt = PasswordHashing()
        self.db = Databasehelper()

    def login(**kwargs):
        email = kwargs.get('email')

        try:
            volunteer_exist = self.db.find_record('kapitbisig', email=email)
            if volunteer_exist:
                for data in volunteer_exist:

                    password_correct = self.hashpasword.check_password(password, data['password'])
                    if password_correct:
                        return {
                                        'success': True,
                                        'idno': data['idno'],
                                        'firstname': data['firstname'],
                                        'middlename': data['middlename'],
                                        'lastname': data['lastname'],
                                        'course': data['course'],
                                        'year': data['year'],
                                        'email': data['email'],
                                        'image': data['image'],
                                        'session': data['session'],
                                        }
                    else:
                        return {'success': False, 'error' :'Password incorrect!' }

            else:
                return {'success': False, 'error': 'User does not exist!'}

        except Exception as e:
            return {'success': False, 'error':str(e)}


    def register(**kwargs):
        email_exist =  [user['email'] for user in users if user['email'] == kwargs.get('email')]
        if not email_exist:
            hashed_password = self.encrypt.hashpassword(kwargs.get('password'))

            volunteer_data = {k:v for k,v in kwargs.items() if k != 'password'}
            self.db.add_record(table='kapitbisig',**volunteer_data)
            
            volunteer_data['success'] = True

            return volunteer_data
        else:
            return {'success': False, 'error': 'Email already exists!'} 