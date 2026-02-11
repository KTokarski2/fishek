package com.fishek.api.service;

import com.fishek.api.model.dto.CreateFlashcardRequest;
import com.fishek.api.model.persistance.Flashcard;
import com.fishek.api.model.types.FlashcardLanguage;
import com.fishek.api.repository.FlashcardRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
@RequiredArgsConstructor
@Slf4j
public class FlashcardService {

    private final FlashcardRepository flashcardRepository;

    public void saveNewFlashcard(CreateFlashcardRequest flashcardRequest) {
        flashcardRepository.save(createFlashcardEntity(flashcardRequest));
    }

    private Flashcard createFlashcardEntity(CreateFlashcardRequest request) {
        return Flashcard.builder()
                .originalText(request.text())
                .flashcardLanguage(FlashcardLanguage.valueOf(request.language()))
                .build();
    }

}
