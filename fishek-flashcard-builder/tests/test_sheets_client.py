import sys
import os
import pickle
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# get_config_dir
# ---------------------------------------------------------------------------

def test_get_config_dir_linux():
    from services.sheets_client import get_config_dir

    with patch.object(sys, "platform", "linux"):
        result = get_config_dir()

    assert result == os.path.join(os.path.expanduser("~"), ".config", "fishek")


def test_get_config_dir_windows():
    from services.sheets_client import get_config_dir

    with patch.dict(os.environ, {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"}), \
         patch.object(sys, "platform", "win32"):
        result = get_config_dir()

    assert result.endswith("fishek")
    assert "Roaming" in result


# ---------------------------------------------------------------------------
# get_sheet_data — header stripping
# ---------------------------------------------------------------------------

def _mock_sheets_service(values):
    service = MagicMock()
    (service.spreadsheets.return_value
     .values.return_value
     .get.return_value
     .execute.return_value) = {"values": values}
    return service


def test_get_sheet_data_strips_header_row():
    from services.sheets_client import get_sheet_data

    raw = [
        ["word", "language", "created"],
        ["cat", "english", "2026-01-01"],
        ["dog", "english", "2026-01-02"],
    ]

    with patch.dict(os.environ, {"SPREADSHEET_ID": "sheet123"}), \
         patch("services.sheets_client.get_credentials", return_value=MagicMock()), \
         patch("services.sheets_client.build", return_value=_mock_sheets_service(raw)):
        result = get_sheet_data()

    assert result == [["cat", "english", "2026-01-01"], ["dog", "english", "2026-01-02"]]


def test_get_sheet_data_keeps_rows_without_header():
    from services.sheets_client import get_sheet_data

    raw = [
        ["cat", "english", "2026-01-01"],
        ["dog", "english", "2026-01-02"],
    ]

    with patch.dict(os.environ, {"SPREADSHEET_ID": "sheet123"}), \
         patch("services.sheets_client.get_credentials", return_value=MagicMock()), \
         patch("services.sheets_client.build", return_value=_mock_sheets_service(raw)):
        result = get_sheet_data()

    assert result == raw


def test_get_sheet_data_returns_empty_for_no_values():
    from services.sheets_client import get_sheet_data

    with patch.dict(os.environ, {"SPREADSHEET_ID": "sheet123"}), \
         patch("services.sheets_client.get_credentials", return_value=MagicMock()), \
         patch("services.sheets_client.build", return_value=_mock_sheets_service([])):
        result = get_sheet_data()

    assert result == []


def test_get_sheet_data_raises_without_spreadsheet_id():
    from services.sheets_client import get_sheet_data

    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("SPREADSHEET_ID", None)
        with pytest.raises(ValueError, match="Spreadsheet ID not found"):
            get_sheet_data()


# ---------------------------------------------------------------------------
# get_credentials — token caching
# ---------------------------------------------------------------------------

def test_get_credentials_loads_valid_token(tmp_path):
    from services.sheets_client import get_credentials

    mock_creds = MagicMock()
    mock_creds.valid = True
    token_file = tmp_path / "token.pickle"

    with patch("services.sheets_client.TOKEN_PATH", token_file), \
         patch("os.path.exists", return_value=True), \
         patch("pickle.load", return_value=mock_creds), \
         patch("builtins.open", MagicMock()):
        result = get_credentials()

    assert result is mock_creds


def test_get_credentials_refreshes_expired_token(tmp_path):
    from services.sheets_client import get_credentials

    mock_creds = MagicMock()
    mock_creds.valid = False
    mock_creds.expired = True
    mock_creds.refresh_token = "refresh_tok"
    token_file = tmp_path / "token.pickle"

    with patch("services.sheets_client.TOKEN_PATH", token_file), \
         patch("os.path.exists", return_value=True), \
         patch("pickle.load", return_value=mock_creds), \
         patch("pickle.dump"), \
         patch("builtins.open", MagicMock()), \
         patch("services.sheets_client.Request"):
        result = get_credentials()

    mock_creds.refresh.assert_called_once()
    assert result is mock_creds
