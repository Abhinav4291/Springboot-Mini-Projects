package com.assignment.bankingsystem.config;

import java.util.ArrayList;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.assignment.bankingsystem.entity.Account;
import com.assignment.bankingsystem.entity.Customer;
import com.assignment.bankingsystem.repository.AccountRepository;
import com.assignment.bankingsystem.repository.CustomerRepository;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner loadBankingData(CustomerRepository customerRepository, AccountRepository accountRepository) {
        return args -> {
            if (customerRepository.count() == 0) {
                        Customer customer = new Customer();
                        customer.setName("Abhinav");
                        customer.setEmail("abhinav@example.com");
                customer.setAccounts(new ArrayList<>());
                customerRepository.save(customer);

                Account account = new Account();
                account.setAccountNumber("SB1001");
                account.setBalance(10000);
                account.setCustomer(customer);
                account.setTransactions(new ArrayList<>());
                accountRepository.save(account);
            }
        };
    }
}
