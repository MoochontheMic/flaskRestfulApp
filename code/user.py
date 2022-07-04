class User:
    """
    Creates/initiaises a user for the system
    """
    def __init__(self, iD:int, username:str, password:str):
        self.id = iD
        self.username = username
        self.password = password
