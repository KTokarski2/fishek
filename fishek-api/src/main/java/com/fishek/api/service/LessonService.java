package com.fishek.api.service;

import com.fishek.api.exception.BadRequestException;
import com.fishek.api.exception.ConflictException;
import com.fishek.api.exception.NotFoundException;
import com.fishek.api.handler.Sm2Handler;
import com.fishek.api.model.dto.LessonEvaluationFlashcard;
import com.fishek.api.model.dto.LessonEvaluationRequest;
import com.fishek.api.model.dto.NewLessonFlashcard;
import com.fishek.api.model.dto.NewLessonResponse;
import com.fishek.api.model.persistence.Flashcard;
import com.fishek.api.model.persistence.Lesson;
import com.fishek.api.model.persistence.LessonFlashcard;
import com.fishek.api.model.types.Language;
import com.fishek.api.repository.FlashcardRepository;
import com.fishek.api.repository.LessonRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;
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
    private static final String ERROR_FLASHCARD_NOT_ANSWERED = "Some flashcard not answered: ";

    private final LessonRepository lessonRepository;
    private final FlashcardRepository flashcardRepository;
    private final Sm2Handler sm2Handler;

    public NewLessonResponse startLesson(String language, Integer count) {
        Language lang = Language.valueOf(language);
        List<Flashcard> flashcards = flashcardRepository.findDueFlashcards(lang, LocalDate.now(), count);
        if (flashcards.isEmpty()) {
            throw new NotFoundException(ERROR_NO_FLASHCARDS_DUE + language);
        }
        Lesson lesson = buildLesson(lang, flashcards);
        Lesson saved = lessonRepository.save(lesson);
        return buildNewLessonResponse(saved, flashcards);
    }

    public void evaluateLesson(String lessonId, LessonEvaluationRequest request) {
        Lesson lesson = lessonRepository.findById(UUID.fromString(lessonId))
                .orElseThrow(() -> new NotFoundException(ERROR_LESSON_NOT_FOUND + lessonId));
        if (Boolean.TRUE.equals(lesson.getLessonCompleted())) {
            throw new ConflictException(ERROR_LESSON_ALREADY_COMPLETED + lessonId);
        }
        if (request.flashcards() == null || request.flashcards().isEmpty()) {
            return;
        }
        Map<UUID, Flashcard> flashcardMap = fetchFlashcardMap(request.flashcards());
        processEvaluations(request.flashcards(), flashcardMap, lesson);
        checkIfAllFlashcardsAnswered(lesson);
        completeLesson(lesson);
    }

    private Lesson buildLesson(Language language, List<Flashcard> flashcards) {
        Lesson lesson = new Lesson();
        lesson.setLanguage(language);
        lesson.setFlashcardsCount(flashcards.size());
        lesson.setLessonStartedTime(LocalDateTime.now());
        lesson.setLessonCompleted(false);
        lesson.setCorrectAnswersCount(0);
        lesson.setWrongAnswersCount(0);
        lesson.getLessonFlashcards().addAll(createLessonFlashcards(flashcards, lesson));
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

    private void processEvaluations(
        List<LessonEvaluationFlashcard> evaluations,
        Map<UUID, Flashcard> flashcardMap,
        Lesson lesson
    ) {
        for (LessonEvaluationFlashcard eval : evaluations) {
            UUID flashcardId = UUID.fromString(eval.flashcardId());
            Flashcard flashcard = flashcardMap.get(flashcardId);
            if (flashcard == null) {
                throw new NotFoundException(ERROR_FLASHCARD_NOT_FOUND + flashcardId);
            }
            sm2Handler.apply(flashcard, eval.correct());

            LessonFlashcard lessonFlashcard = lesson.getLessonFlashcards()
                    .stream()
                    .filter(lf -> lf.getFlashcard().getId().equals(flashcard.getId()))
                    .findAny()
                    .orElseThrow(() -> new NotFoundException(ERROR_FLASHCARD_NOT_FOUND + flashcard.getId()));
            lessonFlashcard.setCorrect(eval.correct());
        }
    }

    private void completeLesson(Lesson lesson) {
        long correct = lesson.getLessonFlashcards().stream()
                .filter(lf -> Boolean.TRUE.equals(lf.getCorrect()))
                .count();
        long wrong = lesson.getLessonFlashcards().size() - correct;
        lesson.setCorrectAnswersCount((int) correct);
        lesson.setWrongAnswersCount((int) wrong);
        lesson.setLessonFinishedTime(LocalDateTime.now());
        lesson.setLessonCompleted(true);
    }

    private List<LessonFlashcard> createLessonFlashcards(List<Flashcard> flashcards, Lesson lesson) {
        return flashcards.stream()
                .map(flashcard -> LessonFlashcard.builder()
                        .flashcard(flashcard)
                        .lesson(lesson)
                        .build()
                )
                .toList();
    }

    private void checkIfAllFlashcardsAnswered(Lesson lesson) {
        lesson.getLessonFlashcards().forEach(lessonFlashcard -> {
            if (lessonFlashcard.getCorrect() == null) {
                throw new BadRequestException(
                        ERROR_FLASHCARD_NOT_ANSWERED + lessonFlashcard.getFlashcard().getId()
                );
            }
        });
    }
}
