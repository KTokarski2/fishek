CREATE TABLE lessons (
    id                    UUID                        NOT NULL,
    created_at            TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at            TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    flashcards_count       INT                         NOT NULL,
    language              VARCHAR(255)                NOT NULL,
    correct_answers_count INT,
    wrong_answers_count   INT,
    lesson_started_time   TIMESTAMP WITHOUT TIME ZONE,
    lesson_finished_time  TIMESTAMP WITHOUT TIME ZONE,

    CONSTRAINT pk_lessons PRIMARY KEY (id)
);

CREATE TABLE lesson_flashcards (
    id           UUID                        NOT NULL,
    created_at   TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at   TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    lesson_id    UUID                        NOT NULL,
    flashcard_id UUID                        NOT NULL,
    correct      BOOLEAN                     NOT NULL,

    CONSTRAINT pk_lesson_flashcards PRIMARY KEY (id),
    CONSTRAINT fk_lesson_flashcards_lesson
                               FOREIGN KEY (lesson_id)
                               REFERENCES lessons (id),
    CONSTRAINT fk_lesson_flashcards_flashcard
                               FOREIGN KEY (flashcard_id)
                               REFERENCES flashcards (id)
);