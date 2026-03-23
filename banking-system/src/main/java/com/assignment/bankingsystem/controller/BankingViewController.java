package com.assignment.bankingsystem.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.assignment.bankingsystem.entity.Account;
import com.assignment.bankingsystem.entity.Customer;
import com.assignment.bankingsystem.service.BankingService;

@Controller
public class BankingViewController {

    private final BankingService bankingService;

    public BankingViewController(BankingService bankingService) {
        this.bankingService = bankingService;
    }

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("customers", bankingService.getAllCustomers());
        model.addAttribute("accounts", bankingService.getAllAccounts());
        model.addAttribute("transactions", bankingService.getAllTransactions());
        model.addAttribute("customer", new Customer());
        model.addAttribute("account", new Account());
        return "index";
    }

    @PostMapping("/customers/save")
    public String saveCustomer(Customer customer) {
        bankingService.saveCustomer(customer);
        return "redirect:/";
    }

    @PostMapping("/accounts/save")
    public String saveAccount(@RequestParam Long customerId, Account account) {
        bankingService.saveAccount(customerId, account);
        return "redirect:/";
    }

    @PostMapping("/deposit")
    public String deposit(@RequestParam Long accountId, @RequestParam double amount) {
        bankingService.deposit(accountId, amount);
        return "redirect:/";
    }

    @PostMapping("/withdraw")
    public String withdraw(@RequestParam Long accountId, @RequestParam double amount) {
        bankingService.withdraw(accountId, amount);
        return "redirect:/";
    }
}
