package com.fishek.api.model.dto;


import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public record CreateFlashcardRequest(

    @NotNull
    String originalText,

    @NotNull
    String translatedPolishText,

    @NotNull
    @Pattern(regexp = "ENGLISH|FRENCH|RUSSIAN", message = "Language must be ENGLISH or FRENCH or RUSSIAN")
    String language

) {}
