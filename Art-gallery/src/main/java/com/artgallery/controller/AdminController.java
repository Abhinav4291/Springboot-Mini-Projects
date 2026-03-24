package com.artgallery.controller;

import com.artgallery.entity.Artwork;
import com.artgallery.entity.Role;
import com.artgallery.service.ArtistService;
import com.artgallery.service.ArtworkService;
import com.artgallery.service.QueryService;
import com.artgallery.service.UserService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@Controller
@RequestMapping("/admin")
public class AdminController {

    private final ArtworkService artworkService;
    private final ArtistService artistService;
    private final QueryService queryService;
    private final UserService userService;

    public AdminController(ArtworkService artworkService, ArtistService artistService, QueryService queryService, UserService userService) {
        this.artworkService = artworkService;
        this.artistService = artistService;
        this.queryService = queryService;
        this.userService = userService;
    }

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        model.addAttribute("users", userService.findAllUsers());
        return "admin-dashboard";
    }

    @PostMapping("/users/{id}/toggle-block")
    public String toggleUserBlock(@PathVariable Long id) {
        userService.toggleBlockStatus(id);
        return "redirect:/admin/dashboard";
    }

    @GetMapping("/artworks")
    public String manageArtworks(Model model) {
        model.addAttribute("artworks", artworkService.findAll());
        return "manage-artworks";
    }

    @GetMapping("/artworks/new")
    public String addArtworkPage(Model model) {
        model.addAttribute("artists", artistService.findAll());
        return "add-artwork";
    }

    @PostMapping("/artworks")
    public String createArtwork(@ModelAttribute Artwork artwork, @RequestParam String artistName, @RequestParam("imageFile") MultipartFile imageFile) {
        artworkService.save(artwork, artistName, imageFile);
        return "redirect:/admin/artworks";
    }

    @GetMapping("/artworks/{id}/edit")
    public String editArtworkPage(@PathVariable Long id, Model model) {
        model.addAttribute("artwork", artworkService.findById(id));
        model.addAttribute("artists", artistService.findAll());
        return "edit-artwork";
    }

    @PostMapping("/artworks/{id}")
    public String updateArtwork(@PathVariable Long id, @ModelAttribute Artwork artwork, @RequestParam String artistName, @RequestParam(value = "imageFile", required = false) MultipartFile imageFile) {
        artworkService.update(id, artwork, artistName, imageFile);
        return "redirect:/admin/artworks";
    }

    @PostMapping("/artworks/{id}/delete")
    public String deleteArtwork(@PathVariable Long id) {
        artworkService.delete(id);
        return "redirect:/admin/artworks";
    }

    @GetMapping("/queries")
    public String viewQueries(Model model) {
        model.addAttribute("queries", queryService.findAll());
        return "view-queries";
    }

    @GetMapping("/users/new")
    public String createUserPage() {
        return "create-user";
    }

    @PostMapping("/users")
    public String createUserProcess(@RequestParam String name, @RequestParam String email, @RequestParam String password, @RequestParam Role role, Model model) {
        try {
            userService.registerUser(name, email, password, role);
            return "redirect:/admin/dashboard?userCreated=true";
        } catch (IllegalArgumentException e) {
            model.addAttribute("error", e.getMessage());
            return "create-user";
        }
    }
}
