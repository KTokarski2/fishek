package com.fishek.api.repository;

import com.fishek.api.model.persistence.Flashcard;
import com.fishek.api.model.types.Language;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Repository
public interface FlashcardRepository extends JpaRepository<Flashcard, UUID> {

    @Query("""
        SELECT f FROM Flashcard f
        WHERE f.language = :language
        AND f.dueDate <= :today
        ORDER BY f.dueDate ASC
        LIMIT :count
        """)
    List<Flashcard> findDueFlashcards(
            @Param("language") Language language,
            @Param("today") LocalDate today,
            @Param("count") Integer count
    );
}
