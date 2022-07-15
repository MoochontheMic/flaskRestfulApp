from resources.user import User






users = [
    User(1,'bob', 'asdf')
]

usernameMapping = {u.username : u for u in users}

userIdMapping = {u.id : u for u in users}

def authenticate(username:str, password:str):
    user = User.findByUsername(username)
    if user and user.password == password:
        return user

def identity(payload):
    userId = payload['identity']
    return User.findById(userId)



