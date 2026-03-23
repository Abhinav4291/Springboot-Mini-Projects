package com.assignment.onlineshopping.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.assignment.onlineshopping.entity.CustomerOrder;

public interface CustomerOrderRepository extends JpaRepository<CustomerOrder, Long> {

    List<CustomerOrder> findByCustomerIdOrderByOrderDateDesc(Long customerId);
}
