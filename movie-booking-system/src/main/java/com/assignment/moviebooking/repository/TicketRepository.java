package com.assignment.moviebooking.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.assignment.moviebooking.entity.Ticket;

public interface TicketRepository extends JpaRepository<Ticket, Long> {

    List<Ticket> findByMovieId(Long movieId);
}
