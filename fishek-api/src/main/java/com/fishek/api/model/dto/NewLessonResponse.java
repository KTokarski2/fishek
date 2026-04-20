package com.fishek.api.model.dto;

import lombok.Builder;

import java.time.LocalDateTime;
import java.util.List;

@Builder
public record NewLessonResponse(
        String lessonId,
        String lessonLanguage,
        LocalDateTime lessonStartedTime,
        Integer flashcardsCount,
        List<NewLessonFlashcard> flashcards
) {}
