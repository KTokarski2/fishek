import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# load_prompt
# ---------------------------------------------------------------------------

def test_load_prompt_replaces_placeholders(tmp_path):
    from services.translation_service import load_prompt

    template = "Translate <Word> from <Language> to Polish."
    prompt_file = tmp_path / "translate.txt"
    prompt_file.write_text(template, encoding="utf-8")

    with patch("services.translation_service.PROMPTS_DIR", tmp_path):
        result = load_prompt("translate.txt", {"<Word>": "cat", "<Language>": "English"})

    assert result == "Translate cat from English to Polish."


def test_load_prompt_multiple_occurrences(tmp_path):
    from services.translation_service import load_prompt

    template = "<Word> means <Word> in Polish."
    prompt_file = tmp_path / "test.txt"
    prompt_file.write_text(template, encoding="utf-8")

    with patch("services.translation_service.PROMPTS_DIR", tmp_path):
        result = load_prompt("test.txt", {"<Word>": "dog"})

    assert result == "dog means dog in Polish."


def test_load_prompt_no_placeholders(tmp_path):
    from services.translation_service import load_prompt

    template = "Just a plain prompt."
    (tmp_path / "plain.txt").write_text(template, encoding="utf-8")

    with patch("services.translation_service.PROMPTS_DIR", tmp_path):
        result = load_prompt("plain.txt", {})

    assert result == "Just a plain prompt."


# ---------------------------------------------------------------------------
# get_translation
# ---------------------------------------------------------------------------

def test_get_translation_calls_ollama_with_filled_prompt(tmp_path):
    from services.translation_service import get_translation

    template = "Translate <Word> from <Language>."
    (tmp_path / "translate.txt").write_text(template, encoding="utf-8")

    with patch("services.translation_service.PROMPTS_DIR", tmp_path), \
         patch("services.translation_service.call_ollama", return_value="kot") as mock_ollama:
        result = get_translation("cat", "English")

    mock_ollama.assert_called_once_with("Translate cat from English.")
    assert result == "kot"


# ---------------------------------------------------------------------------
# evaluate_translation
# ---------------------------------------------------------------------------

def test_evaluate_translation_parses_valid_json():
    from services.translation_service import evaluate_translation

    valid_json = '{"accuracy": 9, "naturalness": 8, "fluency": 7, "notes": "Good"}'

    with patch("services.translation_service.call_ollama", return_value=valid_json), \
         patch("services.translation_service.load_prompt", return_value="prompt"):
        result = evaluate_translation("cat", "kot")

    assert result == {"accuracy": 9, "naturalness": 8, "fluency": 7, "notes": "Good"}


def test_evaluate_translation_falls_back_on_invalid_json():
    from services.translation_service import evaluate_translation

    bad_response = "Here is some explanation: accuracy=9"

    with patch("services.translation_service.call_ollama", return_value=bad_response), \
         patch("services.translation_service.load_prompt", return_value="prompt"):
        result = evaluate_translation("cat", "kot")

    assert "raw_response" in result
    assert result["raw_response"] == bad_response


# ---------------------------------------------------------------------------
# get_refined_translation
# ---------------------------------------------------------------------------

def test_get_refined_translation_passes_all_placeholders(tmp_path):
    from services.translation_service import get_refined_translation

    template = "<Word>|<Language>|<PreviousTranslation>|<Accuracy>|<Naturalness>|<Fluency>|<Notes>"
    (tmp_path / "refine.txt").write_text(template, encoding="utf-8")

    with patch("services.translation_service.PROMPTS_DIR", tmp_path), \
         patch("services.translation_service.call_ollama", return_value="ulepszone") as mock_ollama:
        result = get_refined_translation("cat", "English", "kociak", 6, 5, 7, "Too informal")

    expected_prompt = "cat|English|kociak|6|5|7|Too informal"
    mock_ollama.assert_called_once_with(expected_prompt)
    assert result == "ulepszone"


# ---------------------------------------------------------------------------
# call_ollama
# ---------------------------------------------------------------------------

def test_call_ollama_returns_stripped_response():
    from services.translation_service import call_ollama

    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "  kot  "}
    mock_response.raise_for_status = MagicMock()

    with patch("services.translation_service.requests.post", return_value=mock_response):
        result = call_ollama("translate cat")

    assert result == "kot"


def test_call_ollama_raises_on_http_error():
    from services.translation_service import call_ollama
    import requests as req

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = req.HTTPError("500 Server Error")

    with patch("services.translation_service.requests.post", return_value=mock_response):
        with pytest.raises(req.HTTPError):
            call_ollama("prompt")
