package com.fishek.api.model.persistance;

import com.fishek.api.model.types.FlashcardLanguage;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Table(name = "flashcards")
@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Flashcard extends AbstractJpa {

    @Column(name = "original_text", nullable = false)
    private String originalText;

    @Column(name = "translated_polish_text")
    private String translatedPolishText;

    @Column(name = "flashcard_language", nullable = false)
    @Enumerated(EnumType.STRING)
    private FlashcardLanguage flashcardLanguage;

    //SRS fields
    @Column(name = "repetitions", nullable = false)
    private Integer repetitions;

    @Column(name = "ease_factor", nullable = false)
    private Double easeFactor;

    @Column(name = "interval_days", nullable = false)
    private Integer intervalDays;

    @Column(name = "due_date", nullable = false)
    private LocalDate dueDate;

    @Column(name = "last_reviewed", nullable = false)
    private LocalDateTime lastReviewed;
}
