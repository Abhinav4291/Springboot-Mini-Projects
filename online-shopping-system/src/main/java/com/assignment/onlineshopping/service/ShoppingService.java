package com.assignment.onlineshopping.service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.assignment.onlineshopping.entity.Customer;
import com.assignment.onlineshopping.entity.CustomerOrder;
import com.assignment.onlineshopping.entity.Product;
import com.assignment.onlineshopping.exception.ResourceNotFoundException;
import com.assignment.onlineshopping.repository.CustomerOrderRepository;
import com.assignment.onlineshopping.repository.CustomerRepository;
import com.assignment.onlineshopping.repository.ProductRepository;

@Service
public class ShoppingService {

    private final CustomerRepository customerRepository;
    private final ProductRepository productRepository;
    private final CustomerOrderRepository orderRepository;

    public ShoppingService(CustomerRepository customerRepository, ProductRepository productRepository,
            CustomerOrderRepository orderRepository) {
        this.customerRepository = customerRepository;
        this.productRepository = productRepository;
        this.orderRepository = orderRepository;
    }

    public List<Customer> getAllCustomers() {
        return customerRepository.findAll();
    }

    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    public List<CustomerOrder> getAllOrders() {
        return orderRepository.findAll();
    }

    public Customer saveCustomer(Customer customer) {
        return customerRepository.save(customer);
    }

    public Product saveProduct(Product product) {
        return productRepository.save(product);
    }

    public CustomerOrder placeOrder(Long customerId, Long productId, int quantity) {
        Customer customer = customerRepository.findById(customerId)
                .orElseThrow(() -> new ResourceNotFoundException("Customer not found"));
        Product product = productRepository.findById(productId)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found"));
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be at least 1");
        }
        if (quantity > product.getStock()) {
            throw new IllegalArgumentException("Requested quantity is higher than available stock");
        }

        product.setStock(product.getStock() - quantity);
        productRepository.save(product);

        CustomerOrder order = new CustomerOrder();
        order.setCustomer(customer);
        List<Product> products = new ArrayList<>();
        products.add(product);
        order.setProducts(products);
        order.setQuantity(quantity);
        order.setOrderDate(LocalDate.now());
        order.setTotalAmount(product.getPrice() * quantity);
        return orderRepository.save(order);
    }

    public List<CustomerOrder> getOrderHistoryByCustomer(Long customerId) {
        return orderRepository.findByCustomerIdOrderByOrderDateDesc(customerId);
    }
}
