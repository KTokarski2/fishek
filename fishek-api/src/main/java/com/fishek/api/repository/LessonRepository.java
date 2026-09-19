package com.fishek.api.repository;

import com.fishek.api.model.persistence.Lesson;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface LessonRepository extends JpaRepository<Lesson, UUID> {

    @Query("""
        SELECT l FROM Lesson l
        JOIN FETCH l.lessonFlashcards lf
        JOIN FETCH lf.flashcard
        WHERE l.id = :lessonId
        """)
    Optional<Lesson> findByIdWithLessonFlashcards(@Param("lessonId") UUID lessonId);
}
