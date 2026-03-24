package com.artgallery.repository;

import com.artgallery.entity.Artwork;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface ArtworkRepository extends JpaRepository<Artwork, Long> {
    
    @Query("SELECT a FROM Artwork a WHERE " +
           "LOWER(a.title) LIKE LOWER(CONCAT('%', :keyword, '%')) OR " +
           "LOWER(a.artist.name) LIKE LOWER(CONCAT('%', :keyword, '%')) OR " +
           "LOWER(a.category) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    Page<Artwork> searchArtworks(@Param("keyword") String keyword, Pageable pageable);
}
