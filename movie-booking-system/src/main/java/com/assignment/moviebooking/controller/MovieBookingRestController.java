package com.assignment.moviebooking.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.assignment.moviebooking.entity.Movie;
import com.assignment.moviebooking.entity.Theater;
import com.assignment.moviebooking.entity.Ticket;
import com.assignment.moviebooking.service.MovieBookingService;

@RestController
@RequestMapping("/api/movies")
public class MovieBookingRestController {

    private final MovieBookingService movieBookingService;

    public MovieBookingRestController(MovieBookingService movieBookingService) {
        this.movieBookingService = movieBookingService;
    }

    @GetMapping("/theaters")
    public List<Theater> getTheaters() {
        return movieBookingService.getAllTheaters();
    }

    @GetMapping("/list")
    public List<Movie> getMovies() {
        return movieBookingService.getAllMovies();
    }

    @GetMapping("/tickets")
    public List<Ticket> getTickets() {
        return movieBookingService.getAllTickets();
    }

    @GetMapping("/tickets/by-movie")
    public List<Ticket> getTicketsByMovie(@RequestParam Long movieId) {
        return movieBookingService.getTicketsByMovie(movieId);
    }

    @PostMapping("/theaters")
    public Theater addTheater(@RequestBody Theater theater) {
        return movieBookingService.saveTheater(theater);
    }

    @PostMapping("/movies")
    public Movie addMovie(@RequestParam Long theaterId, @RequestBody Movie movie) {
        return movieBookingService.saveMovie(theaterId, movie);
    }

    @PostMapping("/book")
    public Ticket bookTicket(@RequestParam Long movieId, @RequestParam String customerName,
            @RequestParam int seatCount) {
        return movieBookingService.bookTicket(movieId, customerName, seatCount);
    }
}
