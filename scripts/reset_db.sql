BEGIN;

TRUNCATE
    definitions_questions,
    definitions_meanings,
    meanings_progress_info,
    definitions_progress_info,
    text_definitions,
    image_definitions,
    definitions,
    questions,
    issues,
    meanings,
    categories,
    assets,
    audio_assets,
    image_assets,
    levels
CASCADE;

COMMIT;
