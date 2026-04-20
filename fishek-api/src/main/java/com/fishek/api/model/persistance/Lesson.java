package com.fishek.api.model.persistance;

import com.fishek.api.model.types.Language;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Table(name = "lessons")
@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Lesson extends AbstractJpa {

    @Column(name = "flashcards_count", nullable = false)
    private Integer flashcardsCount;

    @Column(name = "language", nullable = false)
    @Enumerated(EnumType.STRING)
    private Language language;

    @Column(name = "correct_answers_count")
    private Integer correctAnswersCount;

    @Column(name = "wrong_answers_count")
    private Integer wrongAnswersCount;

    @Column(name = "lesson_started_time")
    private LocalDateTime lessonStartedTime;

    @Column(name = "lesson_finished_time")
    private LocalDateTime lessonFinishedTime;

    @Column(name = "lesson_completed")
    private Boolean lessonCompleted;

    @OneToMany(mappedBy = "lesson", cascade = CascadeType.ALL)
    private List<LessonFlashcard> lessonFlashcards = new ArrayList<>();

}
