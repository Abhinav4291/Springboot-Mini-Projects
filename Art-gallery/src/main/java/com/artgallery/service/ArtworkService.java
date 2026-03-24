package com.artgallery.service;

import com.artgallery.entity.Artist;
import com.artgallery.entity.Artwork;
import com.artgallery.repository.ArtistRepository;
import com.artgallery.repository.ArtworkRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.UUID;

@Service
public class ArtworkService {

    private final ArtworkRepository artworkRepository;
    private final ArtistRepository artistRepository;

    public ArtworkService(ArtworkRepository artworkRepository, ArtistRepository artistRepository) {
        this.artworkRepository = artworkRepository;
        this.artistRepository = artistRepository;
    }

    public List<Artwork> findAll() {
        return artworkRepository.findAll();
    }

    public Page<Artwork> findPaginatedAndSorted(int page, int size, String keyword) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("id").descending());
        if (keyword != null && !keyword.isEmpty()) {
            return artworkRepository.searchArtworks(keyword, pageable);
        }
        return artworkRepository.findAll(pageable);
    }

    public Artwork findById(Long id) {
        return artworkRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Artwork not found"));
    }

    private String saveImage(MultipartFile imageFile) {
        if (imageFile == null || imageFile.isEmpty()) return null;
        try {
            String uploadDir = "uploads/";
            Path uploadPath = Paths.get(uploadDir);
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }
            String filename = UUID.randomUUID().toString() + "_" + imageFile.getOriginalFilename().replaceAll("[^a-zA-Z0-9\\.\\-]", "_");
            Path filePath = uploadPath.resolve(filename);
            Files.copy(imageFile.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
            return "/uploads/" + filename;
        } catch (Exception e) {
            throw new RuntimeException("Could not store image file", e);
        }
    }

    public void save(Artwork artwork, String artistName, MultipartFile imageFile) {
        Artist artist = artistRepository.findByName(artistName).orElseGet(() -> {
            Artist newArtist = new Artist();
            newArtist.setName(artistName);
            newArtist.setBio("Artist profile pending.");
            return artistRepository.save(newArtist);
        });
        String imageUrl = saveImage(imageFile);
        if (imageUrl != null) {
            artwork.setImageUrl(imageUrl);
        }
        artwork.setArtist(artist);
        artworkRepository.save(artwork);
    }

    public void update(Long id, Artwork updatedData, String artistName, MultipartFile imageFile) {
        Artwork existing = findById(id);
        existing.setTitle(updatedData.getTitle());
        existing.setDescription(updatedData.getDescription());
        existing.setCategory(updatedData.getCategory());
        existing.setPrice(updatedData.getPrice());
        
        if (imageFile != null && !imageFile.isEmpty()) {
            String imageUrl = saveImage(imageFile);
            if (imageUrl != null) {
                existing.setImageUrl(imageUrl);
            }
        }
        
        Artist artist = artistRepository.findByName(artistName).orElseGet(() -> {
            Artist newArtist = new Artist();
            newArtist.setName(artistName);
            newArtist.setBio("Artist profile pending.");
            return artistRepository.save(newArtist);
        });
        existing.setArtist(artist);
        artworkRepository.save(existing);
    }

    public void incrementLike(Long id) {
        Artwork artwork = findById(id);
        artwork.setLikeCount(artwork.getLikeCount() + 1);
        artworkRepository.save(artwork);
    }

    public void delete(Long id) {
        artworkRepository.deleteById(id);
    }
}
