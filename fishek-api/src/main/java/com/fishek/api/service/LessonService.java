package com.fishek.api.service;

import com.fishek.api.exception.ConflictException;
import com.fishek.api.exception.NotFoundException;
import com.fishek.api.handler.Sm2Handler;
import com.fishek.api.model.dto.LessonEvaluationFlashcard;
import com.fishek.api.model.dto.LessonEvaluationRequest;
import com.fishek.api.model.dto.NewLessonFlashcard;
import com.fishek.api.model.dto.NewLessonResponse;
import com.fishek.api.model.persistance.Flashcard;
import com.fishek.api.model.persistance.Lesson;
import com.fishek.api.model.persistance.LessonFlashcard;
import com.fishek.api.model.types.Language;
import com.fishek.api.repository.FlashcardRepository;
import com.fishek.api.repository.LessonRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@Transactional
@RequiredArgsConstructor
@Slf4j
public class LessonService {

    private static final String ERROR_NO_FLASHCARDS_DUE = "No flashcards due for language: ";
    private static final String ERROR_FLASHCARD_NOT_FOUND = "Flashcard not found: ";
    private static final String ERROR_LESSON_NOT_FOUND = "Lesson not found: ";
    private static final String ERROR_LESSON_ALREADY_COMPLETED = "Lesson already completed: ";

    private final LessonRepository lessonRepository;
    private final FlashcardRepository flashcardRepository;
    private final Sm2Handler sm2Handler;

    public NewLessonResponse startLesson(String language, Integer count) {
        Language lang = Language.valueOf(language);
        List<Flashcard> flashcards = flashcardRepository.findDueFlashcards(lang, LocalDate.now(), count);
        if (flashcards.isEmpty()) {
            throw new NotFoundException(ERROR_NO_FLASHCARDS_DUE + language);
        }
        Lesson lesson = buildLesson(lang, flashcards.size());
        Lesson saved = lessonRepository.save(lesson);
        return buildNewLessonResponse(saved, flashcards);
    }

    public void evaluateLesson(LessonEvaluationRequest request) {
        Lesson lesson = lessonRepository.findById(UUID.fromString(request.lessonId()))
                .orElseThrow(() -> new NotFoundException(ERROR_LESSON_NOT_FOUND + request.lessonId()));
        if (Boolean.TRUE.equals(lesson.getLessonCompleted())) {
            throw new ConflictException(ERROR_LESSON_ALREADY_COMPLETED + request.lessonId());
        }
        if (request.flashcards() == null || request.flashcards().isEmpty()) {
            return;
        }
        Map<UUID, Flashcard> flashcardMap = fetchFlashcardMap(request.flashcards());
        List<LessonFlashcard> lessonFlashcards = processEvaluations(request.flashcards(), flashcardMap, lesson);
        completeLesson(lesson, lessonFlashcards);
    }

    private Lesson buildLesson(Language language, int flashCardCount) {
        Lesson lesson = new Lesson();
        lesson.setLanguage(language);
        lesson.setFlashcardsCount(flashCardCount);
        lesson.setLessonStartedTime(LocalDateTime.now());
        lesson.setLessonCompleted(false);
        lesson.setCorrectAnswersCount(0);
        lesson.setWrongAnswersCount(0);
        return lesson;
    }

    private NewLessonResponse buildNewLessonResponse(Lesson lesson, List<Flashcard> flashcards) {
        List<NewLessonFlashcard> flashcardDtos = flashcards.stream()
                .map(f -> NewLessonFlashcard.builder()
                        .flashcardId(f.getId().toString())
                        .originalText(f.getOriginalText())
                        .translatedPolishText(f.getTranslatedPolishText())
                        .build())
                .toList();
        return NewLessonResponse.builder()
                .lessonId(lesson.getId().toString())
                .lessonLanguage(lesson.getLanguage().toString())
                .lessonStartedTime(lesson.getLessonStartedTime())
                .flashcardsCount(lesson.getFlashcardsCount())
                .flashcards(flashcardDtos)
                .build();
    }

    private Map<UUID, Flashcard> fetchFlashcardMap(List<LessonEvaluationFlashcard> evaluations) {
        List<UUID> ids = evaluations.stream()
                .map(f -> UUID.fromString(f.flashcardId()))
                .toList();
        return flashcardRepository.findAllById(ids)
                .stream()
                .collect(Collectors.toMap(Flashcard::getId, f -> f));
    }

    private List<LessonFlashcard> processEvaluations(
        List<LessonEvaluationFlashcard> evaluations,
        Map<UUID, Flashcard> flashcardMap,
        Lesson lesson
    ) {
        List<LessonFlashcard> lessonFlashcards = new ArrayList<>();
        for (LessonEvaluationFlashcard eval : evaluations) {
            UUID flashcardId = UUID.fromString(eval.flashcardId());
            Flashcard flashcard = flashcardMap.get(flashcardId);
            if (flashcard == null) {
                throw new NotFoundException(ERROR_FLASHCARD_NOT_FOUND + flashcardId);
            }
            sm2Handler.apply(flashcard, eval.correct());
            LessonFlashcard lessonFlashcard = new LessonFlashcard();
            lessonFlashcard.setLesson(lesson);
            lessonFlashcard.setFlashcard(flashcard);
            lessonFlashcard.setCorrect(eval.correct());
            lessonFlashcards.add(lessonFlashcard);
        }
        return lessonFlashcards;
    }

    private void completeLesson(Lesson lesson, List<LessonFlashcard> lessonFlashcards) {
        long correct = lessonFlashcards.stream().filter(LessonFlashcard::getCorrect).count();
        long wrong = lessonFlashcards.size() - correct;
        lesson.setLessonFlashcards(lessonFlashcards);
        lesson.setCorrectAnswersCount((int) correct);
        lesson.setWrongAnswersCount((int) wrong);
        lesson.setLessonFinishedTime(LocalDateTime.now());
        lesson.setLessonCompleted(true);
    }
}
