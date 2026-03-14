import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

def test_append_to_sheet_raises_when_no_spreadsheet_id(monkeypatch):
    monkeypatch.delenv("SPREADSHEET_ID", raising=False)
    from src.sheets_client import append_to_sheet
    with pytest.raises(ValueError):
        append_to_sheet("hello", "ENGLISH")

def test_append_to_sheet_calls_api_with_correct_values(monkeypatch):
    monkeypatch.setenv("SPREADSHEET_ID", "test_sheet_id")

    mock_service = MagicMock()
    mock_credentials = MagicMock()
    fixed_date = "2026-03-14 12:00:00"

    with patch("src.sheets_client.get_credentials", return_value=mock_credentials), \
         patch("src.sheets_client.build", return_value=mock_service), \
         patch("src.sheets_client.datetime") as mock_datetime:

        mock_datetime.now.return_value.strftime.return_value = fixed_date

        from src.sheets_client import append_to_sheet
        append_to_sheet("hello", "ENGLISH")

    mock_service.spreadsheets().values().append.assert_called_once_with(
        spreadsheetId="test_sheet_id",
        range="A:C",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [["hello", "ENGLISH", fixed_date]]}
    )

def test_append_to_sheet_calls_execute(monkeypatch):
    monkeypatch.setenv("SPREADSHEET_ID", "test_sheet_id")

    mock_service = MagicMock()
    mock_credentials = MagicMock()

    with patch("src.sheets_client.get_credentials", return_value=mock_credentials), \
         patch("src.sheets_client.build", return_value=mock_service):

        from src.sheets_client import append_to_sheet
        append_to_sheet("hello", "ENGLISH")

    mock_service.spreadsheets().values().append().execute.assert_called_once()

def test_append_to_sheet_empty_phrase(monkeypatch):
    monkeypatch.setenv("SPREADSHEET_ID", "test_sheet_id")

    mock_service = MagicMock()
    mock_credentials = MagicMock()

    with patch("src.sheets_client.get_credentials", return_value=mock_credentials), \
         patch("src.sheets_client.build", return_value=mock_service):

        from src.sheets_client import append_to_sheet
        append_to_sheet("", "ENGLISH")

    mock_service.spreadsheets().values().append().execute.assert_called_once()