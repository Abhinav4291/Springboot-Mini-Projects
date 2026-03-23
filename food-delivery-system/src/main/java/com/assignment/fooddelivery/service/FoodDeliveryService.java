package com.assignment.fooddelivery.service;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.assignment.fooddelivery.entity.AppUser;
import com.assignment.fooddelivery.entity.FoodOrder;
import com.assignment.fooddelivery.entity.Restaurant;
import com.assignment.fooddelivery.exception.ResourceNotFoundException;
import com.assignment.fooddelivery.repository.AppUserRepository;
import com.assignment.fooddelivery.repository.FoodOrderRepository;
import com.assignment.fooddelivery.repository.RestaurantRepository;

@Service
public class FoodDeliveryService {

    private final AppUserRepository appUserRepository;
    private final RestaurantRepository restaurantRepository;
    private final FoodOrderRepository foodOrderRepository;

    public FoodDeliveryService(AppUserRepository appUserRepository, RestaurantRepository restaurantRepository,
            FoodOrderRepository foodOrderRepository) {
        this.appUserRepository = appUserRepository;
        this.restaurantRepository = restaurantRepository;
        this.foodOrderRepository = foodOrderRepository;
    }

    public List<AppUser> getAllUsers() {
        return appUserRepository.findAll();
    }

    public List<Restaurant> getAllRestaurants() {
        return restaurantRepository.findAll();
    }

    public List<FoodOrder> getAllOrders() {
        return foodOrderRepository.findAll();
    }

    public AppUser saveUser(AppUser user) {
        return appUserRepository.save(user);
    }

    public Restaurant saveRestaurant(Restaurant restaurant) {
        return restaurantRepository.save(restaurant);
    }

    public FoodOrder placeOrder(Long userId, Long restaurantId, List<String> selectedItems, List<Integer> quantities) {
        AppUser user = appUserRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        Restaurant restaurant = restaurantRepository.findById(restaurantId)
                .orElseThrow(() -> new ResourceNotFoundException("Restaurant not found"));

        if (selectedItems == null || quantities == null || selectedItems.isEmpty() || quantities.isEmpty()) {
            throw new IllegalArgumentException("Please select at least one food item");
        }

        Map<String, Double> menu = parseMenu(restaurant.getMenuItems());
        StringBuilder itemsBuilder = new StringBuilder();
        double totalBill = 0;
        int validItemCount = 0;

        for (int i = 0; i < selectedItems.size(); i++) {
            String itemName = selectedItems.get(i);
            if (itemName == null || itemName.isBlank()) {
                continue;
            }

            int quantity = i < quantities.size() && quantities.get(i) != null ? quantities.get(i) : 0;
            if (quantity <= 0) {
                continue;
            }

            Double price = menu.get(itemName);
            if (price == null) {
                throw new IllegalArgumentException("Selected item does not belong to the chosen restaurant");
            }

            if (validItemCount > 0) {
                itemsBuilder.append(", ");
            }
            itemsBuilder.append(itemName).append(" x").append(quantity);
            totalBill += price * quantity;
            validItemCount++;
        }

        if (validItemCount == 0) {
            throw new IllegalArgumentException("Please select valid food items with quantity");
        }

        FoodOrder order = new FoodOrder();
        order.setUser(user);
        order.setRestaurant(restaurant);
        order.setItems(itemsBuilder.toString());
        order.setTotalAmount(totalBill);
        return foodOrderRepository.save(order);
    }

    public List<FoodOrder> getOrderHistoryForUser(Long userId) {
        return foodOrderRepository.findByUserIdOrderByIdDesc(userId);
    }

    public List<FoodOrder> getOrdersByRestaurant(Long restaurantId) {
        return foodOrderRepository.findByRestaurantIdOrderByIdDesc(restaurantId);
    }

    public double getTotalBillForUser(Long userId) {
        return foodOrderRepository.findByUserIdOrderByIdDesc(userId).stream()
                .mapToDouble(FoodOrder::getTotalAmount)
                .sum();
    }

    public Map<Long, List<Map<String, Object>>> getRestaurantMenus() {
        Map<Long, List<Map<String, Object>>> menus = new LinkedHashMap<>();
        for (Restaurant restaurant : getAllRestaurants()) {
            List<Map<String, Object>> items = new ArrayList<>();
            Map<String, Double> menu = parseMenu(restaurant.getMenuItems());
            for (Map.Entry<String, Double> entry : menu.entrySet()) {
                Map<String, Object> row = new LinkedHashMap<>();
                row.put("name", entry.getKey());
                row.put("price", entry.getValue());
                items.add(row);
            }
            menus.put(restaurant.getId(), items);
        }
        return menus;
    }

    private Map<String, Double> parseMenu(String rawMenu) {
        Map<String, Double> menu = new LinkedHashMap<>();
        if (rawMenu == null || rawMenu.isBlank()) {
            return menu;
        }

        String[] entries = rawMenu.split("\\|");
        for (String entry : entries) {
            String[] parts = entry.split(":");
            if (parts.length == 2) {
                menu.put(parts[0].trim(), Double.parseDouble(parts[1].trim()));
            }
        }
        return menu;
    }
}
