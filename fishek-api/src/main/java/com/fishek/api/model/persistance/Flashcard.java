package com.fishek.api.model.persistance;

import com.fishek.api.model.types.FlashcardLanguage;
import jakarta.persistence.*;
import lombok.*;

@Table(name = "flashcard")
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
}
