package com.assignment.bankingsystem.service;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.stereotype.Service;

import com.assignment.bankingsystem.entity.Account;
import com.assignment.bankingsystem.entity.BankTransaction;
import com.assignment.bankingsystem.entity.Customer;
import com.assignment.bankingsystem.exception.ResourceNotFoundException;
import com.assignment.bankingsystem.repository.AccountRepository;
import com.assignment.bankingsystem.repository.BankTransactionRepository;
import com.assignment.bankingsystem.repository.CustomerRepository;

@Service
public class BankingService {

    private final CustomerRepository customerRepository;
    private final AccountRepository accountRepository;
    private final BankTransactionRepository transactionRepository;

    public BankingService(CustomerRepository customerRepository, AccountRepository accountRepository,
            BankTransactionRepository transactionRepository) {
        this.customerRepository = customerRepository;
        this.accountRepository = accountRepository;
        this.transactionRepository = transactionRepository;
    }

    public List<Customer> getAllCustomers() {
        return customerRepository.findAll();
    }

    public List<Account> getAllAccounts() {
        return accountRepository.findAll();
    }

    public List<BankTransaction> getAllTransactions() {
        return transactionRepository.findAll();
    }

    public Customer saveCustomer(Customer customer) {
        return customerRepository.save(customer);
    }

    public Account saveAccount(Long customerId, Account account) {
        Customer customer = customerRepository.findById(customerId)
                .orElseThrow(() -> new ResourceNotFoundException("Customer not found"));
        account.setCustomer(customer);
        return accountRepository.save(account);
    }

    public Account deposit(Long accountId, double amount) {
        if (amount <= 0) {
            throw new ResourceNotFoundException("Deposit amount should be greater than zero");
        }
        Account account = accountRepository.findById(accountId)
                .orElseThrow(() -> new ResourceNotFoundException("Account not found"));
        account.setBalance(account.getBalance() + amount);
        accountRepository.save(account);
        saveTransaction(account, "DEPOSIT", amount);
        return account;
    }

    public Account withdraw(Long accountId, double amount) {
        if (amount <= 0) {
            throw new ResourceNotFoundException("Withdraw amount should be greater than zero");
        }
        Account account = accountRepository.findById(accountId)
                .orElseThrow(() -> new ResourceNotFoundException("Account not found"));
        if (account.getBalance() < amount) {
            throw new ResourceNotFoundException("Insufficient balance");
        }
        account.setBalance(account.getBalance() - amount);
        accountRepository.save(account);
        saveTransaction(account, "WITHDRAW", amount);
        return account;
    }

    private void saveTransaction(Account account, String type, double amount) {
        BankTransaction transaction = new BankTransaction();
        transaction.setAccount(account);
        transaction.setTransactionType(type);
        transaction.setAmount(amount);
        transaction.setTransactionTime(LocalDateTime.now());
        transactionRepository.save(transaction);
    }
}
