package com.assignment.onlineshopping.config;

import java.util.ArrayList;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.assignment.onlineshopping.entity.Customer;
import com.assignment.onlineshopping.entity.Product;
import com.assignment.onlineshopping.repository.CustomerRepository;
import com.assignment.onlineshopping.repository.ProductRepository;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner loadShoppingData(CustomerRepository customerRepository, ProductRepository productRepository) {
        return args -> {
            if (customerRepository.count() == 0) {
                        Customer customer = new Customer();
                        customer.setName("Rakshit Pandey");
                        customer.setEmail("rakshit@example.com");
                customer.setOrders(new ArrayList<>());
                customerRepository.save(customer);

                Product product1 = new Product();
                product1.setName("Laptop Bag");
                product1.setPrice(1200);
                product1.setStock(12);
                product1.setOrders(new ArrayList<>());

                Product product2 = new Product();
                product2.setName("Wireless Mouse");
                product2.setPrice(800);
                product2.setStock(20);
                product2.setOrders(new ArrayList<>());

                productRepository.save(product1);
                productRepository.save(product2);
            }
        };
    }
}
