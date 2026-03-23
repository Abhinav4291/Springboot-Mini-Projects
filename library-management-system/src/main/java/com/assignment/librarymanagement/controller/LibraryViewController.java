package com.assignment.librarymanagement.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.assignment.librarymanagement.entity.Book;
import com.assignment.librarymanagement.entity.Member;
import com.assignment.librarymanagement.service.LibraryService;

@Controller
public class LibraryViewController {

    private final LibraryService libraryService;

    public LibraryViewController(LibraryService libraryService) {
        this.libraryService = libraryService;
    }

    @GetMapping("/")
    public String home(@RequestParam(required = false) String authorName, Model model) {
        model.addAttribute("books", authorName == null || authorName.isBlank()
                ? libraryService.getAllBooks()
                : libraryService.getBooksByAuthor(authorName));
        model.addAttribute("members", libraryService.getAllMembers());
        model.addAttribute("authorName", authorName == null ? "" : authorName);
        model.addAttribute("book", new Book());
        model.addAttribute("member", new Member());
        return "index";
    }

    @PostMapping("/books/save")
    public String saveBook(Book book,
            @RequestParam String authorName,
            @RequestParam(required = false) String authorEmail) {
        libraryService.saveBookWithAuthor(book, authorName, authorEmail);
        return "redirect:/";
    }

    @PostMapping("/members/save")
    public String saveMember(Member member) {
        libraryService.saveMember(member);
        return "redirect:/";
    }

    @PostMapping("/issue-book")
    public String issueBook(@RequestParam Long memberId, @RequestParam Long bookId) {
        libraryService.issueBook(memberId, bookId);
        return "redirect:/";
    }

    @PostMapping("/return-book")
    public String returnBook(@RequestParam Long memberId, @RequestParam Long bookId) {
        libraryService.returnBook(memberId, bookId);
        return "redirect:/";
    }
}
