package com.fishek.api.model.dto;


import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public record CreateFlashcardRequest(
    @NotNull
    String text,

    @NotNull
    @Pattern(regexp = "ENGLISH|FRENCH", message = "Language must be ENGLISH or FRENCH")
    String language
) {}
