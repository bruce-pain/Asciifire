"""User data model"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from api.v1.models.base_model import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)

    # Relationship with Image
    images = relationship("Image", back_populates="user")

    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict.pop("password")
        return obj_dict

    def __str__(self):
        return "User: {}".format(self.username)
