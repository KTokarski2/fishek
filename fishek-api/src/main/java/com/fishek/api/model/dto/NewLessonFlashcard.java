package com.fishek.api.model.dto;

import lombok.Builder;

@Builder
public record NewLessonFlashcard(
        String flashcardId,
        String originalText,
        String translatedPolishText
) {}
