package com.assignment.librarymanagement.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.assignment.librarymanagement.entity.Author;

public interface AuthorRepository extends JpaRepository<Author, Long> {

    Author findByNameIgnoreCase(String name);

    List<Author> findByNameContainingIgnoreCase(String name);
}
