package com.assignment.moviebooking.config;

import java.util.ArrayList;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.assignment.moviebooking.entity.Movie;
import com.assignment.moviebooking.entity.Theater;
import com.assignment.moviebooking.repository.MovieRepository;
import com.assignment.moviebooking.repository.TheaterRepository;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner loadMovieData(TheaterRepository theaterRepository, MovieRepository movieRepository) {
        return args -> {
            if (theaterRepository.count() == 0) {
                Theater theater = new Theater();
                theater.setName("PVR Central");
                theater.setLocation("City Mall");
                theater.setMovies(new ArrayList<>());
                theaterRepository.save(theater);

                Movie movie = new Movie();
                movie.setTitle("Campus Days");
                movie.setAvailableSeats(80);
                movie.setTheater(theater);
                movie.setTickets(new ArrayList<>());
                movieRepository.save(movie);
            }
        };
    }
}
