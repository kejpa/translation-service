from docx import Document

from translation_service.docx_exporter import (
    ParagraphTranslation,
    build_translated_document,
    create_translated_docx,
    translate_document,
    translate_paragraphs,
)
from translation_service.models import DocumentPair, TranslationUnit
from translation_service.ollama_service import OllamaError
from translation_service.translation_status import TranslationStatus


def test_create_translated_docx(tmp_path):
    output_file = tmp_path / "translated.docx"

    create_translated_docx(
        [
            ParagraphTranslation(
                source_text="Hei maailma",
                target_text="Hej världen",
                status=TranslationStatus.TRANSLATED,
            ),
            ParagraphTranslation(
                source_text="Miten voit?",
                target_text="Hur mår du?",
                status=TranslationStatus.TRANSLATED,
            ),
        ],
        output_file,
    )

    document = Document(str(output_file))

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    assert paragraphs == [
        "Hej världen",
        "Hur mår du?",
    ]


def test_translate_paragraphs(db):
    document_pair = DocumentPair(
        source_document="source.docx",
        target_document="target.docx",
    )

    db.add(document_pair)
    db.flush()

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Hei maailma",
            target_text="Hej världen",
        )
    )

    db.commit()

    translated = translate_paragraphs(
        [
            "Hei maailma",
            "Tuntematon teksti",
        ],
        db,
    )

    assert translated[0].target_text == "Hej världen"
    assert translated[0].status == TranslationStatus.TRANSLATED

    assert translated[1].target_text == "Tuntematon teksti"
    assert translated[1].status == TranslationStatus.MISSING


def test_translate_document(
    tmp_path,
    db,
):
    document_pair = DocumentPair(
        source_document="source.docx",
        target_document="target.docx",
    )

    db.add(document_pair)
    db.flush()

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Hei maailma",
            target_text="Hej världen",
        )
    )

    db.commit()

    source_file = tmp_path / "source.docx"
    output_file = tmp_path / "translated.docx"

    source_doc = Document()
    source_doc.add_paragraph("Hei maailma")
    source_doc.add_paragraph("Tuntematon teksti")
    source_doc.save(str(source_file))

    translate_document(
        source_file,
        output_file,
        db,
    )

    translated_doc = Document(str(output_file))

    paragraphs = [paragraph.text for paragraph in translated_doc.paragraphs]

    assert paragraphs == [
        "Hej världen",
        "Tuntematon teksti",
    ]


def test_create_translated_docx_marks_missing_translations(
    tmp_path,
):
    output_file = tmp_path / "translated.docx"

    create_translated_docx(
        [
            ParagraphTranslation(
                source_text="Hei maailma",
                target_text="Hej världen",
                status=TranslationStatus.TRANSLATED,
            ),
            ParagraphTranslation(
                source_text="Tuntematon teksti",
                target_text="Tuntematon teksti",
                status=TranslationStatus.MISSING,
            ),
        ],
        output_file,
    )

    document = Document(str(output_file))

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    assert paragraphs == [
        "Hej världen",
        "Tuntematon teksti",
    ]


def test_build_translated_document():
    document = build_translated_document(
        [
            ParagraphTranslation(
                source_text="Hei maailma",
                target_text="Hej världen",
                status=TranslationStatus.TRANSLATED,
            ),
            ParagraphTranslation(
                source_text="",
                target_text="",
                status=TranslationStatus.EMPTY,
            ),
            ParagraphTranslation(
                source_text="Miten voit?",
                target_text="Hur mår du?",
                status=TranslationStatus.TRANSLATED,
            ),
        ]
    )

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    assert paragraphs == [
        "Hej världen",
        "",
        "Hur mår du?",
    ]


def test_build_translated_document_marks_missing_translations():
    document = build_translated_document(
        [
            ParagraphTranslation(
                source_text="Hei maailma",
                target_text="Hej världen",
                status=TranslationStatus.TRANSLATED,
            ),
            ParagraphTranslation(
                source_text="Tuntematon teksti",
                target_text="Tuntematon teksti",
                status=TranslationStatus.MISSING,
            ),
        ]
    )

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    assert paragraphs == [
        "Hej världen",
        "Tuntematon teksti",
    ]


def test_fuzzy_match_above_reuse_threshold_is_reused(
    db,
    monkeypatch,
):
    monkeypatch.setenv(
        "REUSE_THRESHOLD",
        "85",
    )

    document_pair = DocumentPair(
        source_document="source.docx",
        target_document="target.docx",
    )

    db.add(document_pair)
    db.flush()

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Hei maailma",
            target_text="Hej världen",
        )
    )

    db.commit()

    translations = translate_paragraphs(
        ["Hei maailma!"],
        db,
    )

    assert len(translations) == 1

    assert translations[0].target_text == "Hej världen"

    assert translations[0].status == TranslationStatus.FUZZY_HIGH


def test_fuzzy_match_below_reuse_threshold_is_not_reused(
    db,
    monkeypatch,
):
    monkeypatch.setenv(
        "REUSE_THRESHOLD",
        "95",
    )

    document_pair = DocumentPair(
        source_document="source.docx",
        target_document="target.docx",
    )

    db.add(document_pair)
    db.flush()

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Hei maailma",
            target_text="Hej världen",
        )
    )

    db.commit()

    translations = translate_paragraphs(
        ["God morgon"],
        db,
    )

    assert len(translations) == 1

    assert translations[0].status == TranslationStatus.MISSING


def test_fuzzy_match_between_thresholds_becomes_fuzzy_low(
    db,
    monkeypatch,
):
    monkeypatch.setenv(
        "REUSE_THRESHOLD",
        "98",
    )

    monkeypatch.setenv(
        "REFERENCE_THRESHOLD",
        "30",
    )

    document_pair = DocumentPair(
        source_document="source.docx",
        target_document="target.docx",
    )

    db.add(document_pair)
    db.flush()

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Hei maailma",
            target_text="Hej världen",
        )
    )

    db.commit()

    translations = translate_paragraphs(
        ["Hei maailmaa"],
        db,
    )

    assert len(translations) == 1

    assert translations[0].status == TranslationStatus.FUZZY_LOW

    assert translations[0].target_text == "Hei maailmaa"


def test_missing_translation_uses_llm_fallback(
    monkeypatch,
    db,
):
    monkeypatch.setattr(
        "translation_service.docx_exporter.translate_text",
        lambda text: "Hej världen",
    )

    translations = translate_paragraphs(
        ["Hei maailma"],
        db,
    )

    assert translations[0].target_text == "Hej världen"

    assert translations[0].status == TranslationStatus.LLM


def test_llm_failure_results_in_missing_status(
    monkeypatch,
    db,
):
    def fail(_):
        raise OllamaError(
            "Failed to communicate with Ollama",
        )

    monkeypatch.setattr(
        "translation_service.docx_exporter.translate_text",
        fail,
    )

    translations = translate_paragraphs(
        ["Hei maailma"],
        db,
    )

    assert translations[0].status == TranslationStatus.MISSING
