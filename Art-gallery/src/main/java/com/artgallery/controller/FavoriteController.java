package com.artgallery.controller;

import com.artgallery.service.FavoriteService;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/favorites")
public class FavoriteController {

    private final FavoriteService favoriteService;

    public FavoriteController(FavoriteService favoriteService) {
        this.favoriteService = favoriteService;
    }

    @GetMapping
    public String viewFavorites(Model model, Authentication auth) {
        model.addAttribute("artworks", favoriteService.getUserFavorites(auth.getName()));
        return "favorites";
    }

    @PostMapping("/toggle/{artworkId}")
    public String toggleFavorite(@PathVariable Long artworkId, Authentication auth) {
        favoriteService.toggleFavorite(artworkId, auth.getName());
        return "redirect:/"; // Could be enhanced to redirect to referer
    }
}
