package com.fishek.api.service;

import com.fishek.api.exception.ConflictException;
import com.fishek.api.exception.NotFoundException;
import com.fishek.api.handler.Sm2Handler;
import com.fishek.api.model.dto.LessonEvaluationFlashcard;
import com.fishek.api.model.dto.LessonEvaluationRequest;
import com.fishek.api.model.dto.NewLessonResponse;
import com.fishek.api.model.persistance.Flashcard;
import com.fishek.api.model.persistance.Lesson;
import com.fishek.api.model.types.Language;
import com.fishek.api.repository.FlashcardRepository;
import com.fishek.api.repository.LessonRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class LessonServiceTest {

    private static final String LANGUAGE = "ENGLISH";
    private static final int COUNT = 10;
    private static final UUID LESSON_ID = UUID.randomUUID();
    private static final UUID FLASHCARD_ID = UUID.randomUUID();

    @Mock
    LessonRepository lessonRepository;

    @Mock
    FlashcardRepository flashcardRepository;

    @Mock
    Sm2Handler sm2Handler;

    @InjectMocks
    LessonService lessonService;

    @Test
    void shouldReturnNewLessonResponseWhenFlashcardsFound() {
        List<Flashcard> flashcards = List.of(buildFlashcard(FLASHCARD_ID));
        when(flashcardRepository.findDueFlashcards(Language.ENGLISH, LocalDate.now(), COUNT))
                .thenReturn(flashcards);
        when(lessonRepository.save(any())).thenAnswer(inv -> {
            Lesson l = inv.getArgument(0);
            l.setId(LESSON_ID);
            return l;
        });

        NewLessonResponse response = lessonService.startLesson(LANGUAGE, COUNT);

        assertThat(response.lessonId()).isEqualTo(LESSON_ID.toString());
        assertThat(response.lessonLanguage()).isEqualTo(LANGUAGE);
        assertThat(response.flashcardsCount()).isEqualTo(1);
        assertThat(response.flashcards()).hasSize(1);
        assertThat(response.flashcards().getFirst().flashcardId()).isEqualTo(FLASHCARD_ID.toString());
    }

    @Test
    void shouldThrowNotFoundExceptionWhenNoFlashcardsDue() {
        when(flashcardRepository.findDueFlashcards(any(), any(), any()))
                .thenReturn(List.of());

        assertThatThrownBy(() -> lessonService.startLesson(LANGUAGE, COUNT))
                .isInstanceOf(NotFoundException.class);
    }

    @Test
    void shouldThrowIllegalArgumentExceptionWhenLanguageInvalid() {
        assertThatThrownBy(() -> lessonService.startLesson("INVALID", COUNT))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void shouldSaveLessonWithCorrectInitialValues() {
        when(flashcardRepository.findDueFlashcards(any(), any(), any()))
                .thenReturn(List.of(buildFlashcard(FLASHCARD_ID)));
        when(lessonRepository.save(any())).thenAnswer(inv -> {
            Lesson l = inv.getArgument(0);
            l.setId(LESSON_ID);
            return l;
        });

        lessonService.startLesson(LANGUAGE, COUNT);

        ArgumentCaptor<Lesson> captor = ArgumentCaptor.forClass(Lesson.class);
        verify(lessonRepository).save(captor.capture());
        Lesson saved = captor.getValue();

        assertThat(saved.getLessonCompleted()).isFalse();
        assertThat(saved.getCorrectAnswersCount()).isZero();
        assertThat(saved.getWrongAnswersCount()).isZero();
        assertThat(saved.getLessonStartedTime()).isCloseTo(LocalDateTime.now(), within(1, ChronoUnit.SECONDS));
        assertThat(saved.getLanguage()).isEqualTo(Language.ENGLISH);
        assertThat(saved.getFlashcardsCount()).isEqualTo(1);
    }

    @Test
    void shouldCompleteLessonWithCorrectStats() {
        Lesson lesson = buildLesson(false);
        Flashcard flashcard = buildFlashcard(FLASHCARD_ID);
        LessonEvaluationRequest request = buildRequest(List.of(
                new LessonEvaluationFlashcard(FLASHCARD_ID.toString(), true)
        ));

        when(lessonRepository.findById(LESSON_ID)).thenReturn(Optional.of(lesson));
        when(flashcardRepository.findAllById(any())).thenReturn(List.of(flashcard));

        lessonService.evaluateLesson(request);

        assertThat(lesson.getLessonCompleted()).isTrue();
        assertThat(lesson.getCorrectAnswersCount()).isEqualTo(1);
        assertThat(lesson.getWrongAnswersCount()).isEqualTo(0);
        assertThat(lesson.getLessonFinishedTime()).isNotNull();
    }

    @Test
    void shouldApplySm2ForEachFlashcard() {
        Flashcard flashcard = buildFlashcard(FLASHCARD_ID);
        Lesson lesson = buildLesson(false);
        LessonEvaluationRequest request = buildRequest(List.of(
                new LessonEvaluationFlashcard(FLASHCARD_ID.toString(), true)
        ));

        when(lessonRepository.findById(LESSON_ID)).thenReturn(Optional.of(lesson));
        when(flashcardRepository.findAllById(any())).thenReturn(List.of(flashcard));

        lessonService.evaluateLesson(request);

        verify(sm2Handler).apply(flashcard, true);
    }

    @Test
    void shouldCountCorrectAndWrongAnswers() {
        UUID id1 = UUID.randomUUID();
        UUID id2 = UUID.randomUUID();
        UUID id3 = UUID.randomUUID();

        Lesson lesson = buildLesson(false);
        List<Flashcard> flashcards = List.of(
                buildFlashcard(id1),
                buildFlashcard(id2),
                buildFlashcard(id3)
        );
        LessonEvaluationRequest request = buildRequest(List.of(
                new LessonEvaluationFlashcard(id1.toString(), true),
                new LessonEvaluationFlashcard(id2.toString(), false),
                new LessonEvaluationFlashcard(id3.toString(), true)
        ));

        when(lessonRepository.findById(LESSON_ID)).thenReturn(Optional.of(lesson));
        when(flashcardRepository.findAllById(any())).thenReturn(flashcards);

        lessonService.evaluateLesson(request);

        assertThat(lesson.getCorrectAnswersCount()).isEqualTo(2);
        assertThat(lesson.getWrongAnswersCount()).isEqualTo(1);
    }

    @Test
    void shouldThrowNotFoundExceptionWhenLessonNotFound() {
        when(lessonRepository.findById(any())).thenReturn(Optional.empty());

        assertThatThrownBy(() -> lessonService.evaluateLesson(buildRequest(List.of())))
                .isInstanceOf(NotFoundException.class);
    }

    @Test
    void shouldThrowConflictExceptionWhenLessonAlreadyCompleted() {
        when(lessonRepository.findById(LESSON_ID)).thenReturn(Optional.of(buildLesson(true)));

        assertThatThrownBy(() -> lessonService.evaluateLesson(buildRequest(List.of())))
                .isInstanceOf(ConflictException.class);
    }

    @Test
    void shouldThrowNotFoundExceptionWhenFlashcardNotInMap() {
        Lesson lesson = buildLesson(false);
        LessonEvaluationRequest request = buildRequest(List.of(
                new LessonEvaluationFlashcard(FLASHCARD_ID.toString(), true)
        ));

        when(lessonRepository.findById(LESSON_ID)).thenReturn(Optional.of(lesson));
        when(flashcardRepository.findAllById(any())).thenReturn(List.of());

        assertThatThrownBy(() -> lessonService.evaluateLesson(request))
                .isInstanceOf(NotFoundException.class);
    }

    @Test
    void shouldDoNothingWhenFlashcardsListIsEmpty() {
        Lesson lesson = buildLesson(false);
        when(lessonRepository.findById(LESSON_ID)).thenReturn(Optional.of(lesson));

        lessonService.evaluateLesson(buildRequest(List.of()));

        assertThat(lesson.getLessonCompleted()).isFalse();
        verify(sm2Handler, never()).apply(any(), anyBoolean());
    }

    private Flashcard buildFlashcard(UUID id) {
        Flashcard f = new Flashcard();
        f.setId(id);
        f.setOriginalText("Hello");
        f.setTranslatedPolishText("Cześć");
        f.setLanguage(Language.ENGLISH);
        f.setRepetitions(0);
        f.setEaseFactor(2.5);
        f.setIntervalDays(0);
        f.setDueDate(LocalDate.now());
        f.setLastReviewed(LocalDateTime.now());
        return f;
    }

    private Lesson buildLesson(boolean completed) {
        Lesson l = new Lesson();
        l.setId(LESSON_ID);
        l.setLanguage(Language.ENGLISH);
        l.setFlashcardsCount(1);
        l.setLessonCompleted(completed);
        l.setCorrectAnswersCount(0);
        l.setWrongAnswersCount(0);
        l.setLessonStartedTime(LocalDateTime.now());
        return l;
    }

    private LessonEvaluationRequest buildRequest(List<LessonEvaluationFlashcard> flashcards) {
        return new LessonEvaluationRequest(LESSON_ID.toString(), flashcards);
    }
}
