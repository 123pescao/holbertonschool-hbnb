from datetime import datetime
import uuid


class Basemodel:
    """
    BaseModel class that serves as a base for other models, providing unique ID
    creation timestamp, and update timestamp.
    """
    def __init__(self, id=None, created_at=None, updated_at=None):
        """
        Initialize a new instance of BaseModel.

        Args:
            id (str, optional): Defaults to a new Unique UUID4 string.
            created_at (datetime, optional): Timestamp when created.
            updated_at (datetime, optional): Timestamp when last updated.
        """
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        return self.__dict__
