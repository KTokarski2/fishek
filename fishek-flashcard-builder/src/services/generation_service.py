import json
from services.translation_service import load_prompt, call_ollama


def generate_word_list(tags: str, language: str, count: int = 10) -> list[str]:
    prompt = load_prompt("generate_words.txt", {
        "<Tags>": tags,
        "<Language>": language,
        "<Count>": str(count),
    })
    response = call_ollama(prompt)
    lines = response.strip().split("\n")
    words = []
    for line in lines:
        word = line.strip().lstrip("-•*·").strip()
        if word:
            words.append(word)
    return words[:count]


def validate_word(word: str, language: str, tags: str) -> tuple[bool, str]:
    prompt = load_prompt("validate_word.txt", {
        "<Word>": word,
        "<Language>": language,
        "<Tags>": tags,
    })
    response = call_ollama(prompt)
    try:
        data = json.loads(response)
        return bool(data.get("valid", True)), str(data.get("reason", ""))
    except (json.JSONDecodeError, AttributeError):
        return True, response
