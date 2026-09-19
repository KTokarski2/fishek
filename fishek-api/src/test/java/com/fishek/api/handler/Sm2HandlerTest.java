package com.fishek.api.handler;

import com.fishek.api.model.persistence.Flashcard;
import com.fishek.api.model.types.Language;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.within;

@ExtendWith(MockitoExtension.class)
public class Sm2HandlerTest {

    private static final UUID FLASHCARD_ID = UUID.randomUUID();

    Sm2Handler sm2Handler = new Sm2Handler();

    @Test
    void shouldIncrementRepetitionsOnCorrectAnswer() {
        Flashcard card = buildFlashcard(0, 2.5, 0);

        sm2Handler.apply(card, true);

        assertThat(card.getRepetitions()).isEqualTo(1);
    }

    @Test
    void shouldSetIntervalToOneOnFirstCorrectAnswer() {
        Flashcard card = buildFlashcard(0, 2.5, 0);

        sm2Handler.apply(card, true);

        assertThat(card.getIntervalDays()).isEqualTo(1);
    }

    @Test
    void shouldSetIntervalToSixOnSecondCorrectAnswer() {
        Flashcard card = buildFlashcard(1, 2.5, 1);

        sm2Handler.apply(card, true);

        assertThat(card.getIntervalDays()).isEqualTo(6);
    }

    @Test
    void shouldMultiplyIntervalByEaseFactorOnThirdCorrectAnswer() {
        Flashcard card = buildFlashcard(2, 2.5, 6);

        sm2Handler.apply(card, true);

        assertThat(card.getIntervalDays()).isEqualTo(15);
    }

    @Test
    void shouldIncreaseEaseFactorOnCorrectAnswer() {
        Flashcard card = buildFlashcard(0, 2.5, 0);

        sm2Handler.apply(card, true);

        assertThat(card.getEaseFactor()).isEqualTo(2.6);
    }

    @Test
    void shouldSetDueDateTodayPlusIntervalOnCorrectAnswer() {
        Flashcard card = buildFlashcard(0, 2.5, 0);

        sm2Handler.apply(card, true);

        assertThat(card.getDueDate()).isEqualTo(LocalDate.now().plusDays(1));
    }

    @Test
    void shouldUpdateLastReviewedOnCorrectAnswer() {
        Flashcard card = buildFlashcard(0, 2.5, 0);

        sm2Handler.apply(card, true);

        assertThat(card.getLastReviewed()).isCloseTo(LocalDateTime.now(), within(1, ChronoUnit.SECONDS));
    }

    @Test
    void shouldResetRepetitionsOnWrongAnswer() {
        Flashcard card = buildFlashcard(3, 2.5, 15);

        sm2Handler.apply(card, false);

        assertThat(card.getRepetitions()).isEqualTo(0);
    }

    @Test
    void shouldResetIntervalToOneOnWrongAnswer() {
        Flashcard card = buildFlashcard(3, 2.5, 15);

        sm2Handler.apply(card, false);

        assertThat(card.getIntervalDays()).isEqualTo(1);
    }

    @Test
    void shouldDecreaseEaseFactorOnWrongAnswer() {
        Flashcard card = buildFlashcard(0, 2.5, 0);

        sm2Handler.apply(card, false);

        assertThat(card.getEaseFactor()).isCloseTo(1.96, within(0.01));
    }

    @Test
    void shouldNotDropEaseFactorBelowMinimumOnWrongAnswer() {
        Flashcard card = buildFlashcard(0, 1.3, 0);

        sm2Handler.apply(card, false);

        assertThat(card.getEaseFactor()).isEqualTo(1.3);
    }

    @Test
    void shouldSetDueDateTomorrowOnWrongAnswer() {
        Flashcard card = buildFlashcard(3, 2.5, 15);

        sm2Handler.apply(card, false);

        assertThat(card.getDueDate()).isEqualTo(LocalDate.now().plusDays(1));
    }

    @Test
    void shouldRememberReducedEaseFactorAfterReset() {
        Flashcard card = buildFlashcard(3, 2.5, 15);

        sm2Handler.apply(card, false);
        sm2Handler.apply(card, true);
        sm2Handler.apply(card, true);
        sm2Handler.apply(card, true);

        assertThat(card.getEaseFactor()).isLessThan(2.5);
    }

    private Flashcard buildFlashcard(int repetitions, double easeFactor, int intervalDays) {
        Flashcard f = new Flashcard();
        f.setId(FLASHCARD_ID);
        f.setOriginalText("Hello");
        f.setTranslatedPolishText("Cześć");
        f.setLanguage(Language.ENGLISH);
        f.setRepetitions(repetitions);
        f.setEaseFactor(easeFactor);
        f.setIntervalDays(intervalDays);
        f.setDueDate(LocalDate.now());
        f.setLastReviewed(LocalDateTime.now());
        return f;
    }
}
