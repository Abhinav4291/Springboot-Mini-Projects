package com.assignment.librarymanagement.config;

import java.util.ArrayList;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.assignment.librarymanagement.entity.Author;
import com.assignment.librarymanagement.entity.Book;
import com.assignment.librarymanagement.entity.Member;
import com.assignment.librarymanagement.repository.BookRepository;
import com.assignment.librarymanagement.repository.MemberRepository;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner loadLibraryData(BookRepository bookRepository, MemberRepository memberRepository) {
        return args -> {
            if (bookRepository.count() == 0) {
                Author author1 = new Author();
                author1.setName("R.K. Narayan");
                author1.setEmail("narayan@example.com");

                Author author2 = new Author();
                author2.setName("Chetan Bhagat");
                author2.setEmail("chetan@example.com");

                Book book1 = new Book();
                book1.setTitle("Malgudi Days");
                book1.setIsbn("LIB-101");
                book1.setIssued(false);
                book1.setAuthors(new ArrayList<>());
                book1.getAuthors().add(author1);

                Book book2 = new Book();
                book2.setTitle("Five Point Someone");
                book2.setIsbn("LIB-102");
                book2.setIssued(false);
                book2.setAuthors(new ArrayList<>());
                book2.getAuthors().add(author2);

                bookRepository.save(book1);
                bookRepository.save(book2);
            }

            if (memberRepository.count() == 0) {
                Member member = new Member();
                member.setName("Abhinav");
                member.setPhoneNumber("9123456789");
                member.setIssuedBooks(new ArrayList<>());
                memberRepository.save(member);
            }
        };
    }
}
