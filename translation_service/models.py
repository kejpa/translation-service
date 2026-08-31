from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TranslationUnit(Base):
    __tablename__ = "translation_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    source_text: Mapped[str] = mapped_column(Text)
    target_text: Mapped[str] = mapped_column(Text)

    source_document: Mapped[str] = mapped_column(String(255))
