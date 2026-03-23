package com.assignment.moviebooking.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.assignment.moviebooking.entity.Movie;
import com.assignment.moviebooking.entity.Theater;
import com.assignment.moviebooking.service.MovieBookingService;

@Controller
public class MovieBookingViewController {

    private final MovieBookingService movieBookingService;

    public MovieBookingViewController(MovieBookingService movieBookingService) {
        this.movieBookingService = movieBookingService;
    }

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("theaters", movieBookingService.getAllTheaters());
        model.addAttribute("movies", movieBookingService.getAllMovies());
        model.addAttribute("tickets", movieBookingService.getAllTickets());
        model.addAttribute("theater", new Theater());
        model.addAttribute("movie", new Movie());
        return "index";
    }

    @PostMapping("/theaters/save")
    public String saveTheater(Theater theater) {
        movieBookingService.saveTheater(theater);
        return "redirect:/";
    }

    @PostMapping("/movies/save")
    public String saveMovie(@RequestParam Long theaterId, Movie movie) {
        movieBookingService.saveMovie(theaterId, movie);
        return "redirect:/";
    }

    @PostMapping("/tickets/save")
    public String bookTicket(@RequestParam Long movieId, @RequestParam String customerName,
            @RequestParam int seatCount) {
        movieBookingService.bookTicket(movieId, customerName, seatCount);
        return "redirect:/";
    }
}
