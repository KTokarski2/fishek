package com.fishek.api.rest.controller;

import com.fishek.api.model.dto.CreateFlashcardRequest;
import com.fishek.api.service.FlashcardService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/flashcard")
@RequiredArgsConstructor
public class FlashcardController {

    private final FlashcardService flashcardService;

    @PostMapping
    public ResponseEntity<Void> addFlashcard(@RequestBody CreateFlashcardRequest request) {
        flashcardService.saveNewFlashcard(request);
        return ResponseEntity.ok().build();
    }
}
