package com.fishek.api.model.persistence;

import jakarta.persistence.*;
import lombok.*;

@Table(name = "lesson_flashcards")
@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LessonFlashcard extends AbstractJpa {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "lesson_id", nullable = false)
    private Lesson lesson;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "flashcard_id", nullable = false)
    private Flashcard flashcard;

    @Column(name = "correct")
    private Boolean correct;
}
