package com.assignment.fooddelivery.controller;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.assignment.fooddelivery.entity.AppUser;
import com.assignment.fooddelivery.entity.FoodOrder;
import com.assignment.fooddelivery.entity.Restaurant;
import com.assignment.fooddelivery.service.FoodDeliveryService;

@RestController
@RequestMapping("/api/food")
public class FoodDeliveryRestController {

    private final FoodDeliveryService foodDeliveryService;

    public FoodDeliveryRestController(FoodDeliveryService foodDeliveryService) {
        this.foodDeliveryService = foodDeliveryService;
    }

    @GetMapping("/users")
    public List<AppUser> getUsers() {
        return foodDeliveryService.getAllUsers();
    }

    @GetMapping("/restaurants")
    public List<Restaurant> getRestaurants() {
        return foodDeliveryService.getAllRestaurants();
    }

    @GetMapping("/menus")
    public Map<Long, List<Map<String, Object>>> getMenus() {
        return foodDeliveryService.getRestaurantMenus();
    }

    @GetMapping("/orders")
    public List<FoodOrder> getOrders() {
        return foodDeliveryService.getAllOrders();
    }

    @GetMapping("/orders/by-user")
    public List<FoodOrder> getOrdersByUser(@RequestParam("userId") Long userId) {
        return foodDeliveryService.getOrderHistoryForUser(userId);
    }

    @GetMapping("/orders/by-restaurant")
    public List<FoodOrder> getOrdersByRestaurant(@RequestParam("restaurantId") Long restaurantId) {
        return foodDeliveryService.getOrdersByRestaurant(restaurantId);
    }

    @GetMapping("/total-bill")
    public double getTotalBill(@RequestParam("userId") Long userId) {
        return foodDeliveryService.getTotalBillForUser(userId);
    }

    @PostMapping("/users")
    public AppUser addUser(@RequestBody AppUser user) {
        return foodDeliveryService.saveUser(user);
    }

    @PostMapping("/restaurants")
    public Restaurant addRestaurant(@RequestBody Restaurant restaurant) {
        return foodDeliveryService.saveRestaurant(restaurant);
    }

    @PostMapping("/orders")
    public FoodOrder placeOrder(@RequestParam("userId") Long userId,
            @RequestParam("restaurantId") Long restaurantId,
            @RequestParam("menuItem") List<String> menuItems,
            @RequestParam("quantity") List<Integer> quantities) {
        return foodDeliveryService.placeOrder(userId, restaurantId, menuItems, quantities);
    }
}
