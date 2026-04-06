import os
import requests

FLASHCARD_API_BASE_URL = os.getenv("FLASHCARD_API_BASE_URL", "http://localhost:8080")
FLASHCARD_API_EMAIL = os.getenv("FLASHCARD_API_EMAIL", "")
FLASHCARD_API_PASSWORD = os.getenv("FLASHCARD_API_PASSWORD", "")
FLASHCARD_ENDPOINT = "/api/v1/flashcard"
AUTH_ENDPOINT = "/api/v1/auth/login"

LANGUAGE_MAP = {
    "english": "ENGLISH",
    "french": "FRENCH",
    "russian": "RUSSIAN",
}


def normalize_language(language: str) -> str:
    return LANGUAGE_MAP.get(language.lower().strip(), language.upper().strip())


def get_token() -> str:
    response = requests.post(
        f"{FLASHCARD_API_BASE_URL}{AUTH_ENDPOINT}",
        json={"email": FLASHCARD_API_EMAIL, "password": FLASHCARD_API_PASSWORD},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["token"]


def create_flashcard(original_text: str, translated_polish_text: str, language: str, token: str) -> None:
    payload = {
        "originalText": original_text,
        "translatedPolishText": translated_polish_text,
        "language": normalize_language(language),
    }
    response = requests.post(
        f"{FLASHCARD_API_BASE_URL}{FLASHCARD_ENDPOINT}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()


def create_flashcards(accepted_translations: list) -> list[str]:
    """
    accepted_translations: list of [word, language, translation, accuracy, naturalness, fluency, notes]
    Returns list of words that failed (empty list = all OK).
    """
    token = get_token()
    failed = []
    for item in accepted_translations:
        word, language, translation = item[0], item[1], item[2]
        try:
            create_flashcard(word, translation, language, token)
        except Exception:
            failed.append(word)
    return failed
