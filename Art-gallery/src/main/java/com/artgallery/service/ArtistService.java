package com.artgallery.service;

import com.artgallery.entity.Artist;
import com.artgallery.repository.ArtistRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class ArtistService {
    private final ArtistRepository artistRepository;

    public ArtistService(ArtistRepository artistRepository) {
        this.artistRepository = artistRepository;
    }

    public List<Artist> findAll() {
        return artistRepository.findAll();
    }
}
