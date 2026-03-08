package com.fishek.google;

import com.google.api.services.sheets.v4.Sheets;
import com.google.api.services.sheets.v4.model.ValueRange;

import java.time.LocalDateTime;
import java.util.List;

public class SheetsService {

    private static final String SPREADSHEET_ID = "1yvLKlUawEPnOFeSp9j9Qo0vJiwbjkPuRA4zfhCgkAsY";

    public static void append(String lang, String text) throws Exception {
        Sheets sheets = GoogleAuth.getSheetsService();
        List<List<Object>> values = List.of(List.of(
                LocalDateTime.now().toString(),
                lang,
                text
        ));
        ValueRange body = new ValueRange().setValues(values);
        sheets.spreadsheets()
                .values()
                .append(SPREADSHEET_ID, "Flashcards!A1:C1", body)
                .setValueInputOption("RAW")
                .setInsertDataOption("INSERT_ROWS")
                .execute();
    }


}
