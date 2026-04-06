import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# normalize_language
# ---------------------------------------------------------------------------

def test_normalize_language_lowercase():
    from services.flashcard_service import normalize_language
    assert normalize_language("english") == "ENGLISH"
    assert normalize_language("french") == "FRENCH"
    assert normalize_language("russian") == "RUSSIAN"


def test_normalize_language_mixed_case():
    from services.flashcard_service import normalize_language
    assert normalize_language("English") == "ENGLISH"
    assert normalize_language("FRENCH") == "FRENCH"


def test_normalize_language_with_whitespace():
    from services.flashcard_service import normalize_language
    assert normalize_language("  english  ") == "ENGLISH"


def test_normalize_language_unknown_uppercases():
    from services.flashcard_service import normalize_language
    assert normalize_language("german") == "GERMAN"


# ---------------------------------------------------------------------------
# get_token
# ---------------------------------------------------------------------------

def test_get_token_returns_token_string():
    from services.flashcard_service import get_token

    mock_response = MagicMock()
    mock_response.json.return_value = {"token": "abc123"}
    mock_response.raise_for_status = MagicMock()

    with patch("services.flashcard_service.requests.post", return_value=mock_response):
        token = get_token()

    assert token == "abc123"


def test_get_token_raises_on_http_error():
    from services.flashcard_service import get_token
    import requests as req

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = req.HTTPError("401")

    with patch("services.flashcard_service.requests.post", return_value=mock_response):
        with pytest.raises(req.HTTPError):
            get_token()


# ---------------------------------------------------------------------------
# create_flashcard
# ---------------------------------------------------------------------------

def test_create_flashcard_sends_correct_payload():
    from services.flashcard_service import create_flashcard

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()

    with patch("services.flashcard_service.requests.post", return_value=mock_response) as mock_post:
        create_flashcard("cat", "kot", "english", "tok123")

    call_kwargs = mock_post.call_args
    payload = call_kwargs.kwargs["json"]
    headers = call_kwargs.kwargs["headers"]

    assert payload["originalText"] == "cat"
    assert payload["translatedPolishText"] == "kot"
    assert payload["language"] == "ENGLISH"
    assert headers["Authorization"] == "Bearer tok123"


def test_create_flashcard_raises_on_http_error():
    from services.flashcard_service import create_flashcard
    import requests as req

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = req.HTTPError("400")

    with patch("services.flashcard_service.requests.post", return_value=mock_response):
        with pytest.raises(req.HTTPError):
            create_flashcard("cat", "kot", "english", "tok123")


# ---------------------------------------------------------------------------
# create_flashcards
# ---------------------------------------------------------------------------

def _make_row(word="cat", language="english", translation="kot"):
    return [word, language, translation, 9, 8, 9, "Good translation"]


def test_create_flashcards_returns_empty_on_success():
    from services.flashcard_service import create_flashcards

    rows = [_make_row("cat"), _make_row("dog", translation="pies")]

    with patch("services.flashcard_service.get_token", return_value="tok"), \
         patch("services.flashcard_service.create_flashcard") as mock_create:
        failed = create_flashcards(rows)

    assert failed == []
    assert mock_create.call_count == 2


def test_create_flashcards_returns_failed_words():
    from services.flashcard_service import create_flashcards

    rows = [_make_row("cat"), _make_row("dog", translation="pies")]

    def fail_on_dog(original, translation, language, token):
        if original == "dog":
            raise Exception("API error")

    with patch("services.flashcard_service.get_token", return_value="tok"), \
         patch("services.flashcard_service.create_flashcard", side_effect=fail_on_dog):
        failed = create_flashcards(rows)

    assert failed == ["dog"]


def test_create_flashcards_gets_token_once():
    from services.flashcard_service import create_flashcards

    rows = [_make_row("cat"), _make_row("dog"), _make_row("bird")]

    with patch("services.flashcard_service.get_token", return_value="tok") as mock_token, \
         patch("services.flashcard_service.create_flashcard"):
        create_flashcards(rows)

    mock_token.assert_called_once()


def test_create_flashcards_all_failed():
    from services.flashcard_service import create_flashcards

    rows = [_make_row("cat"), _make_row("dog")]

    with patch("services.flashcard_service.get_token", return_value="tok"), \
         patch("services.flashcard_service.create_flashcard", side_effect=Exception("fail")):
        failed = create_flashcards(rows)

    assert set(failed) == {"cat", "dog"}
