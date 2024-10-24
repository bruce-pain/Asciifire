from sqlalchemy import Column, ForeignKey, String
from api.v1.models.base_model import BaseTableModel


class ImageTag(BaseTableModel):
    __tablename__ = "image_tags"

    image_id = Column(
        String, ForeignKey("images.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    tag_id = Column(
        String, ForeignKey("tags.id", ondelete="CASCADE"), unique=True, nullable=False
    )
