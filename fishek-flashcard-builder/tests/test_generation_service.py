import json
import pytest
from unittest.mock import patch, call


def test_generate_word_list_returns_parsed_lines():
    from services.generation_service import generate_word_list

    with patch("services.generation_service.load_prompt", return_value="prompt"), \
         patch("services.generation_service.call_ollama", return_value="cat\ndog\nbird"):
        result = generate_word_list("animals", "English", 10)

    assert result == ["cat", "dog", "bird"]


def test_generate_word_list_strips_bullet_markers():
    from services.generation_service import generate_word_list

    with patch("services.generation_service.load_prompt", return_value="prompt"), \
         patch("services.generation_service.call_ollama", return_value="- cat\n• dog\n* bird\n· fish"):
        result = generate_word_list("animals", "English", 10)

    assert result == ["cat", "dog", "bird", "fish"]


def test_generate_word_list_limits_to_count():
    from services.generation_service import generate_word_list

    response = "\n".join([f"word{i}" for i in range(15)])

    with patch("services.generation_service.load_prompt", return_value="prompt"), \
         patch("services.generation_service.call_ollama", return_value=response):
        result = generate_word_list("misc", "English", 5)

    assert len(result) == 5


def test_generate_word_list_removes_empty_lines():
    from services.generation_service import generate_word_list

    with patch("services.generation_service.load_prompt", return_value="prompt"), \
         patch("services.generation_service.call_ollama", return_value="cat\n\ndog\n\n"):
        result = generate_word_list("animals", "English", 10)

    assert result == ["cat", "dog"]


def test_generate_word_list_passes_correct_placeholders():
    from services.generation_service import generate_word_list

    with patch("services.generation_service.load_prompt", return_value="prompt") as mock_load, \
         patch("services.generation_service.call_ollama", return_value="cat"):
        generate_word_list("animals", "English", 7)

    mock_load.assert_called_once_with("generate_words.txt", {
        "<Tags>": "animals",
        "<Language>": "English",
        "<Count>": "7",
    })


def test_validate_word_returns_true_for_valid_json():
    from services.generation_service import validate_word

    response = json.dumps({"valid": True, "reason": "relevant IT term"})

    with patch("services.generation_service.load_prompt", return_value="prompt"), \
         patch("services.generation_service.call_ollama", return_value=response):
        valid, reason = validate_word("algorithm", "English", "IT vocabulary")

    assert valid is True
    assert "IT term" in reason


def test_validate_word_returns_false_for_invalid_json():
    from services.generation_service import validate_word

    response = json.dumps({"valid": False, "reason": "not related to topic"})

    with patch("services.generation_service.load_prompt", return_value="prompt"), \
         patch("services.generation_service.call_ollama", return_value=response):
        valid, reason = validate_word("random", "English", "IT vocabulary")

    assert valid is False
    assert "not related" in reason


def test_validate_word_defaults_to_true_on_json_error():
    from services.generation_service import validate_word

    with patch("services.generation_service.load_prompt", return_value="prompt"), \
         patch("services.generation_service.call_ollama", return_value="not json at all"):
        valid, reason = validate_word("algorithm", "English", "IT vocabulary")

    assert valid is True


def test_validate_word_passes_correct_placeholders():
    from services.generation_service import validate_word

    with patch("services.generation_service.load_prompt", return_value="prompt") as mock_load, \
         patch("services.generation_service.call_ollama", return_value='{"valid": true, "reason": "ok"}'):
        validate_word("algorithm", "English", "IT vocabulary")

    mock_load.assert_called_once_with("validate_word.txt", {
        "<Word>": "algorithm",
        "<Language>": "English",
        "<Tags>": "IT vocabulary",
    })


def test_validate_word_handles_missing_reason_field():
    from services.generation_service import validate_word

    response = json.dumps({"valid": True})

    with patch("services.generation_service.load_prompt", return_value="prompt"), \
         patch("services.generation_service.call_ollama", return_value=response):
        valid, reason = validate_word("algorithm", "English", "IT vocabulary")

    assert valid is True
    assert reason == ""
