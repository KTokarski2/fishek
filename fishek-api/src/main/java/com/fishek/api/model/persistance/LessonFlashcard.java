package com.fishek.api.model.persistance;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Table(name = "lesson_flashcards")
@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class LessonFlashcard extends AbstractJpa {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "lesson_id", nullable = false)
    private Lesson lesson;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "flashcard_id", nullable = false)
    private Flashcard flashcard;

    @Column(name = "correct", nullable = false)
    private Boolean correct;
}
