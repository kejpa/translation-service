from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DocumentPair(Base):
    __tablename__ = "document_pairs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_document: Mapped[str] = mapped_column(String)
    target_document: Mapped[str] = mapped_column(String)


class TranslationUnit(Base):
    __tablename__ = "translation_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_pair_id: Mapped[int] = mapped_column(ForeignKey("document_pairs.id"))
    source_text: Mapped[str] = mapped_column(Text)
    target_text: Mapped[str] = mapped_column(Text)
