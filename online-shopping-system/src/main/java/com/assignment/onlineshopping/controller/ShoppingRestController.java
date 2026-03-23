package com.assignment.onlineshopping.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.assignment.onlineshopping.entity.Customer;
import com.assignment.onlineshopping.entity.CustomerOrder;
import com.assignment.onlineshopping.entity.Product;
import com.assignment.onlineshopping.service.ShoppingService;

@RestController
@RequestMapping("/api/shopping")
public class ShoppingRestController {

    private final ShoppingService shoppingService;

    public ShoppingRestController(ShoppingService shoppingService) {
        this.shoppingService = shoppingService;
    }

    @GetMapping("/customers")
    public List<Customer> getCustomers() {
        return shoppingService.getAllCustomers();
    }

    @GetMapping("/products")
    public List<Product> getProducts() {
        return shoppingService.getAllProducts();
    }

    @GetMapping("/orders")
    public List<CustomerOrder> getOrders() {
        return shoppingService.getAllOrders();
    }

    @GetMapping("/orders/by-customer")
    public List<CustomerOrder> getOrdersByCustomer(@RequestParam("customerId") Long customerId) {
        return shoppingService.getOrderHistoryByCustomer(customerId);
    }

    @PostMapping("/customers")
    public Customer addCustomer(@RequestBody Customer customer) {
        return shoppingService.saveCustomer(customer);
    }

    @PostMapping("/products")
    public Product addProduct(@RequestBody Product product) {
        return shoppingService.saveProduct(product);
    }

    @PostMapping("/orders")
    public CustomerOrder placeOrder(@RequestParam("customerId") Long customerId,
            @RequestParam("productId") Long productId,
            @RequestParam("quantity") int quantity) {
        return shoppingService.placeOrder(customerId, productId, quantity);
    }
}
