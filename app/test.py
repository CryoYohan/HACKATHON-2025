from .authorization.login_register import Authorization
auth = Authorization()
def login():
    # Test login
    email = input("Enter email: ")
    password = input("Enter password: ")
    login_result = auth.login(email=email, password=password)

    print("Login Result:", login_result)


def register():
    print("\nRegistering new user...")
    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    
    register_result = auth.register(
        name=name,email=email, password=password,
    )

    print("Registration Result:", register_result)

if __name__ == "__main__":
    register()
    login()