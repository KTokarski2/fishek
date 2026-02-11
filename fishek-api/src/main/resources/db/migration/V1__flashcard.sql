CREATE TABLE flashcard
(
    id                      UUID                         NOT NULL,
    created_at              TIMESTAMP WITHOUT TIME ZONE  NOT NULL,
    updated_at              TIMESTAMP WITHOUT TIME ZONE  NOT NULL,
    original_text           VARCHAR(255)                 NOT NULL,
    translated_polish_text  VARCHAR(255),
    flashcard_language      VARCHAR(255)                 NOT NULL,

    CONSTRAINT pk_flashcard PRIMARY KEY (id)
);