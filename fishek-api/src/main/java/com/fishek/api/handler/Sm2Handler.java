package com.fishek.api.handler;

import com.fishek.api.model.persistance.Flashcard;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Component
public class Sm2Handler {

    public void apply(Flashcard card, boolean correct) {
        int grade = correct ? 5 : 1;
        if (grade < 3) {
            card.setRepetitions(0);
            card.setIntervalDays(1);
        } else {
            switch (card.getRepetitions()) {
                case 0 -> card.setIntervalDays(1);
                case 1 -> card.setIntervalDays(6);
                default -> card.setIntervalDays(
                        (int) Math.round(card.getIntervalDays() * card.getEaseFactor())
                );
            }
            card.setRepetitions(card.getRepetitions() + 1);
        }
        double newEF = card.getEaseFactor()
                + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02));
        card.setEaseFactor(Math.max(1.3, newEF));
        card.setDueDate(LocalDate.now().plusDays(card.getIntervalDays()));
        card.setLastReviewed(LocalDateTime.now());
    }
}
