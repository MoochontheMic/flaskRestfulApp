users = [
    {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
]

usernameMapping = {'bob':{
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}



userIdMapping = {1:{
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}

def authenticate(username, password):
    user = usernameMapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    userId = payload['identity']
    return userIdMapping.get(userId, None)
