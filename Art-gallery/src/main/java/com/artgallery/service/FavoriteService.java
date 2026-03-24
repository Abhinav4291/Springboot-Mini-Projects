package com.artgallery.service;

import com.artgallery.entity.Artwork;
import com.artgallery.entity.Favorite;
import com.artgallery.entity.FavoriteId;
import com.artgallery.entity.User;
import com.artgallery.repository.ArtworkRepository;
import com.artgallery.repository.FavoriteRepository;
import com.artgallery.repository.UserRepository;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class FavoriteService {

    private final FavoriteRepository favoriteRepository;
    private final UserRepository userRepository;
    private final ArtworkRepository artworkRepository;

    public FavoriteService(FavoriteRepository favoriteRepository, UserRepository userRepository, ArtworkRepository artworkRepository) {
        this.favoriteRepository = favoriteRepository;
        this.userRepository = userRepository;
        this.artworkRepository = artworkRepository;
    }

    public List<Artwork> getUserFavorites(String email) {
        User user = userRepository.findByEmail(email).orElseThrow();
        return favoriteRepository.findByUserId(user.getId()).stream()
                .map(Favorite::getArtwork)
                .collect(Collectors.toList());
    }

    public boolean isFavorite(Long artworkId, String email) {
        if (email == null) return false;
        return userRepository.findByEmail(email)
                .map(u -> favoriteRepository.existsByUserIdAndArtworkId(u.getId(), artworkId))
                .orElse(false);
    }

    public void toggleFavorite(Long artworkId, String email) {
        User user = userRepository.findByEmail(email).orElseThrow();
        Artwork artwork = artworkRepository.findById(artworkId).orElseThrow();
        
        if (favoriteRepository.existsByUserIdAndArtworkId(user.getId(), artworkId)) {
            favoriteRepository.deleteById(new FavoriteId(user.getId(), artworkId));
        } else {
            favoriteRepository.save(new Favorite(user, artwork));
        }
    }
}
