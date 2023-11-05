class Image:
    def __init__(self, username: str, image_bytes: bytes):
        self.username = username
        self.image_bytes = image_bytes