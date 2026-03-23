package com.assignment.librarymanagement.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.assignment.librarymanagement.entity.Author;
import com.assignment.librarymanagement.entity.Book;
import com.assignment.librarymanagement.entity.Member;
import com.assignment.librarymanagement.exception.ResourceNotFoundException;
import com.assignment.librarymanagement.repository.AuthorRepository;
import com.assignment.librarymanagement.repository.BookRepository;
import com.assignment.librarymanagement.repository.MemberRepository;

@Service
public class LibraryService {

    private final BookRepository bookRepository;
    private final AuthorRepository authorRepository;
    private final MemberRepository memberRepository;

    public LibraryService(BookRepository bookRepository, AuthorRepository authorRepository, MemberRepository memberRepository) {
        this.bookRepository = bookRepository;
        this.authorRepository = authorRepository;
        this.memberRepository = memberRepository;
    }

    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    public List<Author> getAllAuthors() {
        return authorRepository.findAll();
    }

    public List<Member> getAllMembers() {
        return memberRepository.findAll();
    }

    public Author saveAuthor(Author author) {
        if (author.getBooks() == null) {
            author.setBooks(new ArrayList<>());
        }
        return authorRepository.save(author);
    }

    public Book saveBookWithAuthor(Book book, String authorName, String authorEmail) {
        if (book.getAuthors() == null) {
            book.setAuthors(new ArrayList<>());
        }
        if (book.getMembers() == null) {
            book.setMembers(new ArrayList<>());
        }

        Author author = authorRepository.findByNameIgnoreCase(authorName);
        if (author == null) {
            author = new Author();
            author.setName(authorName);
            author.setEmail(authorEmail);
            author.setBooks(new ArrayList<>());
            author = authorRepository.save(author);
        } else if ((author.getEmail() == null || author.getEmail().isBlank()) && authorEmail != null && !authorEmail.isBlank()) {
            author.setEmail(authorEmail);
            author = authorRepository.save(author);
        }

        Long authorId = author.getId();
        boolean authorAlreadyAdded = false;
        for (Author existingAuthor : book.getAuthors()) {
            if (existingAuthor.getId() != null && existingAuthor.getId().equals(authorId)) {
                authorAlreadyAdded = true;
                break;
            }
        }
        if (!authorAlreadyAdded) {
            book.getAuthors().add(author);
        }

        if (author.getBooks() == null) {
            author.setBooks(new ArrayList<>());
        }
        boolean bookAlreadyLinked = false;
        for (Book existingBook : author.getBooks()) {
            if (existingBook.getIsbn() != null && existingBook.getIsbn().equalsIgnoreCase(book.getIsbn())) {
                bookAlreadyLinked = true;
                break;
            }
        }
        if (!bookAlreadyLinked) {
            author.getBooks().add(book);
        }

        return bookRepository.save(book);
    }

    public Member saveMember(Member member) {
        if (member.getIssuedBooks() == null) {
            member.setIssuedBooks(new ArrayList<>());
        }
        return memberRepository.save(member);
    }

    @Transactional
    public void issueBook(Long memberId, Long bookId) {
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found"));
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found"));

        boolean alreadyIssuedToMember = member.getIssuedBooks().stream()
                .anyMatch(existingBook -> existingBook.getId().equals(bookId));
        if (!alreadyIssuedToMember) {
            member.getIssuedBooks().add(book);
        }

        book.setIssued(true);
        memberRepository.save(member);
        bookRepository.save(book);
    }

    @Transactional
    public void returnBook(Long memberId, Long bookId) {
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found"));
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found"));

        member.getIssuedBooks().removeIf(existingBook -> existingBook.getId().equals(bookId));

        boolean stillIssuedToAnotherMember = memberRepository.findAll().stream()
                .filter(existingMember -> !existingMember.getId().equals(memberId))
                .anyMatch(existingMember -> existingMember.getIssuedBooks().stream()
                        .anyMatch(existingBook -> existingBook.getId().equals(bookId)));

        if (!stillIssuedToAnotherMember) {
            book.setIssued(false);
        }

        memberRepository.save(member);
        bookRepository.save(book);
    }

    public List<Book> getBooksByAuthor(String authorName) {
        if (authorName == null || authorName.isBlank()) {
            return getAllBooks();
        }

        return bookRepository.findByAuthorsNameContainingIgnoreCase(authorName.trim());
    }
}
