from translation_service.database import SessionLocal
from translation_service.models import TranslationUnit

with SessionLocal() as db:
    # Skapa testdata
    unit = TranslationUnit(
        source_text="Hei maailma",
        target_text="Hej världen",
        source_document="test.docx",
    )

    db.add(unit)
    db.commit()

    result = db.query(TranslationUnit).first()

    print(result.source_text)
    print(result.target_text)
    print(result.source_document)

    db.close()
