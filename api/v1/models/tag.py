"""Tag data model"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from api.v1.models.base_model import BaseTableModel


class Tag(BaseTableModel):
    __tablename__ = "tags"

    name = Column(String(255), unique=True, nullable=False)

    # Many-to-Many with Image via association table
    images = relationship("Image", secondary="image_tags", back_populates="tags")
