package com.assignment.moviebooking.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.assignment.moviebooking.entity.Movie;
import com.assignment.moviebooking.entity.Theater;
import com.assignment.moviebooking.entity.Ticket;
import com.assignment.moviebooking.exception.ResourceNotFoundException;
import com.assignment.moviebooking.repository.MovieRepository;
import com.assignment.moviebooking.repository.TheaterRepository;
import com.assignment.moviebooking.repository.TicketRepository;

@Service
public class MovieBookingService {

    private final TheaterRepository theaterRepository;
    private final MovieRepository movieRepository;
    private final TicketRepository ticketRepository;

    public MovieBookingService(TheaterRepository theaterRepository, MovieRepository movieRepository,
            TicketRepository ticketRepository) {
        this.theaterRepository = theaterRepository;
        this.movieRepository = movieRepository;
        this.ticketRepository = ticketRepository;
    }

    public List<Theater> getAllTheaters() {
        return theaterRepository.findAll();
    }

    public List<Movie> getAllMovies() {
        return movieRepository.findAll();
    }

    public List<Ticket> getAllTickets() {
        return ticketRepository.findAll();
    }

    public Theater saveTheater(Theater theater) {
        return theaterRepository.save(theater);
    }

    public Movie saveMovie(Long theaterId, Movie movie) {
        Theater theater = theaterRepository.findById(theaterId)
                .orElseThrow(() -> new ResourceNotFoundException("Theater not found"));
        movie.setTheater(theater);
        return movieRepository.save(movie);
    }

    public Ticket bookTicket(Long movieId, String customerName, int seatCount) {
        Movie movie = movieRepository.findById(movieId)
                .orElseThrow(() -> new ResourceNotFoundException("Movie not found"));
        if (movie.getAvailableSeats() < seatCount) {
            throw new ResourceNotFoundException("Requested seats not available");
        }
        movie.setAvailableSeats(movie.getAvailableSeats() - seatCount);
        movieRepository.save(movie);
        Ticket ticket = new Ticket();
        ticket.setMovie(movie);
        ticket.setCustomerName(customerName);
        ticket.setSeatCount(seatCount);
        return ticketRepository.save(ticket);
    }

    public List<Ticket> getTicketsByMovie(Long movieId) {
        return ticketRepository.findByMovieId(movieId);
    }
}
