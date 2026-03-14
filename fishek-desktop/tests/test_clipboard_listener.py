from unittest.mock import patch, MagicMock
import threading
import time
from src.clipboard_listener import get_clipboard, watch_clipboard

def test_get_clipboard_resturns_string_on_linux():
    mock_result = MagicMock()
    mock_result.stdout = "test clipboard content"
    with patch("sys.platform", "linux"), \
        patch("subprocess.run", return_value=mock_result):
        result = get_clipboard()
        assert result == "test clipboard content"

def test_get_clipboard_returns_none_on_exception():
    with patch("subprocess.run", side_effect=Exception("xclip not found")):
        result = get_clipboard()
        assert result is None

def test_watch_clipboard_calls_callback_on_change():
    calls = []
    with patch("src.clipboard_listener.get_clipboard", side_effect=["first", "second", "second"]):
        watch_clipboard(lambda text: calls.append(text))
        time.sleep(1.2)
    assert "second" in calls

def test_watch_clipboard_does_not_call_callback_when_no_change():
    calls = []
    with patch("src.clipboard_listener.get_clipboard", return_value="same text"):
        watch_clipboard(lambda text: calls.append(text))
        time.sleep(1.2)
    assert len(calls) == 0

