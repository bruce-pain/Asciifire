"""Image data model"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from api.v1.models.base_model import BaseTableModel


class Image(BaseTableModel):
    __tablename__ = "images"

    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    ascii_art = Column(String, nullable=False)

    # Relationship with User
    user = relationship("User", back_populates="images")

    # Many-to-Many with Tag via association table
    tags = relationship("Tag", secondary="image_tags", back_populates="images")
