package com.artgallery.repository;

import com.artgallery.entity.Favorite;
import com.artgallery.entity.FavoriteId;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface FavoriteRepository extends JpaRepository<Favorite, FavoriteId> {
    List<Favorite> findByUserId(Long userId);
    boolean existsByUserIdAndArtworkId(Long userId, Long artworkId);
}
