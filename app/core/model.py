class User:
    def __init__(
        self, id: int, email: str, hashed_password: str, is_active: bool = True
    ):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
