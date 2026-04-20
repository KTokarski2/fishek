package com.fishek.api.model.dto;

import java.util.List;

public record LessonEvaluationRequest(
        String lessonId,
        List<LessonEvaluationFlashcard> flashcards
) {}
