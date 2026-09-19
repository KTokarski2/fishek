package com.fishek.api.rest.controller;

import com.fishek.api.model.dto.LessonEvaluationRequest;
import com.fishek.api.model.dto.NewLessonResponse;
import com.fishek.api.service.LessonService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/lesson")
@RequiredArgsConstructor
public class LessonController {

    private final LessonService lessonService;

    @PostMapping("/new")
    public ResponseEntity<NewLessonResponse> startLesson(
            @RequestParam String language,
            @RequestParam Integer count
    ) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(lessonService.startLesson(language, count));
    }

    @PostMapping("/{lessonId}/evaluate")
    public ResponseEntity<Void> evaluateLesson(
            @PathVariable String lessonId,
            @RequestBody LessonEvaluationRequest request
    ) {
        lessonService.evaluateLesson(lessonId, request);
        return ResponseEntity.ok().build();
    }
}
