package com.artgallery.controller;

import com.artgallery.service.ArtworkService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.data.domain.Page;

@Controller
public class ArtworkController {

    private final ArtworkService artworkService;

    public ArtworkController(ArtworkService artworkService) {
        this.artworkService = artworkService;
    }

    @GetMapping("/")
    public String home(
            Model model, 
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(required = false) String keyword) {
        
        int pageSize = 6;
        Page<com.artgallery.entity.Artwork> artworkPage = artworkService.findPaginatedAndSorted(page, pageSize, keyword);
        
        model.addAttribute("artworks", artworkPage.getContent());
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", artworkPage.getTotalPages());
        model.addAttribute("keyword", keyword);
        
        return "index";
    }

    @PostMapping("/artworks/{id}/like")
    public String likeArtwork(@PathVariable Long id) {
        artworkService.incrementLike(id);
        return "redirect:/";
    }
}
