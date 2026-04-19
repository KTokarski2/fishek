package com.fishek.api.service;

import com.fishek.api.model.dto.CreateFlashcardRequest;
import com.fishek.api.model.persistance.Flashcard;
import com.fishek.api.repository.FlashcardRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.assertj.core.api.Assertions.within;
import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
class FlashcardServiceTest {
    private static final String ORIGINAL_TEXT = "How are you?";
    private static final String TRANSLATED_TEXT = "Jak się masz?";
    private static final String LANGUAGE_ENGLISH = "ENGLISH";
    private static final String LANGUAGE_INVALID = "INVALID";

    @Mock
    FlashcardRepository flashcardRepository;
    @InjectMocks
    FlashcardService flashcardService;

    @Test
    void shouldSaveFlashcardWithCorrectData() {
        CreateFlashcardRequest request = new CreateFlashcardRequest(
                ORIGINAL_TEXT, TRANSLATED_TEXT, LANGUAGE_ENGLISH
        );

        flashcardService.saveNewFlashcard(request);

        ArgumentCaptor<Flashcard> captor = ArgumentCaptor.forClass(com.fishek.api.model.persistance.Flashcard.class);
        verify(flashcardRepository).save(captor.capture());

        com.fishek.api.model.persistance.Flashcard saved = captor.getValue();
        assertThat(saved.getOriginalText()).isEqualTo(ORIGINAL_TEXT);
        assertThat(saved.getTranslatedPolishText()).isEqualTo(TRANSLATED_TEXT);
        assertThat(saved.getFlashcardLanguage().name()).isEqualTo(LANGUAGE_ENGLISH);
    }

    @Test
    void shouldThrowForInvalidLanguage() {
        CreateFlashcardRequest request = new CreateFlashcardRequest(
                ORIGINAL_TEXT, TRANSLATED_TEXT, LANGUAGE_INVALID
        );

        assertThatThrownBy(() -> flashcardService.saveNewFlashcard(request))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void shouldAssignDefaultValuesToSrsFields() {
        CreateFlashcardRequest request = new CreateFlashcardRequest(
                ORIGINAL_TEXT, TRANSLATED_TEXT, LANGUAGE_ENGLISH
        );
        flashcardService.saveNewFlashcard(request);
        ArgumentCaptor<com.fishek.api.model.persistance.Flashcard> captor = ArgumentCaptor.forClass(com.fishek.api.model.persistance.Flashcard.class);
        verify(flashcardRepository).save(captor.capture());
        com.fishek.api.model.persistance.Flashcard saved = captor.getValue();
        assertThat(saved.getRepetitions()).isEqualTo(0);
        assertThat(saved.getEaseFactor()).isEqualTo(2.5);
        assertThat(saved.getIntervalDays()).isEqualTo(0);
        assertThat(saved.getDueDate()).isCloseTo(LocalDate.now(), within(1, ChronoUnit.DAYS));
    }
}
