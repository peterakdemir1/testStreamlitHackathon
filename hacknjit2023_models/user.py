class User:
    def __init__(self, username: str, email: str, password: str, treasures: dict):
        self.username = username
        self.email = email
        self.password = password
        self.treasures = treasures