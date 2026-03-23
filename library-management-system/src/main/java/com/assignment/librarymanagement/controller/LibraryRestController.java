package com.assignment.librarymanagement.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.assignment.librarymanagement.entity.Author;
import com.assignment.librarymanagement.entity.Book;
import com.assignment.librarymanagement.entity.Member;
import com.assignment.librarymanagement.service.LibraryService;

@RestController
@RequestMapping("/api/library")
public class LibraryRestController {

    private final LibraryService libraryService;

    public LibraryRestController(LibraryService libraryService) {
        this.libraryService = libraryService;
    }

    @GetMapping("/books")
    public List<Book> getBooks() {
        return libraryService.getAllBooks();
    }

    @GetMapping("/authors")
    public List<Author> getAuthors() {
        return libraryService.getAllAuthors();
    }

    @GetMapping("/members")
    public List<Member> getMembers() {
        return libraryService.getAllMembers();
    }

    @PostMapping("/books")
    public Book addBook(@RequestBody Book book,
            @RequestParam String authorName,
            @RequestParam(required = false) String authorEmail) {
        return libraryService.saveBookWithAuthor(book, authorName, authorEmail);
    }

    @PostMapping("/authors")
    public Author addAuthor(@RequestBody Author author) {
        return libraryService.saveAuthor(author);
    }

    @PostMapping("/members")
    public Member addMember(@RequestBody Member member) {
        return libraryService.saveMember(member);
    }

    @PostMapping("/issue")
    public ResponseEntity<String> issueBook(@RequestParam Long memberId, @RequestParam Long bookId) {
        libraryService.issueBook(memberId, bookId);
        return ResponseEntity.ok("Book issued successfully");
    }

    @PostMapping("/return")
    public ResponseEntity<String> returnBook(@RequestParam Long memberId, @RequestParam Long bookId) {
        libraryService.returnBook(memberId, bookId);
        return ResponseEntity.ok("Book returned successfully");
    }

    @GetMapping("/books/by-author/{authorName}")
    public List<Book> getBooksByAuthor(@PathVariable String authorName) {
        return libraryService.getBooksByAuthor(authorName);
    }
}
