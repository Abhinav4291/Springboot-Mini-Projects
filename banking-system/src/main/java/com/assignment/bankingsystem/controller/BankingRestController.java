package com.assignment.bankingsystem.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.assignment.bankingsystem.entity.Account;
import com.assignment.bankingsystem.entity.BankTransaction;
import com.assignment.bankingsystem.entity.Customer;
import com.assignment.bankingsystem.service.BankingService;

@RestController
@RequestMapping("/api/banking")
public class BankingRestController {

    private final BankingService bankingService;

    public BankingRestController(BankingService bankingService) {
        this.bankingService = bankingService;
    }

    @GetMapping("/customers")
    public List<Customer> getCustomers() {
        return bankingService.getAllCustomers();
    }

    @GetMapping("/accounts")
    public List<Account> getAccounts() {
        return bankingService.getAllAccounts();
    }

    @GetMapping("/transactions")
    public List<BankTransaction> getTransactions() {
        return bankingService.getAllTransactions();
    }

    @PostMapping("/customers")
    public Customer addCustomer(@RequestBody Customer customer) {
        return bankingService.saveCustomer(customer);
    }

    @PostMapping("/accounts")
    public Account addAccount(@RequestParam Long customerId, @RequestBody Account account) {
        return bankingService.saveAccount(customerId, account);
    }

    @PostMapping("/deposit")
    public Account deposit(@RequestParam Long accountId, @RequestParam double amount) {
        return bankingService.deposit(accountId, amount);
    }

    @PostMapping("/withdraw")
    public Account withdraw(@RequestParam Long accountId, @RequestParam double amount) {
        return bankingService.withdraw(accountId, amount);
    }
}
