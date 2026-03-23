package com.assignment.fooddelivery.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.assignment.fooddelivery.entity.FoodOrder;

public interface FoodOrderRepository extends JpaRepository<FoodOrder, Long> {

    List<FoodOrder> findByUserIdOrderByIdDesc(Long userId);

    List<FoodOrder> findByRestaurantIdOrderByIdDesc(Long restaurantId);
}
