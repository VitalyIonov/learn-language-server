ACTION_STYLE: dict[str, dict[str | None, str]] = {
    "ru": {
        None: "",
        "VERB": (
            "Переведи глагол в форме инфинитива несовершенного вида (что делать?). "
            "Напр.: «wash» → «мыться», «cook» → «готовить»."
        ),
        "NOUN": (
            "Переведи как существительное. "
            "Напр.: «razor» → «бритва», «mirror» → «зеркало»."
        ),
        "DESCRIPTION": (
            "Для описаний действий используй глаголы несовершенного вида "
            "(отвечающие на вопрос «что делает?»). "
            "Напр.: «afeitarse» → «бриться», «lavar los platos» → «мыть посуду». "
            "Существительные и названия предметов оставляй существительными "
            "(напр.: «razor» → «бритва», не «бриться»)."
        ),
        "PHRASE": "Переведи фразу естественно, сохраняя разговорный стиль.",
    },
    "en": {
        None: "",
        "VERB": (
            "Translate as an infinitive verb with 'to'. "
            "E.g.: «мыться» → «to wash», «готовить» → «to cook»."
        ),
        "NOUN": (
            "Translate as a noun. "
            'E.g.: «бритва» → «razor», «зеркало» → «mirror».'
        ),
        "DESCRIPTION": (
            "For action descriptions, prefer present simple or gerund where natural, "
            'e.g., "to shave" / "shaving", "to wash the dishes" / "washing the dishes". '
            "Nouns and object names must remain as nouns "
            '(e.g., "бритва" -> "razor", not "shaving").'
        ),
        "PHRASE": "Translate the phrase naturally, keeping a conversational tone.",
    },
    "es": {
        None: "",
        "VERB": (
            "Traduce como un verbo en infinitivo. "
            "Usa la forma más común y coloquial, no la literaria. "
            "P. ej.: «мыться» → «lavarse», «готовить» → «cocinar», «лежать» → «estar acostado» (NO «yacer»)."
        ),
        "NOUN": (
            "Traduce como un sustantivo. "
            "P. ej.: «бритва» → «maquinilla de afeitar»."
        ),
        "DESCRIPTION": (
            "Para descripciones de acciones, usa el infinitivo "
            "(p. ej., «afeitarse», «lavar los platos»). "
            "Los sustantivos y nombres de objetos deben permanecer como sustantivos "
            "(p. ej., «бритва» → «maquinilla de afeitar», no «afeitarse»)."
        ),
        "PHRASE": "Traduce la frase de forma natural, manteniendo un tono coloquial.",
    },
}

BASE_RULES = (
    "Используй общеупотребимую, разговорную лексику. "
    "Избегай литературных, архаичных и редких слов. "
    "Выводи ТОЛЬКО перевод — без кавычек, пояснений и префиксов. "
    "Сохраняй числовые форматы, эмодзи и разметку."
)

BATCH_OUTPUT_RULES = (
    "Верни ТОЛЬКО валидный JSON-массив вида "
    '[{"id": 0, "text": "перевод"}, ...]. '
    "Без markdown-обёртки, без пояснений, без кавычек вокруг массива."
)
