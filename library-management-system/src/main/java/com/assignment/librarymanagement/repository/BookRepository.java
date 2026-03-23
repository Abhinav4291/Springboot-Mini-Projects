package com.assignment.librarymanagement.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.assignment.librarymanagement.entity.Book;

public interface BookRepository extends JpaRepository<Book, Long> {

    List<Book> findByAuthorsNameContainingIgnoreCase(String authorName);
}
